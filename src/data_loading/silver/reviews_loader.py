import csv
import io

from src.data_loading.connections.azure_connection import download_blob
from src.data_loading.connections.database_connection import get_db_connection


TABLE_NAME = "silver.silver_reviewsdata" 

REVIEW_FILES = [
    "silver/com.etisalat_ar_reviews.csv",
    "silver/com.etisalat_en_reviews.csv",
    "silver/com.ucare.we_ar_reviews.csv",
    "silver/com.ucare.we_en_reviews.csv",
    "silver/com.emeint.android.myservices_arabic_reviews.csv",
    "silver/com.emeint.android.myservices_english_reviews.csv",
    "silver/com.orange.mobinilandme_arabic_reviews.csv",
    "silver/com.orange.mobinilandme_english_reviews.csv",       
]

CSV_COLUMNS = ["reviewId", "content", "score", "thumbsUpCount", "reviewCreatedVersion", "at", "replyContent", "repliedAt", "appVersion",
    "provider", "review_date", "clean_text", "word_count", "char_count", "exclam_count", "year", "month", "has_reply", "sentiment", 
    "label", "filtered_text",
]

DB_COLUMNS = [ "review_id", "content", "score", "thumbs_up_count", "review_created_version", "at", "reply_content", "replied_at", "app_version",
    "provider_name", "review_date", "clean_text", "word_count", "char_count", "exclam_count", "year", "month", "has_reply", "sentiment",
    "label", "filtered_text",
]


INTEGER_COLUMNS = { "score", "thumbsUpCount", "word_count", "char_count", "exclam_count", "year", "month",}
BOOLEAN_COLUMNS = { "has_reply"}

def convert_value(column, value):
    if value in ("", None):
        return None

    if column in INTEGER_COLUMNS:
        return int(float(value))

    if column in BOOLEAN_COLUMNS:
        value = value.strip().lower()

        if value in ("true", "1", "yes"):
            return True

        if value in ("false", "0", "no"):
            return False

        raise ValueError(f"Invalid boolean value for {column}: {value}")

    return value


def load_reviews_file(blob_name):
    print(f"\nLoading file: {blob_name}")
    # 1. Download CSV from Azure Blob Storage
    blob_data = download_blob(blob_name)
    if not blob_data:
        raise ValueError(f"File is empty: {blob_name}")

    # 2. Read CSV
    csv_data = blob_data.decode("utf-8-sig")
    csv_file = io.StringIO(csv_data)
    reader = csv.DictReader(csv_file)

    # 3. Validate CSV headers
    if reader.fieldnames is None:
        raise ValueError(f"CSV file has no headers: {blob_name}")

    if reader.fieldnames != CSV_COLUMNS:
        raise ValueError(
            f"CSV columns do not match expected columns.\n"
            f"File: {blob_name}\n"
            f"Expected: {CSV_COLUMNS}\n"
            f"Received: {reader.fieldnames}"
        )

    # 4. Prepare CSV data for PostgreSQL COPY
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    rows_count = 0
    for row in reader:
        processed_row = []
        for csv_column, db_column in zip(CSV_COLUMNS, DB_COLUMNS):
            value = row[csv_column]
            value = convert_value(csv_column, value)
            processed_row.append(value)
        writer.writerow(processed_row)
        rows_count += 1

    if rows_count == 0:
        raise ValueError(f"No reviews found in CSV: {blob_name}")

    buffer.seek(0)
    print(f"Extracted rows: {rows_count}")
    return buffer, rows_count


def load_reviews():
    print("Silver Reviews Loading")
    # 1. Download and validate all files
    prepared_files = []
    total_expected_rows = 0
    for blob_name in REVIEW_FILES:
        buffer, rows_count = load_reviews_file(blob_name)
        prepared_files.append(
            {
                "blob_name": blob_name,
                "buffer": buffer,
                "rows_count": rows_count,
            }
        )

        total_expected_rows += rows_count

    print("All files downloaded and validated successfully.")
    print(f"Total expected rows: {total_expected_rows}")
    # 2. Connect to PostgreSQL
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Full Refresh
            cursor.execute(f"TRUNCATE TABLE {TABLE_NAME}")
            # 3. Load all files using COPY
            copy_sql = f"""
                COPY {TABLE_NAME} ({', '.join(DB_COLUMNS)})
                FROM STDIN
                WITH (FORMAT CSV, NULL '')
            """
            total_loaded_rows = 0
            with cursor.copy(copy_sql) as copy:
                for file_data in prepared_files:
                    buffer = file_data["buffer"]
                    blob_name = file_data["blob_name"]
                    rows_count = file_data["rows_count"]
                    print(f"\nLoading into database: {blob_name}")
                    while data := buffer.read(8192):
                        copy.write(data)
                    total_loaded_rows += rows_count
                    print(f"Loaded rows: {rows_count}")

            # 4. Validate loaded rows
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            loaded_count = cursor.fetchone()[0]
            if loaded_count != total_expected_rows:
                raise ValueError(
                    "Loading validation failed.\n"
                    f"Expected rows: {total_expected_rows}\n"
                    f"Loaded rows: {loaded_count}"
                )

        # 5. Commit
        conn.commit()
        print("Reviews loading completed successfully!")
        print(f"Expected rows: {total_expected_rows}")
        print(f"Loaded rows: {loaded_count}")
        return loaded_count

    except Exception as e:
        conn.rollback()
        print("\nReviews loading failed!")
        print(f"Error: {e}")
        raise

    finally:

        conn.close()


if __name__ == "__main__":
    load_reviews()