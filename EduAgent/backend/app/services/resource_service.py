"""Resource service."""
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate


class ResourceService:
    """Service for learning resource business logic."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, resource_id: int) -> Optional[Resource]:
        """Get resource by ID."""
        result = await self.db.execute(
            select(Resource).where(Resource.id == resource_id)
        )
        return result.scalar_one_or_none()

    async def list_by_creator(
        self,
        creator_id: int,
        path_stage_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Resource]:
        """List resources by creator with optional filters."""
        query = select(Resource).where(Resource.creator_id == creator_id)
        if path_stage_id:
            query = query.where(Resource.path_stage_id == path_stage_id)
        if resource_type:
            query = query.where(Resource.resource_type == resource_type)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(
        self, creator_id: int, resource_data: ResourceCreate
    ) -> Resource:
        """Create a new resource."""
        resource = Resource(
            creator_id=creator_id,
            title=resource_data.title,
            description=resource_data.description,
            resource_type=resource_data.resource_type,
            content_format=resource_data.content_format,
            content=resource_data.content,
            path_stage_id=resource_data.path_stage_id,
            tags=resource_data.tags,
            difficulty_level=resource_data.difficulty_level,
            estimated_minutes=resource_data.estimated_minutes,
        )
        self.db.add(resource)
        await self.db.flush()
        await self.db.refresh(resource)
        return resource

    async def create_from_agent(
        self,
        creator_id: int,
        path_stage_id: int,
        resources_data: List[dict],
        generation_metadata: dict,
    ) -> List[Resource]:
        """Create resources from agent output."""
        resources = []
        for data in resources_data:
            resource = Resource(
                creator_id=creator_id,
                path_stage_id=path_stage_id,
                title=data.get("title", "Generated Resource"),
                description=data.get("description"),
                resource_type=data.get("resource_type", "article"),
                content_format=data.get("content_format", "markdown"),
                content=data.get("content"),
                tags=data.get("tags", []),
                difficulty_level=data.get("difficulty_level"),
                estimated_minutes=data.get("estimated_minutes"),
                quality_score=data.get("quality_score"),
                generation_metadata=generation_metadata,
                is_published=True,
            )
            self.db.add(resource)
            resources.append(resource)
        await self.db.flush()
        for r in resources:
            await self.db.refresh(r)
        return resources

    async def update(
        self, resource: Resource, resource_data: ResourceUpdate
    ) -> Resource:
        """Update existing resource."""
        update_data = resource_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(resource, field, value)
        await self.db.flush()
        await self.db.refresh(resource)
        return resource
