"""Conversation service."""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import ConversationHistory


class ConversationService:
    """Service for conversation history management."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_history(
        self,
        user_id: int,
        agent_type: str,
        session_id: str,
        limit: int = 50,
    ) -> List[ConversationHistory]:
        """Get conversation history for a session."""
        result = await self.db.execute(
            select(ConversationHistory)
            .where(
                ConversationHistory.user_id == user_id,
                ConversationHistory.agent_type == agent_type,
                ConversationHistory.session_id == session_id,
            )
            .order_by(ConversationHistory.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def add_message(
        self,
        user_id: int,
        agent_type: str,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> ConversationHistory:
        """Add a message to conversation history."""
        message = ConversationHistory(
            user_id=user_id,
            agent_type=agent_type,
            session_id=session_id,
            role=role,
            content=content,
            metadata=metadata,
        )
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)
        return message

    async def clear_history(
        self,
        user_id: int,
        agent_type: str,
        session_id: str,
    ) -> None:
        """Clear conversation history for a session."""
        result = await self.db.execute(
            select(ConversationHistory).where(
                ConversationHistory.user_id == user_id,
                ConversationHistory.agent_type == agent_type,
                ConversationHistory.session_id == session_id,
            )
        )
        messages = result.scalars().all()
        for msg in messages:
            await self.db.delete(msg)
        await self.db.flush()
