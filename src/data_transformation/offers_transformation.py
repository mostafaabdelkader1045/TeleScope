import json
import logging

from pathlib import Path

import pandas as pd

from .config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    DATA_SOURCE,
    AZURE_STORAGE_ACCOUNT,
    AZURE_CONTAINER,
    AZURE_RAW_BLOB,
)


# =========================================================
# 1. Logging Configuration
# =========================================================

logger = logging.getLogger(__name__)


# =========================================================
# 2. Mapping Dictionaries
# =========================================================

TYPE_MAP = {
    "Home DSL": "Home DSL",
    "eHome DSL": "Home DSL",
    "home_dsl": "Home DSL",
    "home_internet": "Home DSL",

    "home_dsl_red_benefit": "Home DSL (Red Benefit)",

    "home_internet_and_iptv": "Home Internet + IPTV",

    "landline_bundle": "Landline Bundle",
    "landline": "Landline",

    "Home Wireless": "Home Wireless",
    "eHome Wireless": "Home Wireless",

    "eHome Wireless Router": "Home Wireless Router",

    "mobile_internet": "Mobile Internet",
    "mobile_internet_plus": "Mobile Internet",

    "mobile_internet_app_plus": "Mobile App Bundle",
    "mobile_internet_mifi": "Mobile MiFi",

    "control_mobile": "Control Mobile",
    "postpaid_mobile": "Postpaid Mobile",
    "prepaid_mobile": "Prepaid Mobile",
}


CATEGORY_MAP = {
    "Home DSL": "Fixed Home",
    "Home DSL (Red Benefit)": "Fixed Home",
    "Home Internet + IPTV": "Fixed Home",
    "Landline Bundle": "Fixed Home",
    "Landline": "Fixed Home",

    "Home Wireless": "Home Wireless",
    "Home Wireless Router": "Home Wireless",

    "Mobile Internet": "Mobile Data",
    "Mobile App Bundle": "Mobile Data",
    "Mobile MiFi": "Mobile Data",

    "Control Mobile": "Mobile Plans",
    "Postpaid Mobile": "Mobile Plans",
    "Prepaid Mobile": "Mobile Plans",
}


QUOTA_UNIT_MAP = {
    "GBs": "GB",
    "MBs": "MB",
    "Megabytes": "MB",
    "unit": "Units",
    "minute": "Minutes",
}


# Keep MB unchanged until its meaning is verified
SPEED_UNIT_MAP = {
    "MB": "Mbps",
    "Mbps": "Mbps"
}

NUMERIC_COLUMNS = [
    "price_egp",
    "quota_amount",
    "speed_limit",
    "validity_days",
]


REQUIRED_COLUMNS = [
    "provider_name",
    "offer_title",
    "offer_type",
    "offer_category",
    "price_egp",
    "quota_amount",
    "quota_unit",
    "speed_limit",
    "speed_unit",
    "validity_days",
]


# =========================================================
# 3. JSON Parsing
# =========================================================

def parse_json_records(raw_data):
    """
    Parse a JSON array, a single JSON object,
    or concatenated JSON objects.
    """

    logger.info("Parsing JSON data")

    raw_data = raw_data.strip()

    if not raw_data:
        raise ValueError("Raw data is empty")

    # Try standard JSON first
    try:
        parsed_data = json.loads(raw_data)

        if isinstance(parsed_data, list):
            records = parsed_data

        elif isinstance(parsed_data, dict):
            records = [parsed_data]

        else:
            raise ValueError("Unexpected JSON structure")

    except json.JSONDecodeError:

        # Handle concatenated JSON objects
        decoder = json.JSONDecoder()

        records = []
        index = 0

        while index < len(raw_data):

            # Skip whitespace and commas
            while index < len(raw_data) and (
                raw_data[index].isspace()
                or raw_data[index] == ","
            ):
                index += 1

            if index >= len(raw_data):
                break

            record, index = decoder.raw_decode(
                raw_data,
                index
            )

            records.append(record)

    if not records:
        raise ValueError("No records found in JSON data")

    logger.info(
        "Successfully parsed %d records",
        len(records)
    )

    df = pd.json_normalize(records)

    logger.info("Parsed DataFrame shape: %s", df.shape)

    return df


