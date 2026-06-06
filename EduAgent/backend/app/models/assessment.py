"""Assessment database model."""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Integer, ForeignKey, JSON, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Assessment(Base):
    """Assessment model for evaluating learning progress."""

    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    creator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), index=True
    )

    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Associated path stage
    path_stage_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("path_stages.id"), nullable=True, index=True
    )

    # Assessment type: quiz, exam, project, self_check
    assessment_type: Mapped[str] = mapped_column(String(50))

    # Questions as JSON array
    questions: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    # Maximum score
    max_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Time limit in minutes
    time_limit_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    is_published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class AssessmentResult(Base):
    """Assessment result model for storing user assessment attempts."""

    __tablename__ = "assessment_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    assessment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("assessments.id"), index=True
    )

    # User's answers
    answers: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Score achieved
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Percentage score
    percentage: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Pass/Fail status
    passed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # Feedback from Evaluate Agent
    feedback: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)

    # Time spent in seconds
    time_spent_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="assessment_results")
    assessment = relationship("Assessment")
