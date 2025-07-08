import logging
import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.fastapi_app.config.config import get_settings

settings = get_settings()

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

required_env_vars = [
    "POSTGRES_USERNAME",
    "POSTGRES_PASSWORD",
    "POSTGRES_HOST",
    "POSTGRES_DATABASE",
    "POSTGRES_PORT",
]

missing_env_vars = [var for var in required_env_vars if not hasattr(settings, var)]

if missing_env_vars:
    logger.error(f"Cant connet to DB: Missing required environment variables: {', '.join(missing_env_vars)}")

POSTGRES_USERNAME = settings.POSTGRES_USERNAME
POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
POSTGRES_HOST = settings.POSTGRES_HOST
POSTGRES_DATABASE = settings.POSTGRES_DATABASE
POSTGRES_PORT = settings.POSTGRES_PORT

sql_url = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

# Create the SQLAlchemy engine with optimized pool settings
# Adjust pool size based on environment
is_development = os.environ.get("DEBUG", "False").lower() == "true"
pool_size = 2 if is_development else 5  # Smaller pool for development
max_overflow = 3 if is_development else 10

engine = create_engine(
    sql_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=pool_size,
    max_overflow=max_overflow,
    connect_args={
        "connect_timeout": 10,  # 10 second connection timeout
        "application_name": "fastapi_app",
    },
    echo=is_development,  # Log SQL queries in development
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
