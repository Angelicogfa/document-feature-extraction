from uuid import uuid4
from config import Config
from fastapi.routing import APIRouter
from fastapi import UploadFile, status
from services.blob_service import BlobService
from fastapi.responses import JSONResponse, Response

router = APIRouter(prefix='/ingestion')
config = Config()
blob_service = BlobService(config)

@router.post('', status_code=status.HTTP_201_CREATED)
async def post(file: UploadFile):
    key = str(uuid4())
    path_name = f'input/{key}/{file.filename.replace(" ", "")}'
    
    buffer_file = await file.read()
    result = blob_service.save_blob('ingestion', path_name, buffer_file)

    status_code = status.HTTP_201_CREATED
    message = 'Salvo com sucesso'

    if not result:
        status_code = status.HTTP_400_BAD_REQUEST
        message = 'Não foi possível salvar o arquivo'
        key = None

    return JSONResponse(dict(message=message, key=key), status_code=status_code)

@router.get('/{key}:status', status_code=status.HTTP_200_OK)
async def get_status(key: str):
    path_name = f'output/{key}'
    result = blob_service.check_status('ingestion', path_name)

    if result is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    elif result is False:
        return JSONResponse(dict(message='Em processamento'))
    else:
        return JSONResponse(dict(message='Processamento finalizado'))