from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    PROJECT_NAME: str = "Parusresort"

    APP_HOST: str = Field(
        default="0.0.0.0",
        description="Host to bind to. Use '0.0.0.0' only in Docker containers.",
    )

    APP_PORT: int = Field(
        default=8000,
        ge=1024,  # Не используем привилегированные порты (<1024)
        le=65535,
        description="Port to bind to (1024-65535)",
    )

    APP_RELOAD: bool = Field(
        default=True, description="Enable auto-reload. Should be False in production."
    )

    BASE_DIR: str = Field(
        default_factory=lambda: str(Path(__file__).resolve().parent.parent),
        description="Base directory of the project",
    )

    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    LOGGING_FILE_MAX_BYTES: int = Field(
        default=500_000,
        ge=100_000,
        le=10_000_000,
        description="Maximum size of log file in bytes before rotation",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # env_prefix="SHOP_BOT_",
    )


settings = Settings()
