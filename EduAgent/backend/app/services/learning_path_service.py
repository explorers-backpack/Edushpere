"""Learning Path service."""
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.learning_path import LearningPath, PathStage
from app.schemas.learning_path import LearningPathCreate, LearningPathUpdate


class LearningPathService:
    """Service for learning path business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, path_id: int) -> Optional[LearningPath]:
        """Get learning path by ID."""
        result = await self.db.execute(
            select(LearningPath)
            .options(selectinload(LearningPath.stages))
            .where(LearningPath.id == path_id)
        )
        return result.scalar_one_or_none()

    async def get_active_by_user_id(self, user_id: int) -> Optional[LearningPath]:
        """Get active learning path for user."""
        result = await self.db.execute(
            select(LearningPath)
            .options(selectinload(LearningPath.stages))
            .where(LearningPath.user_id == user_id, LearningPath.status == "active")
            .order_by(LearningPath.created_at.desc())
        )
        return result.scalar_one_or_none()

    async def get_all_by_user_id(self, user_id: int) -> List[LearningPath]:
        """Get all learning paths for user."""
        result = await self.db.execute(
            select(LearningPath)
            .options(selectinload(LearningPath.stages))
            .where(LearningPath.user_id == user_id)
            .order_by(LearningPath.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self, user_id: int, path_data: LearningPathCreate
    ) -> LearningPath:
        """Create a new learning path."""
        path = LearningPath(
            user_id=user_id,
            title=path_data.title,
            description=path_data.description,
            target_skill=path_data.target_skill,
            total_estimated_hours=path_data.total_estimated_hours,
        )
        self.db.add(path)
        await self.db.flush()
        await self.db.refresh(path)
        return path

    async def create_from_agent(
        self, user_id: int, path_data: dict, raw_plan: str
    ) -> LearningPath:
        """Create learning path from agent output."""
        # Deactivate any existing active paths
        existing = await self.get_active_by_user_id(user_id)
        if existing:
            existing.status = "paused"

        path = LearningPath(
            user_id=user_id,
            title=path_data.get("title", "Generated Learning Path"),
            description=path_data.get("description"),
            target_skill=path_data.get("target_skill"),
            total_estimated_hours=path_data.get("total_estimated_hours"),
            status="active",
            raw_plan=raw_plan,
        )
        self.db.add(path)
        await self.db.flush()

        # Create stages if provided
        stages_data = path_data.get("stages", [])
        for i, stage_data in enumerate(stages_data):
            stage = PathStage(
                learning_path_id=path.id,
                stage_order=i + 1,
                title=stage_data.get("title", f"Stage {i+1}"),
                description=stage_data.get("description"),
                objectives=stage_data.get("objectives"),
                estimated_hours=stage_data.get("estimated_hours"),
                prerequisites=stage_data.get("prerequisites"),
                content_summary=stage_data.get("content_summary"),
            )
            self.db.add(stage)

        await self.db.flush()
        await self.db.refresh(path)
        return path

    async def update(
        self, path: LearningPath, path_data: LearningPathUpdate
    ) -> LearningPath:
        """Update existing learning path."""
        update_data = path_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(path, field, value)
        await self.db.flush()
        await self.db.refresh(path)
        return path
