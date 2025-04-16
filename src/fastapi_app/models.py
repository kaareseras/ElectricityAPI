# import logging
# import os

# from urllib.parse import quote_plus
# from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from src.fastapi_app.config.database import Base


class Restaurant(Base):
    __tablename__ = "restaurant"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    street_address = Column(String(500))
    description = Column(String(500))
    reviews = relationship("Review", back_populates="restaurant", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey("restaurant.id", ondelete="CASCADE"), nullable=False)
    user_name = Column(String(50), nullable=False)
    rating = Column(Integer)
    review_text = Column(String(500))
    review_date = Column(DateTime, default=func.now())
    restaurant = relationship("Restaurant", back_populates="reviews")


# from src.fastapi_app.models import Restaurant, Review

# logger = logging.getLogger("app")
# logger.setLevel(logging.INFO)

# sql_url = ""
# if os.getenv("WEBSITE_HOSTNAME"):
#     logger.info("Connecting to Azure PostgreSQL Flexible server based on AZURE_POSTGRESQL_CONNECTIONSTRING...")
#     env_connection_string = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
#     if env_connection_string is None:
#         logger.info("Missing environment variable AZURE_POSTGRESQL_CONNECTIONSTRING")
#     else:
#         Parse the connection string
#         details = dict(item.split("=") for item in env_connection_string.split())

#         Properly format the URL for SQLAlchemy
#         sql_url = (
#             f"postgresql://{quote_plus(details['user'])}:{quote_plus(details['password'])}"
#             f"@{details['host']}:{details['port']}/{details['dbname']}?sslmode={details['sslmode']}"
#         )

# else:
#     logger.info("Connecting to local PostgreSQL server based on .env file...")
#     load_dotenv()
#     POSTGRES_USERNAME = os.environ.get("DBUSER")
#     POSTGRES_PASSWORD = os.environ.get("DBPASS")
#     POSTGRES_HOST = os.environ.get("DBHOST")
#     POSTGRES_DATABASE = os.environ.get("DBNAME")
#     POSTGRES_PORT = os.environ.get("DBPORT", 5432)

#     sql_url = (
#         f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
#     )

# engine = create_engine(sql_url)


# def create_db_and_tables():
#     return SQLModel.metadata.create_all(engine)
