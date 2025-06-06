from typing import Dict, List

from src.agent.langgraph.main import HealthAIAgent
from src.agent.langgraph.utils import format_chat_history
from src.schemas.chat import ChatMessageResponse


def process_ai_chat_service(user_id: str, user_message: str, chat_history: List[Dict]):
    healthAIAgent = HealthAIAgent()

    chat_history = format_chat_history(message_list=chat_history)
    response = healthAIAgent.invoke(message=user_message, chat_history=chat_history)

    return ChatMessageResponse(
        input=user_message,
        response=response.get("response") or "",
        diagnosis=response.get("diagnosis") or "",
        is_emergency=response.get("is_emergency") or False,
        treatment=response.get("treatment") or "",
    )
