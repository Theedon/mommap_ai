import os

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from src.api import api
from src.core.config import settings
from src.core.logger import log as logger

app = FastAPI(title="Mommap AI Microservice")


@app.get("/")
async def welcome():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(current_dir, "templates/index.html")
    return FileResponse(html_file_path)


app.include_router(api.api_router, prefix=f"/api/{settings.API_VERSION}")
