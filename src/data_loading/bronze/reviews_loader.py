import csv
from io import BytesIO, StringIO, TextIOWrapper

from src.data_loading.connections.azure_connection import download_blob
from src.data_loading.connections.database_connection import get_db_connection


# Mapping between Azure Blob files and Bronze tables
REVIEW_SOURCES = {
    "bronze/reviews/my_we/com.ucare.we_ar_reviews.csv": {
        "table": "bronze.raw_reviews_we_ar",
        "provider": "WE",
        "language": "ar",
    },
    "bronze/reviews/my_we/com.ucare.we_en_reviews.csv": {
        "table": "bronze.raw_reviews_we_en",
        "provider": "WE",
        "language": "en",
    },
    "bronze/reviews/my_etisalat/com.etisalat_ar_reviews.csv": {
        "table": "bronze.raw_reviews_etisalat_ar",
        "provider": "ETISALAT",
        "language": "ar",
    },
    "bronze/reviews/my_etisalat/com.etisalat_en_reviews.csv": {
        "table": "bronze.raw_reviews_etisalat_en",
        "provider": "ETISALAT",
        "language": "en",
    },
}


# Source CSV columns mapped to Bronze column names
COLUMN_MAPPING = {
    "reviewId": "review_id",
    "userName": "user_name",
    "userImage": "user_image",
    "content": "content",
    "score": "score",
    "thumbsUpCount": "thumbs_up_count",
    "reviewCreatedVersion": "review_created_version",
    "at": "at",
    "replyContent": "reply_content",
    "repliedAt": "replied_at",
    "appVersion": "app_version",
}

COLUMNS = list(COLUMN_MAPPING.values())

BATCH_SIZE = 5000


def load_single_review_file(blob_name: str, table_name: str) -> int:
    """
    Download one review CSV file from Azure
    and load its records into the corresponding Bronze table.
    """

    # Download source file
    file_data = download_blob(blob_name)

    csv_file = TextIOWrapper(
        BytesIO(file_data),
        encoding="utf-8-sig",
        newline=""
    )

    reader = csv.DictReader(csv_file)

    # Validate source columns
    missing_columns = [
        column
        for column in COLUMN_MAPPING
        if column not in (reader.fieldnames or [])
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in {blob_name}: {missing_columns}"
        )

    copy_query = f"""
        COPY {table_name} ({", ".join(COLUMNS)})
        FROM STDIN
        WITH (FORMAT CSV)
    """

    loaded_count = 0
    batch = StringIO()
    writer = csv.writer(batch)

    with get_db_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(f"TRUNCATE TABLE {table_name}")

            with cursor.copy(copy_query) as copy:

                for row in reader:

                    values = [
                        row[source_column]
                        if row[source_column] is not None
                        else ""
                        for source_column in COLUMN_MAPPING
                    ]

                    writer.writerow(values)
                    loaded_count += 1

                    if loaded_count % BATCH_SIZE == 0:
                        copy.write(batch.getvalue())
                        batch.seek(0)
                        batch.truncate(0)

                # Load remaining records
                if batch.tell() > 0:
                    copy.write(batch.getvalue())

    csv_file.close()

    return loaded_count


def load_reviews() -> dict:
    """
    Load all configured review files into their Bronze tables.
    """

    results = {}

    for blob_name, source_info in REVIEW_SOURCES.items():

        table_name = source_info["table"]

        loaded_count = load_single_review_file(
            blob_name=blob_name,
            table_name=table_name
        )

        results[table_name] = loaded_count

    return results
 