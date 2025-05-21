# Description: Charger model for database table creation.
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import mapped_column, relationship

from src.fastapi_app.config.database import Base


class Chargeowner(Base):
    __tablename__ = "chargeowner"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    glnnumber = mapped_column(String(15))
    company = mapped_column(String(15))
    chargetype = mapped_column(String(150))
    chargetypecode = mapped_column(String(150))
    updated_at = mapped_column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    is_active = mapped_column(Boolean, default=True)

    charges = relationship("Charge", back_populates="chargeowner", cascade="all, delete-orphan", passive_deletes=True)
