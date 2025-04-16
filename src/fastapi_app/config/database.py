import logging
from collections.abc import Generator
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlmodel import SQLModel

from src.fastapi_app.config.config import get_settings

settings = get_settings()

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

sql_url = ""
if settings.WEBSITE_HOSTNAME:
    logger.info("Connecting to Azure PostgreSQL Flexible server based on AZURE_POSTGRESQL_CONNECTIONSTRING...")
    env_connection_string = settings.AZURE_POSTGRESQL_CONNECTIONSTRING
    if env_connection_string is None:
        logger.info("Missing environment variable AZURE_POSTGRESQL_CONNECTIONSTRING")
    else:
        # Parse the connection string
        details = dict(item.split("=") for item in env_connection_string.split())

        # Properly format the URL for SQLAlchemy
        sql_url = (
            f"postgresql://{quote_plus(details['user'])}:{quote_plus(details['password'])}"
            f"@{details['host']}:{details['port']}/{details['dbname']}?sslmode={details['sslmode']}"
        )

else:
    logger.info("Connecting to local PostgreSQL server based on .env file...")

    POSTGRES_USERNAME = settings.POSTGRES_USERNAME
    POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
    POSTGRES_HOST = settings.POSTGRES_HOST
    POSTGRES_DATABASE = settings.POSTGRES_DATABASE
    POSTGRES_PORT = settings.POSTGRES_PORT

    sql_url = (
        f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    )

# Create the SQLAlchemy engine
engine = create_engine(sql_url, pool_pre_ping=True, pool_recycle=3600, pool_size=20, max_overflow=0)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db_url() -> str:
    """Get the database URL."""
    if settings.WEBSITE_HOSTNAME:
        env_connection_string = settings.AZURE_POSTGRESQL_CONNECTIONSTRING
        # Parse the connection string
        details = dict(item.split("=") for item in env_connection_string.split())

        # Properly format the URL for SQLAlchemy
        sql_url = (
            f"postgresql://{quote_plus(details['user'])}:{quote_plus(details['password'])}"
            f"@{details['host']}:{details['port']}/{details['dbname']}?sslmode={details['sslmode']}"
        )
        return sql_url
    else:
        return f"postgresql://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}"


def get_db_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_db_and_tables():
    return SQLModel.metadata.create_all(engine)
