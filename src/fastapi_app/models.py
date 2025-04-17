# import logging
# import os

# from urllib.parse import quote_plus
# from dotenv import load_dotenv
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.fastapi_app.config.database import Base


class Restaurant(Base):
    __tablename__ = "restaurant"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    street_address: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    reviews: Mapped[List["Review"]] = relationship(back_populates="restaurant", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "review"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurant.id", ondelete="CASCADE"), nullable=False)
    user_name: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    review_text: Mapped[str] = mapped_column()
    review_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    restaurant: Mapped["Restaurant"] = relationship(back_populates="reviews")
