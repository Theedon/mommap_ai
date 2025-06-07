from enum import Enum
from typing import List

from pydantic import BaseModel


class Role(str, Enum):
    human = "human"
    agent = "agent"


class ChatMessage(BaseModel):
    message_id: str
    user_id: str
    message: str
    identifier: Role
    timestamp: str
    created_at: str


class ChatMessageResponse(BaseModel):
    input: str
    response: str
    diagnosis: str
    is_emergency: bool = False
    treatment: str

    class Config:
        orm_mode = True


class SymptomsRequest(BaseModel):
    symptoms: List[str]


class SymptomResponse(BaseModel):
    diagnosis: str
