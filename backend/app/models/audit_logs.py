# backend/app/models/audit_logs.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class AuditLog(Base):
    """
    SQLAlchemy AuditLog model for config lock/unlock actions.
    """
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(Enum('lock', 'unlock', name='audit_action'), nullable=False)
    role = Column(String(50), nullable=False)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="audit_logs")
