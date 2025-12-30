"""
Configuration settings for the Security Incident Management API.
Uses Pydantic Settings for type-safe configuration management.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Security Incident Management API"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str

    # Security - JWT
    SECRET_KEY: str  # Used to sign JWT tokens
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AWS Configuration (for S3 file uploads)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: Optional[str] = None

    # CORS (Cross-Origin Resource Sharing)
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        """Pydantic config - tells it to read from .env file"""
        env_file = ".env"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
