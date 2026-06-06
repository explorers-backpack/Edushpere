"""Learning Profile service."""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning_profile import LearningProfile
from app.schemas.learning_profile import (
    LearningProfileCreate,
    LearningProfileUpdate,
)


class LearningProfileService:
    """Service for learning profile business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: int) -> Optional[LearningProfile]:
        """Get learning profile by user ID."""
        result = await self.db.execute(
            select(LearningProfile).where(LearningProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self, user_id: int, profile_data: LearningProfileCreate
    ) -> LearningProfile:
        """Create a new learning profile."""
        profile = LearningProfile(
            user_id=user_id,
            knowledge_level=profile_data.knowledge_level,
            learning_goals=profile_data.learning_goals,
            preferred_learning_style=profile_data.preferred_learning_style,
            available_time_per_week=profile_data.available_time_per_week,
            target_completion_date=profile_data.target_completion_date,
            interests=profile_data.interests,
            constraints=profile_data.constraints,
        )
        self.db.add(profile)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile

    async def create_from_agent(
        self, user_id: int, profile_data: dict, raw_analysis: str
    ) -> LearningProfile:
        """Create profile from agent output."""
        existing = await self.get_by_user_id(user_id)
        if existing:
            # Update existing
            for key, value in profile_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.raw_analysis = raw_analysis
            await self.db.flush()
            await self.db.refresh(existing)
            return existing

        profile = LearningProfile(
            user_id=user_id,
            raw_analysis=raw_analysis,
            **{k: v for k, v in profile_data.items() if k != "raw_analysis"},
        )
        self.db.add(profile)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile

    async def update(
        self, profile: LearningProfile, profile_data: LearningProfileUpdate
    ) -> LearningProfile:
        """Update existing profile."""
        update_data = profile_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
        await self.db.flush()
        await self.db.refresh(profile)
        return profile

    async def update_by_user_id(
        self, user_id: int, profile_data: LearningProfileUpdate
    ) -> Optional[LearningProfile]:
        """Update profile by user ID."""
        profile = await self.get_by_user_id(user_id)
        if not profile:
            return None
        return await self.update(profile, profile_data)
