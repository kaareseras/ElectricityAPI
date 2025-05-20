# Description: Tax model for database table creation.
from sqlalchemy import Boolean, DateTime, Float, Integer, func
from sqlalchemy.orm import mapped_column

from src.fastapi_app.config.database import Base


class Tax(Base):
    __tablename__ = "tax"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    valid_from = mapped_column(DateTime, nullable=True)
    valid_to = mapped_column(DateTime, nullable=True)
    taxammount = mapped_column(Float)
    includingVAT = mapped_column(Boolean)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
