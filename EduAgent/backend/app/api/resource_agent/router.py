"""Resource Agent API router."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.resource import (
    ResourceGenerateRequest,
    ResourceGenerateResponse,
    ResourceResponse,
)
from app.services.resource_service import ResourceService
from app.agents.resource_agent.agent import ResourceAgent

router = APIRouter(prefix="/api/resource", tags=["resource_agent"])
agent = ResourceAgent()


@router.post("/generate", response_model=ResourceGenerateResponse)
async def generate_resource(
    request: ResourceGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate learning resources for a specific path stage."""
    result = await agent.process({
        "path_stage_id": request.path_stage_id,
        "resource_type": request.resource_type,
        "topic": request.topic,
        "difficulty": request.difficulty,
        "count": request.count,
    })

    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    service = ResourceService(db)
    resources = await service.create_from_agent(
        creator_id=current_user.id,
        path_stage_id=request.path_stage_id,
        resources_data=result.data.get("resources", []),
        generation_metadata=result.metadata,
    )

    return ResourceGenerateResponse(
        resources=[ResourceResponse.model_validate(r) for r in resources],
        generation_notes=result.raw_output,
    )


@router.get("/list", response_model=List[ResourceResponse])
async def list_resources(
    path_stage_id: int = None,
    resource_type: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List resources with optional filters."""
    service = ResourceService(db)
    resources = await service.list_by_creator(
        creator_id=current_user.id,
        path_stage_id=path_stage_id,
        resource_type=resource_type,
    )
    return resources


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific resource by ID."""
    service = ResourceService(db)
    resource = await service.get_by_id(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource
