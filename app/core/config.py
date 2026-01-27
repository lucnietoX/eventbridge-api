from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "EventBridge API"

    class Config:
        env_file: str = ".env"


settings = Settings()
