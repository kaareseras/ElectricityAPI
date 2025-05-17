from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import mapped_column, relationship

from src.fastapi_app.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(150))
    email = mapped_column(String(255), unique=True, index=True)
    password = mapped_column(String(100))
    is_active = mapped_column(Boolean, default=False)
    is_admin = mapped_column(Boolean, default=False)
    verified_at = mapped_column(DateTime, nullable=True, default=None)
    updated_at = mapped_column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    tokens = relationship("UserToken", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)

    def get_context_string(self, context: str):
        return f"{context}{self.password[-6:]}{self.updated_at.strftime('%m%d%Y%H%M%S')}".strip()


class UserToken(Base):
    __tablename__ = "user_tokens"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    access_key = mapped_column(String(250), nullable=True, index=True, default=None)
    refresh_key = mapped_column(String(250), nullable=True, index=True, default=None)
    created_at = mapped_column(DateTime, nullable=False, server_default=func.now())
    expires_at = mapped_column(DateTime, nullable=False)

    user = relationship("User", back_populates="tokens")
