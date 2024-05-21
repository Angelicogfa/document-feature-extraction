from config import Config

from fastapi import FastAPI, Security
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from controllers.health_controller import router as health_router
from controllers.ingestion_controller import router as ingestion_router

config = Config()

app = FastAPI(
    title='API para ingestão de dados',
    description='API para extração de dados via arquivo',
    docs_url='/swagger',
    redoc_url='/docs',
    separate_input_output_schemas=True)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=config.APP_CORS, 
    allow_credentials=True, 
    allow_methods=['*'], 
    allow_headers=['*'])

app.include_router(router=health_router, tags=['health'])
app.include_router(router=ingestion_router, tags=['ingestion'])

if __name__ == '__main__':
    import uvicorn
    try:
        uvicorn.run(app=app, host=config.APP_HOST, port=config.APP_PORT)
    except:
        pass

