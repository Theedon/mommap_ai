from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.api.services.chat import process_ai_chat_service
from src.core.logger import log as logger
from src.schemas.chat import ChatMessage, ChatMessageResponse

router = APIRouter()


@router.post("/", status_code=200, response_model=ChatMessageResponse)
async def process_ai_chat(user_id: str, message: str, chat_history: List[ChatMessage]):
    try:
        user_message = message
        user_chat_history = [chat_msg.model_dump() for chat_msg in chat_history]
        logger.debug(f"chat_history: {user_chat_history} {type(user_chat_history)}")

        chatResponse = process_ai_chat_service(
            user_id=user_id, user_message=user_message, chat_history=user_chat_history
        )
        return chatResponse

    except Exception as e:
        import traceback

        logger.error(f"Error processing chat: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
