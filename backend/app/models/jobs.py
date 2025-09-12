# user.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base

class Job(Base):
    __tablename__ = "jobs" 
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String) 
    config_json = Column(String) 
    created_at = Column(DateTime, default=datetime.utcnow)

