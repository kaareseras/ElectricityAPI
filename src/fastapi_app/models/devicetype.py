# Description: Tax model for database table creation.
from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from src.fastapi_app.config.database import Base


class DeviceType(Base):
    __tablename__ = "devicetype"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(String(500), nullable=True)
    created_at = mapped_column(Date, nullable=False)

    devices = relationship("Device", back_populates="devicetype")
    firmwares = relationship("Firmware", back_populates="devicetype")
    hardwares = relationship("Hardware", back_populates="devicetype")
