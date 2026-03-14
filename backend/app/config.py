from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://medaudit:password@localhost:5432/medaudit_db"
    REDIS_URL: str = "redis://localhost:6379"

    # API Keys
    CLAUDE_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GOOGLE_VISION_API_KEY: Optional[str] = None

    # JWT
    SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Storage
    STORAGE_PATH: str = "/tmp/medaudit/uploads"

    class Config:
        env_file = ".env"


settings = Settings()
