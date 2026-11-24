import csv
from datetime import date, datetime
from io import BytesIO, StringIO

from openpyxl import load_workbook

from src.data_loading.connections.azure_connection import download_blob
from src.data_loading.connections.database_connection import get_db_connection


SOURCE_BLOB = (
    "bronze/survey/"
    "استبيان تجربة عملاء شركات الاتصالات في مصر- Telescope (الردود).xlsx"
)

SHEET_NAME = "ردود النموذج 1"

TABLE_NAME = "bronze.raw_surveys"

COLUMNS = [
    "response_timestamp",
    "provider_name",
    "tenure",
    "network_coverage_rating",
    "internet_speed_rating",
    "value_for_money_rating",
    "customer_service_rating",
    "mobile_app_rating",
    "overall_satisfaction_rating",
    "network_importance",
    "value_for_money_importance",
    "customer_service_importance",
    "app_experience_importance",
    "offers_importance",
    "monthly_spending",
    "customer_comment",
]

BATCH_SIZE = 1000


def format_value(value):
    """Convert Excel values into strings for Bronze TEXT columns."""

    if value is None:
        return ""

    if isinstance(value, datetime):
        return value.isoformat(sep=" ")

    if isinstance(value, date):
        return value.isoformat()

    return str(value)


def load_survey():
    """Load survey responses from Azure Excel file into PostgreSQL."""

    # Download Excel file
    file_data = download_blob(SOURCE_BLOB)

    workbook = load_workbook(
        BytesIO(file_data),
        read_only=True,
        data_only=True
    )

    try:
        if SHEET_NAME not in workbook.sheetnames:
            raise ValueError(
                f"Worksheet '{SHEET_NAME}' was not found."
            )

        worksheet = workbook[SHEET_NAME]

        rows = worksheet.iter_rows(values_only=True)

        # Read and validate header
        header = next(rows, None)

        if header is None or len(header) != len(COLUMNS):
            raise ValueError(
                f"Unexpected number of columns in survey file. "
                f"Expected {len(COLUMNS)}."
            )

        copy_query = f"""
            COPY {TABLE_NAME} ({", ".join(COLUMNS)})
            FROM STDIN
            WITH (FORMAT CSV)
        """

        loaded_count = 0
        batch = StringIO(newline="")
        writer = csv.writer(batch)

        with get_db_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute(f"TRUNCATE TABLE {TABLE_NAME}")

                with cursor.copy(copy_query) as copy:

                    for row in rows:

                        # Skip completely empty rows
                        if all(value is None for value in row):
                            continue

                        if len(row) > len(COLUMNS):
                            if any(value is not None for value in row[len(COLUMNS):]):
                                raise ValueError(
                                    "Survey row contains unexpected extra columns."
                                )

                        # Match Excel columns with PostgreSQL columns by position
                        values = [
                            format_value(value)
                            for value in row[:len(COLUMNS)]
                        ]

                        # Fill missing trailing columns
                        values.extend(
                            [""] * (len(COLUMNS) - len(values))
                        )

                        writer.writerow(values)
                        loaded_count += 1

                        if loaded_count % BATCH_SIZE == 0:
                            copy.write(batch.getvalue())
                            batch.seek(0)
                            batch.truncate(0)

                    # Load remaining records
                    if batch.tell() > 0:
                        copy.write(batch.getvalue())

                if loaded_count == 0:
                    raise ValueError("No survey responses found.")

                # Verify loaded records
                cursor.execute(
                    f"SELECT COUNT(*) FROM {TABLE_NAME}"
                )

                db_count = cursor.fetchone()[0]

                if db_count != loaded_count:
                    raise ValueError(
                        f"Loading mismatch: "
                        f"Source={loaded_count}, Database={db_count}"
                    )

        return loaded_count

    finally:
        workbook.close()