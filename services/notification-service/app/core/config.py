"""
Notification Service configuration.
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Service
    SERVICE_NAME: str = "notification-service"
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", 8006))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://shopzy:shopzy@localhost/notification_db")
    DATABASE_POOL_SIZE: int = 20
    DATABASE_POOL_MAX_OVERFLOW: int = 10
    AUTO_MIGRATE: bool = os.getenv("AUTO_MIGRATE", "true").lower() == "true"

    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # RabbitMQ
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

    # Notification settings
    NOTIFICATION_LOG_ONLY: bool = os.getenv("NOTIFICATION_LOG_ONLY", "true").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
