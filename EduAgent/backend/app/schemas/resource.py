"""Resource Pydantic schemas."""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class ResourceBase(BaseModel):
    """Base resource schema."""

    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    resource_type: str = Field(..., pattern="^(video|article|exercise|quiz|project)$")
    content_format: str = Field(..., pattern="^(markdown|html|video_url|interactive)$")
    path_stage_id: Optional[int] = None
    tags: Optional[List[str]] = None
    difficulty_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    estimated_minutes: Optional[int] = None


class ResourceCreate(ResourceBase):
    """Schema for creating a resource."""

    content: Optional[str] = None


class ResourceUpdate(BaseModel):
    """Schema for updating a resource."""

    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    resource_type: Optional[str] = Field(None, pattern="^(video|article|exercise|quiz|project)$")
    content_format: Optional[str] = Field(None, pattern="^(markdown|html|video_url|interactive)$")
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    estimated_minutes: Optional[int] = None
    is_published: Optional[bool] = None


class ResourceResponse(ResourceBase):
    """Schema for resource response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int
    quality_score: Optional[float] = None
    generation_metadata: Optional[dict] = None
    is_published: bool
    created_at: datetime
    updated_at: datetime


class ResourceGenerateRequest(BaseModel):
    """Request schema for Resource Agent to generate resources."""

    path_stage_id: int
    resource_type: str = Field(..., pattern="^(video|article|exercise|quiz|project)$")
    topic: str = Field(..., description="Topic for the resource")
    difficulty: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    count: int = Field(1, ge=1, le=10, description="Number of resources to generate")


class ResourceGenerateResponse(BaseModel):
    """Response schema from Resource Agent."""

    resources: List[ResourceResponse]
    generation_notes: str
