"""Learning Profile Pydantic schemas."""
from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict


class LearningProfileBase(BaseModel):
    """Base learning profile schema."""

    knowledge_level: Optional[Dict[str, str]] = None
    learning_goals: Optional[List[str]] = None
    preferred_learning_style: Optional[Dict[str, float]] = None
    available_time_per_week: Optional[int] = None
    target_completion_date: Optional[datetime] = None
    interests: Optional[List[str]] = None
    constraints: Optional[Dict[str, Any]] = None


class LearningProfileCreate(LearningProfileBase):
    """Schema for creating a learning profile."""

    pass


class LearningProfileUpdate(BaseModel):
    """Schema for updating a learning profile."""

    knowledge_level: Optional[Dict[str, str]] = None
    learning_goals: Optional[List[str]] = None
    preferred_learning_style: Optional[Dict[str, float]] = None
    available_time_per_week: Optional[int] = None
    target_completion_date: Optional[datetime] = None
    interests: Optional[List[str]] = None
    constraints: Optional[Dict[str, Any]] = None


class LearningProfileResponse(LearningProfileBase):
    """Schema for learning profile response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    raw_analysis: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProfileGenerateRequest(BaseModel):
    """Request schema for Profile Agent to generate a profile."""

    user_input: str = Field(..., description="User's description of their learning goals and background")
    existing_profile: Optional[LearningProfileUpdate] = None


class ProfileGenerateResponse(BaseModel):
    """Response schema from Profile Agent."""

    profile: LearningProfileResponse
    raw_analysis: str
    suggestions: List[str] = []
