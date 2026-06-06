"""Assessment Pydantic schemas."""
from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict


class AssessmentBase(BaseModel):
    """Base assessment schema."""

    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    path_stage_id: Optional[int] = None
    assessment_type: str = Field(..., pattern="^(quiz|exam|project|self_check)$")
    max_score: Optional[float] = None
    time_limit_minutes: Optional[int] = None


class AssessmentCreate(AssessmentBase):
    """Schema for creating an assessment."""

    questions: Optional[List[Dict[str, Any]]] = None


class AssessmentUpdate(BaseModel):
    """Schema for updating an assessment."""

    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    questions: Optional[List[Dict[str, Any]]] = None
    max_score: Optional[float] = None
    time_limit_minutes: Optional[int] = None
    is_published: Optional[bool] = None


class AssessmentResponse(AssessmentBase):
    """Schema for assessment response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int
    questions: Optional[List[Dict[str, Any]]] = None
    is_published: bool
    created_at: datetime
    updated_at: datetime


class AssessmentResultBase(BaseModel):
    """Base assessment result schema."""

    answers: Optional[Dict[str, Any]] = None
    score: Optional[float] = None
    percentage: Optional[float] = None
    passed: Optional[bool] = None
    feedback: Optional[str] = None
    time_spent_seconds: Optional[int] = None


class AssessmentResultCreate(AssessmentResultBase):
    """Schema for creating an assessment result."""

    assessment_id: int


class AssessmentResultResponse(AssessmentResultBase):
    """Schema for assessment result response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    assessment_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime


class EvaluationRequest(BaseModel):
    """Request schema for Evaluate Agent."""

    assessment_id: int
    answers: Dict[str, Any] = Field(..., description="User's answers to the assessment")


class EvaluationResponse(BaseModel):
    """Response schema from Evaluate Agent."""

    result: AssessmentResultResponse
    detailed_feedback: str
    areas_for_improvement: List[str] = []
    strengths: List[str] = []
    recommendations: List[str] = []
