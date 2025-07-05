# Description: Tax model for database table creation.
from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from src.fastapi_app.config.database import Base


class DeviceType(Base):
    __tablename__ = "devicetype"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(100), nullable=False)
    hw_version = mapped_column(String(50), nullable=True)
    sw_version = mapped_column(String(50), nullable=True)
    sw_date = mapped_column(Date, nullable=True)


DeviceType.devices = relationship("Device", back_populates="devicetype")


class Firmware(Base):
    __tablename__ = "firmware"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    devicetype_id = mapped_column(Integer, nullable=False)

    version = mapped_column(String(50), nullable=True)
    filename = mapped_column(String(50), nullable=True)
    repo_url = mapped_column(String(50), nullable=True)
    is_active = mapped_column(Boolean, nullable=True)
    created_at = mapped_column(Date, nullable=True)


Firmware.devicetypes = relationship("DeviceType", back_populates="firmwares")


class Hardware(Base):
    __tablename__ = "hardware"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    devicetype_id = mapped_column(Integer, nullable=False)
    version = mapped_column(String(50), nullable=True)
    name = mapped_column(String(100), nullable=False)
    description = mapped_column(String(500), nullable=False)
    created_at = mapped_column(Date, nullable=True)
    is_active = mapped_column(Boolean, nullable=True)


Hardware.devicetypes = relationship("DeviceType", back_populates="hardwares")
