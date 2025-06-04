from enum import Enum

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
