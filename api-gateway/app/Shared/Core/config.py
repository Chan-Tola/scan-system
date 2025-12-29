from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API URLs
    API_SCAN_URL: str = "http://api-scan:8001"
    API_STAFF_URL: str = "http://api-staff-management:80"

    #Redis Configuration
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()