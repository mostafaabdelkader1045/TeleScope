import csv
import io

from src.data_loading.connections.azure_connection import download_blob
from src.data_loading.connections.database_connection import get_db_connection


SURVEY_FILES = {
    "responses": {
        "blob_name": "silver/survey_responses.csv",
        "table_name": "silver.silver_survey_responses",
        "columns": [
            "response_id",
            "submitted_at",
            "submission_date",
            "company_name",
            "tenure_category",
            "spending_category",
            "comment_original",
            "is_nlp_eligible",
        ],
        "csv_columns": [
            "survey_response_id",
            "submitted_at",
            "submission_date",
            "company_name",
            "tenure_category",
            "spending_category",
            "comment_original",
            "is_nlp_eligible",
        ],
    },
    "ratings": {
        "blob_name": "silver/survey_ratings.csv",
        "table_name": "silver.silver_survey_ratings",
        "columns": [
            "response_id",
            "rating_category",
            "rating_score",
        ],
        "csv_columns": [
            "survey_response_id",
            "rating_category",
            "rating_score",
        ],
    },
    "preferences": {
        "blob_name": "silver/survey_preferences.csv",
        "table_name": "silver.silver_survey_preferences",
        "columns": [
            "response_id",
            "preference_factor",
            "importance_rank",
        ],
        "csv_columns": [
            "survey_response_id",
            "preference_factor",
            "importance_rank",
        ],
    },
}


def load_survey_table(blob_name, table_name, columns, csv_columns):
    # Extract
    blob_data = download_blob(blob_name)

    if not blob_data:
        raise ValueError(f"File is empty: {blob_name}")

    csv_data = blob_data.decode("utf-8-sig")
    csv_file = io.StringIO(csv_data)
    reader = csv.DictReader(csv_file)
    if reader.fieldnames is None:
        raise ValueError(f"CSV has no headers: {blob_name}")

    # Validate CSV headers
    if reader.fieldnames != csv_columns:
        raise ValueError(
            f"CSV headers mismatch for {table_name}.\n"
            f"Expected: {csv_columns}\n"
            f"Received: {reader.fieldnames}"
        )

    rows = list(reader)

    if not rows:
        raise ValueError(f"No rows found in {blob_name}")
    print(f"Extracted rows: {len(rows)}")

    # Transform
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    for row in rows:
        processed_row = []
        for csv_column, db_column in zip(csv_columns, columns):
            value = row[csv_column]
            if value in ("", None):
                value = None
            processed_row.append(value)
        writer.writerow(processed_row)
    buffer.seek(0)
    # Load
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE {table_name}")

            copy_sql = f"""
                COPY {table_name} ({', '.join(columns)})
                FROM STDIN
                WITH (FORMAT CSV, NULL '')
            """

            with cursor.copy(copy_sql) as copy:

                while data := buffer.read(8192):
                    copy.write(data)

            # Validation
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            loaded_count = cursor.fetchone()[0]
            if loaded_count != len(rows):

                raise ValueError(
                    f"Loading validation failed for {table_name}.\n"
                    f"Expected: {len(rows)}\n"
                    f"Loaded: {loaded_count}"
                )

        conn.commit()
        print(f"Successfully loaded: {table_name}")
        print(f"Expected rows: {len(rows)}")
        print(f"Loaded rows: {loaded_count}")
        return loaded_count

    except Exception as e:

        conn.rollback()
        print(f"Loading failed for {table_name}")
        print(f"Error: {e}")

        raise

    finally:

        conn.close()

def load_survey_responses():
    config = SURVEY_FILES["responses"]
    return load_survey_table(blob_name=config["blob_name"], table_name=config["table_name"], columns=config["columns"], csv_columns=config["csv_columns"])

def load_survey_ratings():
    config = SURVEY_FILES["ratings"]
    return load_survey_table(blob_name=config["blob_name"], table_name=config["table_name"], columns=config["columns"], csv_columns=config["csv_columns"])

def load_survey_preferences():
    config = SURVEY_FILES["preferences"]
    return load_survey_table(blob_name=config["blob_name"], table_name=config["table_name"], columns=config["columns"], csv_columns=config["csv_columns"])


def load_all_survey_data():
    print("=" * 60)
    print("Silver Survey Loading")
    print("=" * 60)
    load_survey_responses()
    load_survey_ratings()
    load_survey_preferences()
    print("\nAll Survey tables loaded successfully!")


if __name__ == "__main__":
    load_all_survey_data()