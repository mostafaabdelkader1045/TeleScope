from os import getenv

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv


load_dotenv()

CONNECTION_STRING = getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = getenv("AZURE_CONTAINER_NAME")


def get_container_client():
    """Create and return an Azure Blob container client."""

    if not CONNECTION_STRING:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING is missing.")

    if not CONTAINER_NAME:
        raise ValueError("AZURE_CONTAINER_NAME is missing.")

    blob_service = BlobServiceClient.from_connection_string(
        CONNECTION_STRING
    )

    return blob_service.get_container_client(CONTAINER_NAME)


def download_blob(blob_name: str) -> bytes:
    """Download a blob and return its content as bytes."""

    container_client = get_container_client()

    blob_client = container_client.get_blob_client(blob_name)

    return blob_client.download_blob().readall()