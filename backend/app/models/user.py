# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class User(Base):
    """
    SQLAlchemy User model.
    Stores user credentials and role-based access.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    audit_logs = relationship(
        "AuditLog", back_populates="user", cascade="all, delete-orphan"
    )
