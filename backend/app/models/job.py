# user.py
from sqlalchemy import Column, Integer, String, TIMESTAMP
from .base import Base
import datetime

class Job(Base):
    __tablename__ = "jobs" 
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String) 
    config_json = Column(String) 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
