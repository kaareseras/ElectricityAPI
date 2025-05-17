# Description: Tax model for database table creation.
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import mapped_column, relationship

from src.fastapi_app.config.database import Base


class Device(Base):
    __tablename__ = "device"
    uuid = mapped_column(String(100), primary_key=True, nullable=False)
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = mapped_column(String(100), nullable=False)
    chargeowner_id = mapped_column(Integer, ForeignKey("chargeowner.id"), nullable=True)
    PriceArea = mapped_column(String(15), nullable=True)
    Config = mapped_column(String(1000), nullable=True)
    last_activity = mapped_column(DateTime, nullable=True)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="devices")
