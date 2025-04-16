import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # App
    APP_NAME: str = os.environ.get("APP_NAME", "FastAPI")
    DEBUG: bool = bool(os.environ.get("DEBUG", False))

    # Azure PostgreSQL Config
    WEBSITE_HOSTNAME: str = os.environ.get("WEBSITE_HOSTNAME", "")
    AZURE_POSTGRESQL_CONNECTIONSTRING: str = os.environ.get("AZURE_POSTGRESQL_CONNECTIONSTRING", "")

    # Postgres Database Config
    POSTGRES_USERNAME: str = os.environ.get("DBUSER")
    POSTGRES_PASSWORD: str = os.environ.get("DBPASS")
    POSTGRES_HOST: str = os.environ.get("DBHOST")
    POSTGRES_DATABASE: str = os.environ.get("DBNAME")
    POSTGRES_PORT: int = os.environ.get("DBPORT", 5432)

    DATABASE_URI: str = (
        f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
