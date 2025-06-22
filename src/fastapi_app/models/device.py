# Description: Tax model for database table creation.
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import mapped_column, relationship

from src.fastapi_app.config.database import Base


class Device(Base):
    __tablename__ = "device"
    uuid = mapped_column(String(100), primary_key=True, nullable=False)
    name = mapped_column(String(100), nullable=True)
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    chargeowner_id = mapped_column(Integer, ForeignKey("chargeowner.id"), nullable=True)
    price_area = mapped_column(String(10), nullable=True)
    config = mapped_column(String(1000), nullable=True)
    last_activity = mapped_column(DateTime, nullable=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    is_adopted = mapped_column(Integer, nullable=False, default=0)
    adopted_at = mapped_column(DateTime, nullable=True)
    is_blocked = mapped_column(Integer, nullable=False, default=0)
    blocked_at = mapped_column(DateTime, nullable=True)

    user = relationship("User", back_populates="devices")
    chargeowner = relationship("Chargeowner", back_populates="devices")
