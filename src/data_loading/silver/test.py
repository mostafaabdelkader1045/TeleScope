from src.data_loading.connections.azure_connection import get_container_client

container_client = get_container_client()

for blob in container_client.list_blobs(name_starts_with="silver/"):
    print(blob.name)