# Description: Tax model for database table creation.
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from src.fastapi_app.config.database import Base


class Device(Base):
    __tablename__ = "device"
    uuid = Column(String(100), primary_key=True, nullable=False)
    chargeowner_id = Column(Integer, ForeignKey("chargeowner.id"), nullable=True)
    PriceArea = Column(String(15), nullable=True)
    Config = Column(String(1000), nullable=True)
    last_activity = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
