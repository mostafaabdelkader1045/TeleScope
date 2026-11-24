from os import getenv

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_db_connection():
    """Create and return a PostgreSQL connection."""

    config = {
        "host": getenv("POSTGRES_HOST", "localhost"),
        "port": getenv("POSTGRES_PORT", "5432"),
        "dbname": getenv("POSTGRES_DB"),
        "user": getenv("POSTGRES_USER"),
        "password": getenv("POSTGRES_PASSWORD"),
    }

    required_fields = ["dbname", "user", "password"]

    for field in required_fields:
        if not config[field]:
            raise ValueError(f"POSTGRES_{field.upper()} is missing.")

    return psycopg.connect(**config)