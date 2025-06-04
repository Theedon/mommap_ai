from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    ENV: Literal["development", "staging", "production"] = "development"
    GROQ_API_KEY: str = ""
    MODEL_DEPLOYMENT_NAME: str = "llama-3.1-8b-instant"
    DEBUG: bool = True
    API_VERSION: str = "v1"

    model_config = SettingsConfigDict(
        env_file="./.env",
    )


settings = Settings()
