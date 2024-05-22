from io import BytesIO
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
    
    def get_items(self, container_name: str, folder_name: str) -> list:
        container: ContainerClient = self.client.get_container_client(container=container_name)
        
        if not container.exists():
            container.create_container()

        blobs = [blob.name.split('/')[-1] for blob in container.list_blobs(name_starts_with=folder_name)]
        return blobs
    
    def get_item(self, container_name: str, file_name):
        container: ContainerClient = self.client.get_container_client(container=container_name)
        
        if not container.exists():
            container.create_container()

        try:
            blob: BlobClient = self.client.get_blob_client('ingestion', blob=file_name)
            properties = blob.get_blob_properties()

            with BytesIO() as memory_stream:
                
                stream = blob.download_blob()
                stream.readinto(memory_stream)
                return memory_stream.getvalue(), properties.content_settings.content_type
        except:
            return None
        

