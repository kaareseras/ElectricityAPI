# Description: Charger model for database table creation.
from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.fastapi_app.config.database import Base


class Charge(Base):
    __tablename__ = "charge"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chargeowner_id: Mapped[int] = mapped_column(ForeignKey("chargeowner.id", ondelete="CASCADE"), nullable=False)
    charge_type: Mapped[str] = mapped_column(String(15))
    charge_type_code: Mapped[str] = mapped_column(String(15))
    note: Mapped[str] = mapped_column(String(250))
    description: Mapped[str] = mapped_column(String(250))
    valid_from: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    valid_to: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    price1: Mapped[float] = mapped_column(Float)
    price2: Mapped[float] = mapped_column(Float)
    price3: Mapped[float] = mapped_column(Float)
    price4: Mapped[float] = mapped_column(Float)
    price5: Mapped[float] = mapped_column(Float)
    price6: Mapped[float] = mapped_column(Float)
    price7: Mapped[float] = mapped_column(Float)
    price8: Mapped[float] = mapped_column(Float)
    price9: Mapped[float] = mapped_column(Float)
    price10: Mapped[float] = mapped_column(Float)
    price11: Mapped[float] = mapped_column(Float)
    price12: Mapped[float] = mapped_column(Float)
    price13: Mapped[float] = mapped_column(Float)
    price14: Mapped[float] = mapped_column(Float)
    price15: Mapped[float] = mapped_column(Float)
    price16: Mapped[float] = mapped_column(Float)
    price17: Mapped[float] = mapped_column(Float)
    price18: Mapped[float] = mapped_column(Float)
    price19: Mapped[float] = mapped_column(Float)
    price20: Mapped[float] = mapped_column(Float)
    price21: Mapped[float] = mapped_column(Float)
    price22: Mapped[float] = mapped_column(Float)
    price23: Mapped[float] = mapped_column(Float)
    price24: Mapped[float] = mapped_column(Float)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    chargeowner = relationship("Chargeowner", back_populates="charges")
