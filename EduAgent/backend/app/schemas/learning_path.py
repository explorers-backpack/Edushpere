"""Learning Path Pydantic schemas."""
from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict


class PathStageBase(BaseModel):
    """Base path stage schema."""

    stage_order: int
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    objectives: Optional[List[str]] = None
    estimated_hours: Optional[float] = None
    prerequisites: Optional[List[int]] = None
    content_summary: Optional[str] = None


class PathStageCreate(PathStageBase):
    """Schema for creating a path stage."""

    learning_path_id: int


class PathStageUpdate(BaseModel):
    """Schema for updating a path stage."""

    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    objectives: Optional[List[str]] = None
    estimated_hours: Optional[float] = None
    prerequisites: Optional[List[int]] = None
    content_summary: Optional[str] = None


class PathStageResponse(PathStageBase):
    """Schema for path stage response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    learning_path_id: int
    created_at: datetime
    updated_at: datetime


class LearningPathBase(BaseModel):
    """Base learning path schema."""

    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    target_skill: Optional[str] = Field(None, max_length=200)
    total_estimated_hours: Optional[float] = None


class LearningPathCreate(LearningPathBase):
    """Schema for creating a learning path."""

    pass


class LearningPathUpdate(BaseModel):
    """Schema for updating a learning path."""

    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    target_skill: Optional[str] = Field(None, max_length=200)
    total_estimated_hours: Optional[float] = None
    progress: Optional[float] = Field(None, ge=0, le=100)
    status: Optional[str] = Field(None, pattern="^(draft|active|paused|completed)$")


class LearningPathResponse(LearningPathBase):
    """Schema for learning path response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    progress: float
    status: str
    raw_plan: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    stages: List[PathStageResponse] = []


class PathGenerateRequest(BaseModel):
    """Request schema for Path Agent to generate a learning path."""

    target_skill: str = Field(..., description="The skill to learn")
    current_knowledge: Dict[str, str] = Field(..., description="Current knowledge levels")
    time_available: int = Field(..., description="Hours per week available")
    goals: List[str] = Field(..., description="Learning goals")
    constraints: Optional[Dict[str, Any]] = None


class PathGenerateResponse(BaseModel):
    """Response schema from Path Agent."""

    learning_path: LearningPathResponse
    raw_plan: str
    recommendations: List[str] = []
