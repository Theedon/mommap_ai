from typing import List, Optional, TypedDict

from langchain.schema import AIMessage, HumanMessage
from langgraph.graph import END, StateGraph

from src.agent.config import LLMProviderManager
from src.agent.langgraph.prompts import (
    CHECK_EMERGENCY_PROMPT,
    COMPILE_RESULT_PROMPT,
    PARSE_SYMPTOMS_PROMPT,
    REASON_DIAGNOSIS_PROMPT,
    SUGGEST_TREATMENT_PROMPT,
)
from src.agent.langgraph.schemas import (
    EmergencyStatus,
    ExtractedSymptoms,
    FinalResponse,
    ReasonDiagnosis,
    TreatmentSuggestion,
)
from src.core.logger import log as logger


class HealthState(TypedDict):
    input: str
    symptoms: Optional[List[str]]
    diagnosis: Optional[str]
    treatment: Optional[str]
    response: Optional[str]
    is_emergency: Optional[bool]
    chat_history: List[HumanMessage | AIMessage]


class HealthAIAgent:
    def __init__(self):
        self.llm = LLMProviderManager().get_chat_model()
        self.graph = self._build_graph()

    def parse_symptoms(self, state: HealthState):
        logger.info("--------📝 Parsing Symptoms Node--------")

        logger.info(f"State: {state}")
        parse_symptoms_prompt = PARSE_SYMPTOMS_PROMPT.format(
            input=state["input"],
            chat_history=(
                state["chat_history"]
                if len(state["chat_history"]) > 0
                else "No chat history"
            ),
        )

        structured_llm = self.llm.with_structured_output(ExtractedSymptoms)

        response = structured_llm.invoke([HumanMessage(content=parse_symptoms_prompt)])
        symptoms = response.symptoms
        logger.info(f"Extracted symptoms: {symptoms}")
        return {**state, "symptoms": response.symptoms}

    def check_emergency(self, state: HealthState):
        logger.info("--------🚨 Checking Emergency Node--------")
        prompt = CHECK_EMERGENCY_PROMPT.format(
            symptoms=", ".join(state["symptoms"]),
            chat_history=(
                state["chat_history"]
                if len(state["chat_history"]) > 0
                else "No chat history"
            ),
        )
        structured_llm = self.llm.with_structured_output(EmergencyStatus)
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        is_emergency = response.is_emergency
        logger.info(f"Emergency check result: {is_emergency}")
        return {**state, "is_emergency": is_emergency}

    def handle_emergency(self, state: HealthState):
        logger.info("--------🚑 Handling Emergency Node--------")
        return {
            **state,
            "response": "⚠️ Your symptoms may indicate a medical emergency. Please seek immediate care or call emergency services now.",
        }

    def reason_diagnosis(self, state: HealthState):
        logger.info("--------🩺 Reasoning Diagnosis Node--------")
        prompt = REASON_DIAGNOSIS_PROMPT.format(
            symptoms=", ".join(state["symptoms"]),
            chat_history=(
                state["chat_history"]
                if len(state["chat_history"]) > 0
                else "No chat history"
            ),
        )
        structured_llm = self.llm.with_structured_output(ReasonDiagnosis)
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        diagnosis = response.diagnosis.strip()
        logger.info(f"Diagnosed condition: {diagnosis}")
        return {**state, "diagnosis": diagnosis}

    def suggest_treatment(self, state: HealthState):
        logger.info("--------💊 Suggesting Treatment Node--------")
        prompt = SUGGEST_TREATMENT_PROMPT.format(
            diagnosis=state["diagnosis"],
            symptoms=", ".join(state["symptoms"]),
            chat_history=(
                state["chat_history"]
                if len(state["chat_history"]) > 0
                else "No chat history"
            ),
        )
        structured_llm = self.llm.with_structured_output(TreatmentSuggestion)
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        treatment = response.treatment.strip()
        logger.info(f"Suggested treatment: {treatment}")
        return {**state, "treatment": treatment}

    def format_response(self, state: HealthState):
        logger.info("--------📋 Formatting Response Node--------")
        prompt = COMPILE_RESULT_PROMPT.format(
            diagnosis=state["diagnosis"],
            symptoms=", ".join(state["symptoms"]),
            treatment=state["treatment"],
            chat_history=(
                state["chat_history"]
                if len(state["chat_history"]) > 0
                else "No chat history"
            ),
        )
        structured_llm = self.llm.with_structured_output(FinalResponse)
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        summary = response.summary.strip()
        logger.info(f"Final response summary: {summary}")
        logger.info(f"Final state: {state}")
        return {**state, "response": summary}

    def _build_graph(self):
        workflow = StateGraph(HealthState)

        workflow.add_node("symptom_parser", self.parse_symptoms)
        workflow.add_node("emergency_check", self.check_emergency)
        workflow.add_node("emergency_response", self.handle_emergency)
        workflow.add_node("diagnosis_reasoning", self.reason_diagnosis)
        workflow.add_node("treatment_suggestion", self.suggest_treatment)
        workflow.add_node("response_formatter", self.format_response)

        # Transitions
        workflow.set_entry_point("symptom_parser")
        workflow.add_edge("symptom_parser", "emergency_check")
        workflow.add_conditional_edges(
            "emergency_check",
            lambda state: (
                "emergency_response" if state["is_emergency"] else "diagnosis_reasoning"
            ),
        )
        workflow.add_edge("emergency_response", "response_formatter")
        workflow.add_edge("diagnosis_reasoning", "treatment_suggestion")
        workflow.add_edge("treatment_suggestion", "response_formatter")
        workflow.add_edge("response_formatter", END)

        return workflow.compile()

    def invoke(self, message: str, chat_history: List) -> HealthState:
        initial_state: HealthState = {
            "input": message,
            "chat_history": chat_history,
            "symptoms": None,
            "diagnosis": None,
            "treatment": None,
            "response": None,
            "is_emergency": None,
        }
        final_state: HealthState = self.graph.invoke(initial_state)
        return final_state
