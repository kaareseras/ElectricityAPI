# Description: Charger model for database table creation.
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func

from src.fastapi_app.config.database import Base


class Charge(Base):
    __tablename__ = "charge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chargeowner_id = Column(Integer, ForeignKey("chargeowner.id", ondelete="CASCADE"), nullable=False)
    charge_type = Column(String(15))
    charge_type_code = Column(String(15))
    note = Column(String(250))
    description = Column(String(250))
    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)
    price1 = Column(Float)
    price2 = Column(Float)
    price3 = Column(Float)
    price4 = Column(Float)
    price5 = Column(Float)
    price6 = Column(Float)
    price7 = Column(Float)
    price8 = Column(Float)
    price9 = Column(Float)
    price10 = Column(Float)
    price11 = Column(Float)
    price12 = Column(Float)
    price13 = Column(Float)
    price14 = Column(Float)
    price15 = Column(Float)
    price16 = Column(Float)
    price17 = Column(Float)
    price18 = Column(Float)
    price19 = Column(Float)
    price20 = Column(Float)
    price21 = Column(Float)
    price22 = Column(Float)
    price23 = Column(Float)
    price24 = Column(Float)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
