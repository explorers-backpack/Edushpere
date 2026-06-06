"""Learning Profile database model."""
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, DateTime, Integer, ForeignKey, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LearningProfile(Base):
    """Learning profile model storing user preferences and characteristics."""

    __tablename__ = "learning_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), unique=True, index=True
    )

    # Profile data stored as JSON for flexibility
    knowledge_level: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    """e.g. {"math": "beginner", "programming": "intermediate"}"""

    learning_goals: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    """e.g. ["Learn Python", "Master Machine Learning"]"""

    preferred_learning_style: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    """e.g. {"visual": 0.8, "auditory": 0.5, "reading": 0.7}"""

    available_time_per_week: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    """Hours per week available for learning"""

    target_completion_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )

    interests: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    """Topics the user is interested in"""

    constraints: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    """Any constraints like budget, equipment, etc."""

    raw_analysis: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    """Raw output from Profile Agent for reference"""

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user = relationship("User", back_populates="learning_profile")
