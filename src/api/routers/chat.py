import traceback
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.api.services.chat import (
    get_diagnosis_from_symptom_service,
    process_ai_chat_service,
)
from src.core.logger import log as logger
from src.schemas.chat import (
    ChatMessage,
    ChatMessageResponse,
    SymptomResponse,
    SymptomsRequest,
)

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

        logger.error(f"Error processing chat: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/symptoms", status_code=status.HTTP_200_OK, response_model=SymptomResponse
)
async def get_diagnosis_from_symptom(symptoms: SymptomsRequest):
    try:
        diagnosis = get_diagnosis_from_symptom_service(symptoms=symptoms.symptoms)
        return diagnosis
    except Exception as e:
        logger.error(
            f"Error processing symptom request: {str(e)}\n{traceback.format_exc()}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
