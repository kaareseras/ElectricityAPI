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

    # FrontEnd Application
    FRONTEND_HOST: str = os.environ.get("FRONTEND_HOST", "http://localhost:3000")

    # Azure PostgreSQL Config
    WEBSITE_HOSTNAME: str = os.environ.get("WEBSITE_HOSTNAME", "")
    AZURE_POSTGRESQL_CONNECTIONSTRING: str = os.environ.get("AZURE_POSTGRESQL_CONNECTIONSTRING", "")

    # Postgres Database Config
    POSTGRES_USERNAME: str = os.environ.get("DBUSER", "username")
    POSTGRES_PASSWORD: str = os.environ.get("DBPASS", "password")
    POSTGRES_HOST: str = os.environ.get("DBHOST", "localhost")
    POSTGRES_DATABASE: str = os.environ.get("DBNAME", "testdb")
    POSTGRES_PORT: int = os.environ.get("DBPORT", 5432)

    DATABASE_URI: str = (
        f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    )

    # JWT Secret Key
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "649fb93ef34e4fdf4187709c84d643dd61ce730d91856418fdcf563f895ea40f")
    JWT_ALGORITHM: str = os.environ.get("ACCESS_TOKEN_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 600))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))

    # App Secret Key
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")

    # GPT Configuration
    AZURE_OPENAI_DEPLOYMENT: str = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
    AZURE_OPENAI_ENDPOINT: str = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_KEY: str = os.environ.get("AZURE_OPENAI_KEY", "")


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_app_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
