# Description: Tax model for database table creation.
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, func

from src.fastapi_app.config.database import Base


class Tarif(Base):
    __tablename__ = "tarif"
    id = Column(Integer, primary_key=True, autoincrement=True)
    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)
    nettarif = Column(Float)
    systemtarif = Column(Float)
    includingVAT = Column(Boolean)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
