from fastapi import FastAPI

from src.api import api
from src.core.config import settings
from src.core.logger import log as logger

app = FastAPI(title="Mommap AI Microservice")

app.include_router(api.api_router, prefix=f"/api/{settings.API_VERSION}")
