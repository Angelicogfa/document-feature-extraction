from config import Config
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


class DocumentService:
    def __init__(self, config: Config):
        credential = AzureKeyCredential(config.AZURE_DOCUMENT_RECOGNIZER_API_KEY)
        self.client = DocumentAnalysisClient(config.AZURE_DOCUMENT_RECOGNIZER_URL, credential)

    def analyse_document(self, file: bytes):
        poller = self.client.begin_analyze_document('prebuilt-document', document=file)
        result = poller.result()

        content = result.content
        paragrphs = [p.content for p in result.paragraphs]

        tables: list[dict] = []
        for table in result.tables:
            headers = [header for header in table.cells if header.kind == 'columnHeader']
            values = [value for value in table.cells if value.kind == 'content']

            indices = set([value.row_index for value in values])
            rows: list[dict] = []
            for indice in indices:
                indice_values = list(filter(lambda x: x.row_index == indice, values))
                row = dict()
                for header in headers:
                    value = list(filter(lambda x: x.column_index == header.column_index, indice_values))
                    index_name = 'index' if header.content == '' and indice == 0 else header.content
                    row[index_name] = None if len(value) == 0 else value[0].content
                rows.append(row)
            tables.append(dict(row_count=table.row_count, rows=rows))
        
        keyvalue: list[dict] = [{"key": kvp.key.content, "value": kvp.value.content if kvp.value != None else None } for kvp in result.key_value_pairs],

        return (content, paragrphs, tables, keyvalue)
        
