import traceback
from typing import Dict, List

from langchain.schema import HumanMessage

from src.agent.config import LLMProviderManager
from src.agent.langgraph.main import HealthAIAgent
from src.agent.langgraph.prompts import FIND_SYMPTOM_DIAGNOSIS_PROMPT
from src.agent.langgraph.utils import format_chat_history
from src.core.logger import log as logger
from src.schemas.chat import ChatMessageResponse, SymptomResponse


def process_ai_chat_service(user_id: str, user_message: str, chat_history: List[Dict]):
    try:
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
    except Exception as e:
        logger.error(f"Error in process_ai_chat_service: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return ChatMessageResponse(
            input=user_message,
            response="Sorry, I encountered an error processing your request.",
            diagnosis="",
            is_emergency=False,
            treatment="",
        )


def get_diagnosis_from_symptom_service(symptoms: List[str]):
    try:
        llm = LLMProviderManager().get_chat_model()

        prompt = FIND_SYMPTOM_DIAGNOSIS_PROMPT.format(symptoms=symptoms)

        structured_llm = llm.with_structured_output(SymptomResponse)
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        diagnosis = response.diagnosis.strip()
        logger.info(f"Diagnosis from symptoms: {diagnosis}")

        return SymptomResponse(diagnosis=diagnosis)

    except Exception as e:
        logger.error(f"Error in get_diagnosis_from_symptom_service: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return SymptomResponse(diagnosis="Unable to process symptoms at this time")
