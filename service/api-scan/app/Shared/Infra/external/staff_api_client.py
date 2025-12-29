import httpx
from typing import Optional, Dict, Any
from app.Shared.Core.config import settings
from app.Shared.Core.logging import get_logger

logger = get_logger(__name__)

class StaffAPIClient:
    """Client to communicate with Laravel Staff Management API"""
    
    def __init__(self):
        self.base_url = settings.STAFF_API_URL
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)
    
    async def get_user_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user information from Staff API"""
        try:
            response = await self.client.get(f"/users/{user_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error("staff_api_error", user_id=user_id, error=str(e))
            return None
    
    async def verify_user_permissions(self, user_id: int, permission: str) -> bool:
        """Check if user has specific permission (Spatie)"""
        try:
            response = await self.client.get(
                f"/users/{user_id}/permissions",
                params={"permission": permission}
            )
            response.raise_for_status()
            return response.json().get("has_permission", False)
        except httpx.HTTPError:
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

# Singleton instance
staff_api_client = StaffAPIClient()