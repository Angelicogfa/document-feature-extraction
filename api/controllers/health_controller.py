from fastapi.routing import APIRouter

router = APIRouter(prefix='/healthcheck')

@router.get('')
def get():
    return {'status': 'ok'}