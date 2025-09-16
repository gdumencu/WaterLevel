# backend/app/models/__init__.py
# Import all models so SQLAlchemy sees them when initializing metadata
from  app.models.user import User
from app.models.audit_logs import AuditLog
from app.models.base import Base
from app.models.database import engine, SessionLocal
# Add other models as needed (Device, Telemetry, etc.)
