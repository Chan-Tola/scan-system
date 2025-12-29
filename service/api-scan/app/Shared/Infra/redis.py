import redis.asyncio as redis
from typing import Optional
from app.Shared.Core.config import settings
from app.Shared.Core.logging import get_logger

logger = get_logger(__name__)

_redis_client: Optional[redis.Redis] = None

async def get_redis() -> redis.Redis:
    """Get or create Redis client (singleton)"""
    global _redis_client
    
    if _redis_client is None:
        _redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
            encoding="utf-8"
        )
        logger.info("redis_connected", host=settings.REDIS_HOST)
    
    return _redis_client

async def close_redis():
    """Close Redis connection"""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("redis_disconnected")