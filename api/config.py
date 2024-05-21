from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Application configuration
    APP_HOST: str = environ.get('APP_HOST', 'localhost')
    APP_PORT: int = int(environ.get('APP_PORT', 8080))
    APP_CORS: list[str] = str(environ.get('APP_CORS', 'http://localhost:8080;')).split(';')

    AZURE_BLOB_CONNECTION_STRING: str = environ.get('AZURE_BLOB_CONNECTION_STRING')