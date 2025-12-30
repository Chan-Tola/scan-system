import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API URLs
    API_SCAN_URL: str = "http://api-scan:8001"
    API_STAFF_URL: str = "http://api-staff-management:80"

    #Redis Configuration
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # 7 Days in seconds
    SESSION_EXPIRY: int = 604800
    
    @property
    def public_staff_verify_url(self) -> str:
        return f"{self.API_STAFF_URL}/api/internal/verify-credentials"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()