from typing import List, Optional

from langchain_core.language_models.chat_models import (
    BaseChatModel,
)
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_groq import ChatGroq

from src.core.config import settings


class LLMProviderManager:
    def __init__(
        self,
    ):
        self.rate_limiter = (
            InMemoryRateLimiter(
                requests_per_second=0.2,
                check_every_n_seconds=0.1,
                max_bucket_size=10,
            )
            if settings.DEBUG
            else None
        )

    def get_chat_model(
        self,
        model: Optional[str] = None,
        callbacks: Optional[List] = None,
    ) -> BaseChatModel:
        return ChatGroq(
            model=settings.MODEL_DEPLOYMENT_NAME,
            temperature=0.9,
            max_retries=2,
            rate_limiter=self.rate_limiter,
            callbacks=callbacks,
        )
