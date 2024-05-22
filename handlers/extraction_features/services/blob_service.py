from io import BytesIO
from config import Config
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings

class BlobService:
    def __init__(self, config: Config):
        self.client = BlobServiceClient.from_connection_string(config.AZURE_BLOB_CONNECTION_STRING)

    def save_blob(self, container_name: str, path_file_name: str, file: bytes, content_type: str|None = None) -> bool:
        container: ContainerClient = self.client.get_container_client(container=container_name)
        
        if not container.exists():
            container.create_container()

        blob_client: BlobClient = container.get_blob_client(blob=path_file_name)
        content: ContentSettings = None

        if content_type != None:
            content = ContentSettings(content_type=content_type)

        result = blob_client.upload_blob(file, content_settings=content)

        return result != None
    
    def get_document(self, url: str) -> bytes | None:
        blob_name = url.split('ingestion')[1][1:]

        with BytesIO() as memory_stream:
            blob: BlobClient = self.client.get_blob_client('ingestion', blob=f'{blob_name}')
            stream = blob.download_blob()
            stream.readinto(memory_stream)

            return memory_stream.getvalue()

        

