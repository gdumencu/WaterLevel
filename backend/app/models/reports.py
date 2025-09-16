from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base
class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    device_id = Column(Integer, ForeignKey('devices.id'))
    report_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # user = relationship("User", back_populates="reports")
    device = relationship("Device", back_populates="reports")