# =========================================================
# 4. Load Local Data
# =========================================================

def load_local_data(file_path):
    """
    Load JSON data from a local file.
    """

    file_path = Path(file_path)

    logger.info("Loading local data from %s", file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    raw_data = file_path.read_text(
        encoding="utf-8"
    )

    df = parse_json_records(raw_data)

    logger.info("Local data loaded successfully")

    return df


# =========================================================
# 5. Load Azure Data
# =========================================================

def load_azure_data():
    """
    Load JSON data from Azure Blob Storage.
    Authentication is handled by DefaultAzureCredential.
    """

    logger.info("Loading data from Azure Blob Storage")

    from azure.identity import DefaultAzureCredential
    from azure.storage.blob import BlobServiceClient

    if not all([
        AZURE_STORAGE_ACCOUNT,
        AZURE_CONTAINER,
        AZURE_RAW_BLOB,
    ]):
        raise ValueError(
            "Missing Azure Storage configuration"
        )

    account_url = (
        f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net"
    )

    credential = DefaultAzureCredential()

    blob_service_client = BlobServiceClient(
        account_url=account_url,
        credential=credential,
    )

    blob_client = blob_service_client.get_blob_client(
        container=AZURE_CONTAINER,
        blob=AZURE_RAW_BLOB,
    )

    logger.info(
        "Downloading Azure blob: %s",
        AZURE_RAW_BLOB
    )

    raw_data = blob_client.download_blob().readall()

    logger.info(
        "Downloaded %d bytes from Azure",
        len(raw_data)
    )

    df = parse_json_records(
        raw_data.decode("utf-8")
    )

    logger.info("Azure data loaded successfully")

    return df


# =========================================================
# 6. Data Loading Dispatcher
# =========================================================

def load_data():
    """
    Load data according to DATA_SOURCE configuration.
    """

    logger.info("Starting data loading stage")

    if DATA_SOURCE == "local":

        df = load_local_data(
            RAW_DATA_PATH
        )

    elif DATA_SOURCE == "azure":

        df = load_azure_data()

    else:

        raise ValueError(
            f"Unsupported DATA_SOURCE: {DATA_SOURCE}"
        )

    logger.info(
        "Data loading completed. Shape: %s",
        df.shape
    )

    return df


# =========================================================
# 7. Standardize Offer Types
# =========================================================

def standardize_offer_types(df):
    """
    Standardize provider names and offer types.
    """

    logger.info("Standardizing provider names and offer types")

    df = df.copy()

    df["provider_name"] = (
        df["provider_name"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    df["offer_type"] = (
        df["offer_type"]
        .astype("string")
        .str.strip()
        .replace(TYPE_MAP)
    )

    unmapped_types = df.loc[
        ~df["offer_type"].isin(set(TYPE_MAP.values())),
        "offer_type"
    ].dropna().unique()

    if len(unmapped_types):

        logger.warning(
            "Unmapped offer types: %s",
            unmapped_types.tolist()
        )

    else:

        logger.info("All offer types mapped successfully")

    return df


# =========================================================
# 8. Standardize Categories
# =========================================================

def standardize_categories(df):
    """
    Map standardized offer types to offer categories.
    """

    logger.info("Standardizing offer categories")

    df = df.copy()

    df["offer_category"] = (
        df["offer_type"].map(CATEGORY_MAP)
    )

    unmapped_categories = df.loc[
        df["offer_category"].isna(),
        "offer_type"
    ].dropna().unique()

    if len(unmapped_categories):

        logger.warning(
            "Unmapped offer categories: %s",
            unmapped_categories.tolist()
        )

    else:

        logger.info(
            "All offer categories mapped successfully"
        )

    return df


# =========================================================
# 9. Handle Missing Values
# =========================================================

def handle_missing_values(df):
    """
    Fill validity for verified annual WE landline offers.
    """

    logger.info("Handling missing values")

    df = df.copy()

    annual_we_mask = (
        df["provider_name"].eq("We")
        & df["offer_type"].eq("Landline Bundle")
        & df["validity_days"].isna()
    )

    filled_count = annual_we_mask.sum()

    df.loc[
        annual_we_mask,
        "validity_days"
    ] = 365

    logger.info(
        "Filled validity for %d annual WE landline offers",
        filled_count
    )

    return df


# =========================================================
# 10. Convert Gbps to Mbps
# =========================================================

def convert_speed_to_mbps(df):
    """
    Convert speeds from Gbps to Mbps.

    1 Gbps = 1000 Mbps
    """

    logger.info("Converting Gbps speeds to Mbps")

    df = df.copy()

    gbps_mask = (
        df["speed_unit"]
        .astype("string")
        .str.strip()
        .eq("Gbps")
    )

    converted_count = gbps_mask.sum()

    df.loc[
        gbps_mask,
        "speed_limit"
    ] = (
        df.loc[gbps_mask, "speed_limit"] * 1000
    )

    df.loc[
        gbps_mask,
        "speed_unit"
    ] = "Mbps"

    logger.info(
        "Converted %d records from Gbps to Mbps",
        converted_count
    )

    return df


# =========================================================
# 11. Standardize Units
# =========================================================

def standardize_units(df):
    """
    Standardize quota units and speed unit labels.
    """

    logger.info("Standardizing units")

    df = df.copy()

    df["quota_unit"] = (
        df["quota_unit"]
        .replace(QUOTA_UNIT_MAP)
    )

    df["speed_unit"] = (
        df["speed_unit"]
        .replace(SPEED_UNIT_MAP)
    )

    logger.info("Unit standardization completed")

    return df


# =========================================================
# 12. Handle Missing Speeds
# =========================================================

def handle_missing_speeds(df):
    """
    Fill verified Orange Home Wireless speeds
    based on offer descriptions.
    """

    logger.info("Handling missing speeds")

    df = df.copy()

    orange_mask = (
        df["provider_name"].eq("Orange")
        & df["offer_type"].eq("Home Wireless")
        & df["speed_limit"].isna()
    )

    filled_count = orange_mask.sum()

    df.loc[
        orange_mask,
        "speed_limit"
    ] = 3600

    df.loc[
        orange_mask,
        "speed_unit"
    ] = "Mbps"

    logger.info(
        "Filled Orange Home Wireless speeds: %d records",
        filled_count
    )

    return df


# =========================================================
# 13. Numeric Conversion
# =========================================================

def convert_numeric_columns(df):
    """
    Convert numeric columns to numeric data types.
    Invalid non-null values raise an error.
    """

    logger.info("Converting numeric columns")

    df = df.copy()

    for column in NUMERIC_COLUMNS:

        if column not in df.columns:
            continue

        original = df[column]

        converted = pd.to_numeric(
            original,
            errors="coerce"
        )

        invalid_values = (
            original.notna()
            & converted.isna()
        )

        if invalid_values.any():

            examples = (
                original.loc[invalid_values]
                .head(5)
                .tolist()
            )

            raise ValueError(
                f"Invalid numeric values in {column}: {examples}"
            )

        df[column] = converted

        logger.info(
            "Converted column %s to numeric",
            column
        )

    return df


# =========================================================
# 14. Data Validation
# =========================================================

def validate_offers(df):
    """
    Validate the transformed dataset.
    """

    logger.info("Starting data validation")

    # Empty dataset
    if df.empty:

        raise ValueError(
            "Validation failed: dataset is empty"
        )

    # Required columns
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    logger.info("Required columns check passed")

    # Numeric validation
    price = df["price_egp"]
    quota = df["quota_amount"]
    speed = df["speed_limit"]
    validity = df["validity_days"]

    invalid_counts = {
        "negative_prices": price.lt(0).sum(),
        "negative_quotas": quota.lt(0).sum(),
        "non_positive_speeds": speed.le(0).sum(),
        "non_positive_validity": validity.le(0).sum(),
    }

    for check_name, count in invalid_counts.items():

        if count > 0:

            logger.error(
                "%s: %d records",
                check_name,
                count
            )

    if any(invalid_counts.values()):

        raise ValueError(
            f"Numeric validation failed: {invalid_counts}"
        )

    logger.info("Numeric validation passed")

    # Category validation
    unmapped_types = df.loc[
        ~df["offer_type"].isin(set(TYPE_MAP.values())),
        "offer_type"
    ].dropna().unique()

    if len(unmapped_types):

        logger.warning(
            "Unmapped offer types: %s",
            unmapped_types.tolist()
        )

    unmapped_categories = df.loc[
        df["offer_category"].isna(),
        "offer_type"
    ].dropna().unique()

    if len(unmapped_categories):

        logger.warning(
            "Offers with missing categories: %s",
            unmapped_categories.tolist()
        )

    # Missing values
    missing_counts = (
        df.isna()
        .sum()
    )

    missing_counts = (
        missing_counts[missing_counts > 0]
    )

    if not missing_counts.empty:

        logger.warning(
            "Missing values detected: %s",
            missing_counts.to_dict()
        )

    else:

        logger.info("No missing values found")

    # Duplicate validation
    duplicate_count = df.duplicated().sum()

    if duplicate_count:

        logger.warning(
            "Found %d duplicate records",
            duplicate_count
        )

    else:

        logger.info("No duplicate records found")

    logger.info(
        "Validation completed successfully. Shape: %s",
        df.shape
    )

    return df


# =========================================================
# 15. Transformation Pipeline
# =========================================================

def transform_offers(df):
    """
    Apply all transformation steps.
    """

    logger.info("Starting transformation pipeline")

    logger.info(
        "Initial shape: %s",
        df.shape
    )

    # Standardization
    df = standardize_offer_types(df)

    df = standardize_categories(df)

    # Missing values
    df = handle_missing_values(df)

    # Numeric data types
    df = convert_numeric_columns(df)

    # Speed conversion must happen before unit standardization
    df = convert_speed_to_mbps(df)

    # Unit standardization
    df = standardize_units(df)

    # Known missing speed values
    df = handle_missing_speeds(df)

    
    # Remove unnecessary column
    if "scraped_at" in df.columns:

        df = df.drop(
            columns=["scraped_at"]
        )

        logger.info("Removed scraped_at column")

    # Data validation
    df = validate_offers(df)

    logger.info("Transformation completed successfully")

    logger.info(
        "Final shape: %s",
        df.shape
    )

    return df


# =========================================================
# 16. Save Processed Data
# =========================================================

def save_data(df, output_path):
    """
    Save transformed data to CSV.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info(
        "Saving processed data to %s",
        output_path
    )

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    logger.info(
        "Data saved successfully. Records: %d",
        len(df)
    )

    return output_path


# =========================================================
# 17. Main Pipeline
# =========================================================

def run_transformation():
    """
    Execute the complete transformation pipeline.
    """

    logger.info("=" * 60)

    logger.info(
        "Telecom Offers Transformation Started"
    )

    logger.info("=" * 60)

    # Load
    raw_df = load_data()

    # Transform
    transformed_df = transform_offers(raw_df)

    # Save
    output_path = save_data(
        transformed_df,
        PROCESSED_DATA_PATH
    )

    logger.info(
        "Pipeline completed successfully"
    )

    logger.info(
        "Output file: %s",
        output_path
    )

    return transformed_df


# =========================================================
# 18. Local Execution
# =========================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        )
    )

    run_transformation()
