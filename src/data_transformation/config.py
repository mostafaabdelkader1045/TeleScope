
import os
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]


# Data source configuration
DATA_SOURCE = os.getenv("DATA_SOURCE", "local").lower()


# Local data paths
RAW_DATA_PATH = Path(
    os.getenv(
        "RAW_DATA_PATH",
        str(BASE_DIR / "data" / "raw" / "all_offers.json"),
    )
)

PROCESSED_DATA_PATH = Path(
    os.getenv(
        "PROCESSED_DATA_PATH",
        str(BASE_DIR / "data" / "processed" / "cleaned_telecom_offers.csv"),
    )
)


# Azure Storage configuration
AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_CONTAINER = os.getenv("AZURE_CONTAINER")
AZURE_RAW_BLOB = os.getenv("AZURE_RAW_BLOB")
