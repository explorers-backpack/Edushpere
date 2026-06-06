"""Profile Agent API router."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.learning_profile import (
    ProfileGenerateRequest,
    ProfileGenerateResponse,
    LearningProfileResponse,
    LearningProfileUpdate,
)
from app.services.learning_profile_service import LearningProfileService
from app.agents.profile_agent.agent import ProfileAgent

router = APIRouter(prefix="/api/profile", tags=["profile_agent"])
agent = ProfileAgent()


@router.post("/generate", response_model=ProfileGenerateResponse)
async def generate_profile(
    request: ProfileGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a learning profile based on user input."""
    # Process through Profile Agent
    result = await agent.process({
        "user_input": request.user_input,
        "existing_profile": request.existing_profile,
    })

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    # Save to database
    service = LearningProfileService(db)
    profile = await service.create_from_agent(
        user_id=current_user.id,
        profile_data=result.data,
        raw_analysis=result.raw_output,
    )

    return ProfileGenerateResponse(
        profile=LearningProfileResponse.model_validate(profile),
        raw_analysis=result.raw_output,
        suggestions=result.metadata.get("suggestions", []),
    )


@router.get("/current", response_model=LearningProfileResponse)
async def get_current_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's learning profile."""
    service = LearningProfileService(db)
    profile = await service.get_by_user_id(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/update", response_model=LearningProfileResponse)
async def update_profile(
    profile_data: LearningProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user's learning profile."""
    service = LearningProfileService(db)
    profile = await service.update_by_user_id(current_user.id, profile_data)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
