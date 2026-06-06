"""Path Agent API router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.learning_path import (
    PathGenerateRequest,
    PathGenerateResponse,
    LearningPathResponse,
)
from app.services.learning_path_service import LearningPathService
from app.agents.path_agent.agent import PathAgent

router = APIRouter(prefix="/api/path", tags=["path_agent"])
agent = PathAgent()


@router.post("/generate", response_model=PathGenerateResponse)
async def generate_path(
    request: PathGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a learning path based on user profile and goals."""
    result = await agent.process({
        "target_skill": request.target_skill,
        "current_knowledge": request.current_knowledge,
        "time_available": request.time_available,
        "goals": request.goals,
        "constraints": request.constraints,
    })

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    service = LearningPathService(db)
    path = await service.create_from_agent(
        user_id=current_user.id,
        path_data=result.data,
        raw_plan=result.raw_output,
    )

    return PathGenerateResponse(
        learning_path=LearningPathResponse.model_validate(path),
        raw_plan=result.raw_output,
        recommendations=result.metadata.get("recommendations", []),
    )


@router.get("/current", response_model=LearningPathResponse)
async def get_current_path(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's active learning path."""
    service = LearningPathService(db)
    path = await service.get_active_by_user_id(current_user.id)
    if not path:
        raise HTTPException(status_code=404, detail="No active learning path found")
    return path


@router.get("/", response_model=list[LearningPathResponse])
async def list_paths(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all learning paths for current user."""
    service = LearningPathService(db)
    paths = await service.get_all_by_user_id(current_user.id)
    return paths
