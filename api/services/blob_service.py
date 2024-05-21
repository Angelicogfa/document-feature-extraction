from config import Config
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

class BlobService:
    def __init__(self, config: Config):
        self.client = BlobServiceClient.from_connection_string(config.AZURE_BLOB_CONNECTION_STRING)

    def save_blob(self, container_name: str, path_file_name: str, file: bytes) -> bool:
        container: ContainerClient = self.client.get_container_client(container=container_name)
        
        if not container.exists():
            container.create_container()

        blob_client: BlobClient = container.get_blob_client(blob=path_file_name)
        result = blob_client.upload_blob(file)

        return result != None
    
    def check_status(self, container_name: str, folder_name: str) -> bool:
        container: ContainerClient = self.client.get_container_client(container=container_name)
        
        if not container.exists():
            container.create_container()

        blob = container.get_blob_client(folder_name)
        if blob is None:
            return None
        
        blobs = [blob for blob in container.list_blobs(name_starts_with=folder_name)]
        return True if len(blobs) > 1 else False
        

