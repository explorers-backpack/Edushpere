"""Redis client for caching and session management."""
from typing import Optional

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

# Global redis client
_redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """Get or create Redis client."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            decode_responses=True,
        )
    return _redis_client


async def close_redis() -> None:
    """Close Redis connection."""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


class CacheService:
    """Redis cache service."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        return await self.redis.get(key)

    async def set(
        self, key: str, value: str, expire: Optional[int] = None
    ) -> None:
        """Set value to cache with optional expiration in seconds."""
        if expire:
            await self.redis.setex(key, expire, value)
        else:
            await self.redis.set(key, value)

    async def delete(self, key: str) -> None:
        """Delete key from cache."""
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        return await self.redis.exists(key) > 0

    # Learning path cache keys
    @staticmethod
    def learning_path_key(user_id: int) -> str:
        return f"learning_path:user:{user_id}"

    # User session cache keys
    @staticmethod
    def user_session_key(user_id: int) -> str:
        return f"user:session:{user_id}"

    # Agent conversation cache keys
    @staticmethod
    def agent_conv_key(user_id: int, agent_type: str) -> str:
        return f"agent:conv:{user_id}:{agent_type}"


async def get_cache_service() -> CacheService:
    """Dependency for getting cache service."""
    redis_client = await get_redis()
    return CacheService(redis_client)
