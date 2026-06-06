"""Assessment service."""
from typing import Optional, List
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.assessment import Assessment, AssessmentResult


class AssessmentService:
    """Service for assessment business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_assessment_by_id(self, assessment_id: int) -> Optional[Assessment]:
        """Get assessment by ID."""
        result = await self.db.execute(
            select(Assessment).where(Assessment.id == assessment_id)
        )
        return result.scalar_one_or_none()

    async def get_result_by_id(
        self, result_id: int, user_id: int
    ) -> Optional[AssessmentResult]:
        """Get assessment result by ID for specific user."""
        result = await self.db.execute(
            select(AssessmentResult).where(
                AssessmentResult.id == result_id,
                AssessmentResult.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_user_results(self, user_id: int) -> List[AssessmentResult]:
        """Get all assessment results for user."""
        result = await self.db.execute(
            select(AssessmentResult)
            .where(AssessmentResult.user_id == user_id)
            .order_by(AssessmentResult.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_result(
        self,
        user_id: int,
        assessment_id: int,
        result_data: dict,
    ) -> AssessmentResult:
        """Create assessment result."""
        assessment_result = AssessmentResult(
            user_id=user_id,
            assessment_id=assessment_id,
            answers=result_data.get("answers"),
            score=result_data.get("score"),
            percentage=result_data.get("percentage"),
            passed=result_data.get("passed"),
            feedback=result_data.get("feedback"),
            completed_at=datetime.utcnow(),
        )
        self.db.add(assessment_result)
        await self.db.flush()
        await self.db.refresh(assessment_result)
        return assessment_result
