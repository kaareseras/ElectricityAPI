# Description: Tax model for database table creation.

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import mapped_column, relationship

from src.fastapi_app.config.database import Base
from src.fastapi_app.models.chargeowner import Chargeowner
from src.fastapi_app.models.devicetype import DeviceType
from src.fastapi_app.models.user import User


class Device(Base):
    __tablename__ = "device"

    uuid = mapped_column(String(100), primary_key=True, nullable=False)
    name = mapped_column(String(100), nullable=True)
    user_id = mapped_column(ForeignKey(User.id, ondelete="CASCADE"), nullable=True)
    chargeowner_id = mapped_column(Integer, ForeignKey(Chargeowner.id), nullable=True)
    devicetype_id = mapped_column(Integer, ForeignKey(DeviceType.id), nullable=False)
    price_area = mapped_column(String(10), nullable=True)
    is_electric_heated = mapped_column(Boolean, nullable=True, default=False)
    config = mapped_column(String(1000), nullable=True)
    last_activity = mapped_column(DateTime, nullable=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    is_adopted = mapped_column(Boolean, nullable=False, default=False)
    adopted_at = mapped_column(DateTime, nullable=True)
    is_blocked = mapped_column(Boolean, nullable=False, default=False)
    blocked_at = mapped_column(DateTime, nullable=True)
    retail_markup = mapped_column(Float, nullable=True)

    user = relationship(User, back_populates="devices")
    chargeowner = relationship(Chargeowner, back_populates="devices")
    devicetype = relationship(DeviceType, back_populates="devices")
