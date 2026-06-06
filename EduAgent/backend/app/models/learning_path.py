"""Learning Path database model."""
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, DateTime, Integer, ForeignKey, JSON, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PathStage(Base):
    """Individual stage within a learning path."""

    __tablename__ = "path_stages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    learning_path_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("learning_paths.id"), index=True
    )

    stage_order: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Learning objectives for this stage
    objectives: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)

    # Estimated duration in hours
    estimated_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Prerequisite stage IDs
    prerequisites: Mapped[Optional[List[int]]] = mapped_column(JSON, nullable=True)

    # Stage content summary from Path Agent
    content_summary: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class LearningPath(Base):
    """Learning path model defining a structured learning journey."""

    __tablename__ = "learning_paths"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)

    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Target skill or certification
    target_skill: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Total estimated hours
    total_estimated_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Current progress (0-100)
    progress: Mapped[float] = mapped_column(Float, default=0.0)

    # Status: draft, active, paused, completed
    status: Mapped[str] = mapped_column(String(20), default="draft")

    # Raw output from Path Agent
    raw_plan: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    user = relationship("User", back_populates="learning_paths")
    stages = relationship(
        "PathStage",
        back_populates="learning_path",
        order_by="PathStage.stage_order",
        cascade="all, delete-orphan",
    )
