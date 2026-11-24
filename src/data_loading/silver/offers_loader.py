import csv
import io

from src.data_loading.connections.azure_connection import download_blob
from src.data_loading.connections.database_connection import get_db_connection


BLOB_NAME = "silver/cleaned_telecom_offers.csv"

TABLE_NAME = "silver.silver_offers"

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
    "source_url",
    "offer_category",
]


def load_offers():

    print("=" * 50)
    print("Silver Offers Loading")
    print("=" * 50)

    # 1. Download CSV from Azure Blob Storage
    blob_data = download_blob(BLOB_NAME)

    if not blob_data:
        raise ValueError("Offers CSV file is empty.")

    # 2. Read CSV
    csv_data = blob_data.decode("utf-8-sig")

    csv_file = io.StringIO(csv_data)

    reader = csv.DictReader(csv_file)

    # 3. Validate CSV headers
    if reader.fieldnames is None:
        raise ValueError("CSV file has no headers.")

    if reader.fieldnames != COLUMNS:
        raise ValueError(
            "CSV columns do not match the expected columns.\n"
            f"Expected: {COLUMNS}\n"
            f"Received: {reader.fieldnames}"
        )

    rows = list(reader)

    if not rows:
        raise ValueError("No offers found in CSV.")

    print(f"Extracted rows: {len(rows)}")

    # 4. Prepare CSV data for PostgreSQL COPY
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    for row in rows:
        processed_row = []
        for column in COLUMNS:
            value = row[column]
            if value in ("", None):
                value = None
            elif column == "validity_days":
                value = int(float(value))
            processed_row.append(value)
        writer.writerow(processed_row)

    buffer.seek(0)

    # 5. Connect to PostgreSQL
    conn = get_db_connection()

    try:

        with conn.cursor() as cursor:
            # Full Refresh
            cursor.execute(f"TRUNCATE TABLE {TABLE_NAME}")
            # Bulk Loading using COPY
            copy_sql = f"""
                COPY {TABLE_NAME} ({', '.join(COLUMNS)})
                FROM STDIN
                WITH (FORMAT CSV, NULL '')
            """
            with cursor.copy(copy_sql) as copy:
                while data := buffer.read(8192):
                    copy.write(data)

            # 6. Validate loaded rows
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            loaded_count = cursor.fetchone()[0]
            if loaded_count != len(rows):
                raise ValueError(
                    "Loading validation failed.\n"
                    f"Expected rows: {len(rows)}\n"
                    f"Loaded rows: {loaded_count}"
                )

        # Commit
        conn.commit()
        print("\nLoading completed successfully!")
        print(f"Expected rows: {len(rows)}")
        print(f"Loaded rows: {loaded_count}")
        return loaded_count

    except Exception as e:
        conn.rollback()
        print("\nLoading failed!")
        print(f"Error: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    load_offers()