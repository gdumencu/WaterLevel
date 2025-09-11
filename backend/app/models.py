from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    audit_logs = relationship("AuditLog", back_populates="user")
    reports = relationship("Report", back_populates="user")

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100), nullable=False)
    details = Column(Text)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    serial_number = Column(String(100), unique=True)
    location = Column(String(100))
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    telemetry = relationship("Telemetry", back_populates="device")
    reports = relationship("Report", back_populates="device")

class Telemetry(Base):
    __tablename__ = 'telemetry'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    timestamp = Column(TIMESTAMP, nullable=False)
    data = Column(JSON, nullable=False)

    device = relationship("Device", back_populates="telemetry")

class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    device_id = Column(Integer, ForeignKey('devices.id'))
    report_path = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="reports")
    device = relationship("Device", back_populates="reports")
