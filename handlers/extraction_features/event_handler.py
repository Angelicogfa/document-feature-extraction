import json as j
from config import Config
from services.blob_service import BlobService
from services.document_service import DocumentService


class EventHandler:
    def __init__(self, config: Config):
        self.blob_service = BlobService(config)
        self.document_service = DocumentService(config)

    def handler_event(self, event: dict) -> bool:
        event_data = event['data']
        file_url: str = event_data['url']

        try:
            directory = file_url.split('input')[1].split('/')[1]
            buffer = self.blob_service.get_document(file_url)
            (content, paragrphs, tables, kv) = self.document_service.analyse_document(buffer)

            container = 'ingestion'
            directory = f'output/{directory}'

            self.blob_service.save_blob(container, f'{directory}/{file_url.split("/")[-1]}', buffer)

            if content != None and len(content) > 0:
                self.blob_service.save_blob(container, f'{directory}/content.txt', content.encode(), 'application/text')
            if paragrphs != None and len(paragrphs) > 0:
                self.blob_service.save_blob(container, f'{directory}/paragrphs.json', j.dumps(paragrphs).encode(), 'application/json')
            if tables != None and len(tables) > 0:
                self.blob_service.save_blob(container, f'{directory}/tables.json', j.dumps(tables).encode(), 'application/json')
            if kv != None and len(kv) > 0:
                self.blob_service.save_blob(container, f'{directory}/kv.json', j.dumps(kv).encode(), 'application/json')

            return True
        except:
            return False