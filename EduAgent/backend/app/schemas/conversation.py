"""Conversation History Pydantic schemas."""
from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict


class ConversationHistoryBase(BaseModel):
    """Base conversation history schema."""

    agent_type: str = Field(..., pattern="^(tutor|profile|path|resource|evaluate)$")
    session_id: str = Field(..., max_length=100)
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    metadata: Optional[Dict[str, Any]] = None


class ConversationHistoryCreate(ConversationHistoryBase):
    """Schema for creating a conversation history entry."""

    pass


class ConversationHistoryResponse(ConversationHistoryBase):
    """Schema for conversation history response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime


class ChatMessage(BaseModel):
    """Schema for a single chat message."""

    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class ChatRequest(BaseModel):
    """Request schema for Tutor Agent chat."""

    session_id: str = Field(..., max_length=100)
    message: str = Field(..., description="User's message")
    context: Optional[Dict[str, Any]] = Field(
        None, description="Additional context like current learning path, stage, etc."
    )


class ChatResponse(BaseModel):
    """Response schema from Tutor Agent."""

    response: str
    session_id: str
    suggestions: list[str] = []
    conversation_history: list[ChatMessage] = []
