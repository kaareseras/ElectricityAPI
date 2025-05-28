# Description: Charger model for database table creation.

from sqlalchemy import DateTime, Float, Index, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import mapped_column

from src.fastapi_app.config.database import Base


class Spotprice(Base):
    __tablename__ = "spotprice"
    __table_args__ = (
        UniqueConstraint("HourDK", "PriceArea", name="uq_hourdk_pricearea"),
        Index("ix_datedk_pricearea", "DateDK", "PriceArea"),
    )
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    HourUTC = mapped_column(DateTime, nullable=False)
    HourDK = mapped_column(DateTime, nullable=False)
    DateDK = mapped_column(DateTime, nullable=False, index=True)
    PriceArea = mapped_column(String(15), nullable=False, index=True)
    SpotpriceDKK = mapped_column(Float, nullable=False)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
