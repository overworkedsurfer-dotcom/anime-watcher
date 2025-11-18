"""Application configuration."""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Manga Release Radar"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://manga_user:manga_pass@db:5432/manga_radar"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://redis:6379"
    REDIS_CACHE_TTL: int = 3600  # 1 hour

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # External APIs
    MANGADEX_API_URL: str = "https://api.mangadex.org"
    MANGADEX_RATE_LIMIT: int = 5  # requests per second

    # Pagination
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 100

    # Cache TTLs (in seconds)
    CACHE_CURRENT_MONTH: int = 3600  # 1 hour
    CACHE_UPCOMING_MONTHS: int = 21600  # 6 hours
    CACHE_SEARCH: int = 1800  # 30 minutes
    CACHE_METADATA: int = 86400  # 24 hours

    # Background Worker
    ENABLE_WORKER: bool = True
    SYNC_CURRENT_CRON: str = "0 */6 * * *"  # Every 6 hours
    SYNC_UPCOMING_CRON: str = "0 2 * * *"  # Daily at 2 AM

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
