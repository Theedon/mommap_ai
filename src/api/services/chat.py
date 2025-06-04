import re
from typing import Any, Dict, List

from src.agent.langgraph.main import HealthAIAgent
from src.agent.langgraph.utils import format_chat_history


def process_ai_chat_service(user_id: str, user_message: str, chat_history: List[Dict]):
    healthAIAgent = HealthAIAgent()

    chat_history = format_chat_history(message_list=chat_history)
    response = healthAIAgent.invoke(message=user_message, chat_history=chat_history)

    return {
        "input": user_id,
        "response": response.get("response", ""),
        "diagnosis": response.get("diagnosis", ""),
        "is_emergency": response.get("is_emergency", False),
    }
