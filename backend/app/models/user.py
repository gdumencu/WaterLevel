# user.py
from sqlalchemy import Column, Integer, String, TIMESTAMP
from .base import Base
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

