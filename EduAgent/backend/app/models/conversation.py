"""Conversation History database model."""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ConversationHistory(Base):
    """Conversation history for Tutor Agent interactions."""

    __tablename__ = "conversation_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)

    # Agent type: tutor, profile, path, resource, evaluate
    agent_type: Mapped[str] = mapped_column(String(50), index=True)

    # Session identifier for grouping related messages
    session_id: Mapped[str] = mapped_column(String(100), index=True)

    # Role: user, assistant, system
    role: Mapped[str] = mapped_column(String(20))

    # Message content
    content: Mapped[str] = mapped_column(Text)

    # Additional metadata (e.g., tool calls, citations)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
