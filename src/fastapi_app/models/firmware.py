# Description: Tax model for database table creation.
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from sqlmodel import DateTime, ForeignKey, func

from src.fastapi_app.config.database import Base


class Firmware(Base):
    __tablename__ = "firmware"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    devicetype_id = mapped_column(Integer, ForeignKey("devicetype.id"), nullable=False)

    version = mapped_column(String(50), nullable=False)
    filename = mapped_column(String(50), nullable=False)
    repo_url = mapped_column(String(50), nullable=True)
    is_active = mapped_column(Boolean, nullable=False)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    devicetype = relationship("DeviceType", back_populates="firmwares")
    devices = relationship("Device", back_populates="firmware", cascade="all, delete-orphan", passive_deletes=False)
