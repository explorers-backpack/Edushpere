"""Learning Resource database model."""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, Integer, ForeignKey, JSON, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Resource(Base):
    """Learning resource model for educational materials."""

    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    creator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), index=True
    )

    # Resource metadata
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Resource type: video, article, exercise, quiz, project
    resource_type: Mapped[str] = mapped_column(String(50))

    # Content format: markdown, html, video_url, interactive
    content_format: Mapped[str] = mapped_column(String(50))

    # The actual content or URL
    content: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)

    # Associated learning path stage
    path_stage_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("path_stages.id"), nullable=True, index=True
    )

    # Tags for categorization
    tags: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)

    # Difficulty level: beginner, intermediate, advanced
    difficulty_level: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )

    # Estimated time to complete (minutes)
    estimated_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Quality score from Resource Agent
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Metadata from Resource Agent
    generation_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    is_published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    creator = relationship("User", back_populates="resources")
    path_stage = relationship("PathStage", back_populates="resources")
