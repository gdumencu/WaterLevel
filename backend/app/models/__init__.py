# backend/app/models/__init__.py
# Import all models so SQLAlchemy sees them when initializing metadata
""" from  app.models.user import User
from app.models.audit_logs import AuditLog
from app.models.base import Base
from db.database import engine, SessionLocal
# Add other models as needed (Device, Telemetry, etc.) """
# backend/app/models/__init__.py
# Expose models and Base for automatic table registration

from app.models.base import Base
from app.models.user import User
from app.models.audit_logs import AuditLog
# from app.models.device import Device
# from app.models.telemetry import Telemetry

# Optional: make it easier to import all models elsewhere
__all__ = ["Base", "User", "AuditLog"]  # add more as you create them
