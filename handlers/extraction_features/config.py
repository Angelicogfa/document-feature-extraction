from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    AZURE_SERVICE_BUS_CONNECTION_STRING: str = environ.get('AZURE_SERVICE_BUS_CONNECTION_STRING')
    AZURE_SERVICE_BUS_QUEUE_NAME: str = environ.get('AZURE_SERVICE_BUS_QUEUE_NAME')
    AZURE_DOCUMENT_RECOGNIZER_URL: str = environ.get('AZURE_DOCUMENT_RECOGNIZER_URL')
    AZURE_DOCUMENT_RECOGNIZER_API_KEY: str = environ.get('AZURE_DOCUMENT_RECOGNIZER_API_KEY')
    AZURE_BLOB_CONNECTION_STRING: str = environ.get('AZURE_BLOB_CONNECTION_STRING')