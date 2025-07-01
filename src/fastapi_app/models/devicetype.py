# Description: Tax model for database table creation.
from sqlalchemy import Date, Integer, String
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
