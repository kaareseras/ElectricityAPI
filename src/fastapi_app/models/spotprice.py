# Description: Charger model for database table creation.

from sqlalchemy import Column, DateTime, Float, Integer, String, func

from src.fastapi_app.config.database import Base


class Spotprice(Base):
    __tablename__ = "spotprice"
    id = Column(Integer, primary_key=True, autoincrement=True)
    HourUTC = Column(DateTime, nullable=False)
    HourDK = Column(DateTime, nullable=False)
    DateDK = Column(DateTime, nullable=False, index=True)
    PriceArea = Column(String(15), nullable=False, index=True)
    SpotpriceDKK = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
