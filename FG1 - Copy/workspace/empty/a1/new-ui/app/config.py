from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Default to SQLite if no environment variable is set
    database_url: str = "sqlite:///./bank.db"
    secret_key: str = "supersecretkey"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
