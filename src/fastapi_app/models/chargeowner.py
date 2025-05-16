# Description: Charger model for database table creation.
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from src.fastapi_app.config.database import Base


class Chargeowner(Base):
    __tablename__ = "chargeowner"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150))
    glnnumber = Column(String(15))
    company = Column(String(15))
    type = Column(String(150))
    chargetype = Column(String(255))
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    is_active = Column(Boolean, default=True)

    # charges = relationship('Charge', backref='chargeowner')
