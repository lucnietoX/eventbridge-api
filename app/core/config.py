"""Configuration settings for the application."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    app_name: str = "EventBridge API"

    class Config:
        """Pydantic configuration for settings."""

        env_file: str = ".env"


settings = Settings()
