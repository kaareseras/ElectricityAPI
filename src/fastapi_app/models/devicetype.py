# Description: Tax model for database table creation.
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, relationship
from sqlmodel import DateTime, func

from src.fastapi_app.config.database import Base


class DeviceType(Base):
    __tablename__ = "devicetype"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(String(500), nullable=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    devices = relationship("Device", back_populates="devicetype")
    firmwares = relationship("Firmware", back_populates="devicetype")
    hardwares = relationship("Hardware", back_populates="devicetype")
