from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class Telemetry(Base):
    __tablename__ = 'telemetry'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    timestamp = Column(TIMESTAMP, nullable=False)
    data = Column(JSON, nullable=False)

    device = relationship("Device", back_populates="telemetry")