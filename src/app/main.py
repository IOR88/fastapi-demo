import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app import settings


logger = logging.getLogger(__name__)

ROOT_PATH = settings.ROOT_PATH

app = FastAPI(docs_url=f'/{ROOT_PATH}/docs',
              openapi_url=f"/{ROOT_PATH}/openapi.json")

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(f'/{ROOT_PATH}/v1/ping')
def read_root():
    return {'ping': True}
