from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Severice info
    SERVICE_NAME: str = "API Scan Service"
    API_VERSION: str  = "v1"
    DEBUG: bool = False

    # Database infor
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "attendance_db"
    POSTGRES_USER: str = "useradmin"
    POSTGRES_PASSWORD: str = "useradminpassword"

    # Redis information
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_CACHE_EXPIRE: int = 300 # 5 minutes

    # External APIs
    # STAFF_API_URL: str = "http://nginx-laravel:8002/api"
    STAFF_API_URL: str = "http://localhost:8002/api" 
    
    # Security
    # SECRET_KEY: str = "your-secret-key-change-in-production"
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    
    # Geofencing
    # OFFICE_RADIUS_METERS: float = 100.0

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
