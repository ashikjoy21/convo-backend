from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class User:
    id: str
    email: str
    created_at: datetime

@dataclass
class Conversation:
    id: str
    user_id: str
    role: str
    content: str
    timestamp: datetime

@dataclass
class UserMemory:
    id: str
    user_id: str
    type: str
    information: str
    importance: float
    created_at: datetime

@dataclass
class ApiKey:
    id: str
    user_id: str
    api_key: str
    created_at: datetime
    last_used: Optional[datetime]

@dataclass
class ChatRequest:
    message: str
    user_id: str
    context: Optional[List[dict]] = None

@dataclass
class ChatResponse:
    text: str
    audio_url: Optional[str] = None
    error: Optional[str] = None 