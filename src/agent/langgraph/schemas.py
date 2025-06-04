from typing import List

from pydantic import BaseModel, Field


class ExtractedSymptoms(BaseModel):
    symptoms: List[str] = Field(
        ..., description="List of symptoms extracted from the input text."
    )


class EmergencyStatus(BaseModel):
    is_emergency: bool = Field(
        ..., description="Indicates if the symptoms suggest a medical emergency."
    )


class ReasonDiagnosis(BaseModel):
    diagnosis: str = Field(
        ..., description="A possible diagnosis based on the symptoms provided."
    )


class TreatmentSuggestion(BaseModel):
    treatment: str = Field(
        ...,
        description="Suggested treatment or advice based on the diagnosis and symptoms.",
    )


class FinalResponse(BaseModel):
    summary: str = Field(..., description="Comprehensive response to objective")
