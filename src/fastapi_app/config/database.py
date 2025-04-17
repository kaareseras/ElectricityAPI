import logging
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

# Create the SQLAlchemy engine
engine = create_engine(sql_url, pool_pre_ping=True, pool_recycle=3600, pool_size=20, max_overflow=0)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
