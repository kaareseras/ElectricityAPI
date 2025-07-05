# Description: Tax model for database table creation.
from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from src.fastapi_app.config.database import Base


class Hardware(Base):
    __tablename__ = "hardware"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    devicetype_id = mapped_column(Integer, ForeignKey("devicetype.id"), nullable=False)
    version = mapped_column(String(50), nullable=False)
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(String(500), nullable=True)
    created_at = mapped_column(Date, nullable=False)
    is_active = mapped_column(Boolean, nullable=False)

    devicetype = relationship("DeviceType", back_populates="hardwares")
    devices = relationship("Device", back_populates="hardware", cascade="all, delete-orphan", passive_deletes=False)
