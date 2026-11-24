import csv
import json
from io import StringIO

from src.data_loading.connections.azure_connection import download_blob
from src.data_loading.connections.database_connection import get_db_connection


SOURCE_BLOB = "bronze/offers/all_offers.json"

TABLE_NAME = "bronze.raw_offers"

COLUMNS = [
    "provider_name",
    "offer_title",
    "offer_type",
    "price_egp",
    "quota_amount",
    "quota_unit",
    "speed_limit",
    "speed_unit",
    "validity_days",
    "offer_description",
    "target_customer",
    "scraped_at",
    "source_url",
]


def parse_offers(data: bytes) -> list[dict]:
    """Parse offers JSON, including files with missing separators."""

    text = data.decode("utf-8-sig").strip()

    try:
        offers = json.loads(text)

        if isinstance(offers, dict):
            offers = [offers]

    except json.JSONDecodeError:

        decoder = json.JSONDecoder()

        offers = []
        position = 0

        while position < len(text):

            while position < len(text) and (
                text[position].isspace()
                or text[position] in ",[]"
            ):
                position += 1

            if position >= len(text):
                break

            offer, position = decoder.raw_decode(text, position)

            if not isinstance(offer, dict):
                raise ValueError("Invalid offer record.")

            offers.append(offer)

    if not isinstance(offers, list):
        raise ValueError("Offers data must be a list.")

    return offers


def prepare_csv(offers: list[dict]) -> StringIO:
    """Convert offers into CSV format for PostgreSQL COPY."""

    buffer = StringIO()
    writer = csv.writer(buffer)

    for index, offer in enumerate(offers, start=1):

        missing_columns = [
            column for column in COLUMNS
            if column not in offer
        ]

        if missing_columns:
            raise ValueError(
                f"Offer {index} is missing columns: {missing_columns}"
            )

        writer.writerow([
            offer[column] for column in COLUMNS
        ])

    buffer.seek(0)

    return buffer


def load_offers() -> int:
    """Load offers from Azure Blob Storage into Bronze."""

    source_data = download_blob(SOURCE_BLOB)

    offers = parse_offers(source_data)

    if not offers:
        raise ValueError("No offers found in source file.")

    csv_buffer = prepare_csv(offers)

    copy_query = f"""
        COPY {TABLE_NAME} (
            {", ".join(COLUMNS)}
        )
        FROM STDIN
        WITH (FORMAT CSV)
    """

    with get_db_connection() as conn:

        with conn.cursor() as cursor:

            cursor.execute(f"TRUNCATE TABLE {TABLE_NAME}")

            with cursor.copy(copy_query) as copy:
                copy.write(csv_buffer.getvalue())

            cursor.execute(
                f"SELECT COUNT(*) FROM {TABLE_NAME}"
            )

            loaded_count = cursor.fetchone()[0]

            if loaded_count != len(offers):
                raise ValueError(
                    f"Validation failed: expected {len(offers)}, "
                    f"loaded {loaded_count}."
                )

    return loaded_count