"""Tutor Agent API router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.conversation import (
    ChatRequest,
    ChatResponse,
    ChatMessage,
)
from app.services.conversation_service import ConversationService
from app.agents.tutor_agent.agent import TutorAgent

router = APIRouter(prefix="/api/tutor", tags=["tutor_agent"])
agent = TutorAgent()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Send a message to the tutor."""
    conversation_service = ConversationService(db)

    # Get conversation history
    history = await conversation_service.get_history(
        user_id=current_user.id,
        agent_type="tutor",
        session_id=request.session_id,
    )

    # Process through Tutor Agent
    result = await agent.process({
        "message": request.message,
        "session_id": request.session_id,
        "context": request.context,
        "history": history,
    })

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    # Save user message
    await conversation_service.add_message(
        user_id=current_user.id,
        agent_type="tutor",
        session_id=request.session_id,
        role="user",
        content=request.message,
    )

    # Save assistant response
    await conversation_service.add_message(
        user_id=current_user.id,
        agent_type="tutor",
        session_id=request.session_id,
        role="assistant",
        content=result.data.get("response", ""),
    )

    # Get updated history
    updated_history = await conversation_service.get_history(
        user_id=current_user.id,
        agent_type="tutor",
        session_id=request.session_id,
    )

    return ChatResponse(
        response=result.data.get("response", ""),
        session_id=request.session_id,
        suggestions=result.data.get("suggestions", []),
        conversation_history=[
            ChatMessage(role=msg.role, content=msg.content)
            for msg in updated_history[-10:]  # Last 10 messages
        ],
    )


@router.get("/history", response_model=list[ChatMessage])
async def get_chat_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get chat history for a session."""
    service = ConversationService(db)
    messages = await service.get_history(
        user_id=current_user.id,
        agent_type="tutor",
        session_id=session_id,
    )
    return [ChatMessage(role=msg.role, content=msg.content) for msg in messages]
