# backend/app/routers/audit_logs.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.database import get_db
from app.models.audit_logs import AuditLog
from app.models.user import User
from app.dependencies import get_current_admin_or_operator
from pydantic import BaseModel

router = APIRouter(
    tags=["Audit Logs"]
)

# ✅ Response schema for frontend
class AuditLogResponse(BaseModel):
    id: int
    action: str
    role: str
    details: str | None
    created_at: datetime

# ✅ GET logs for current user (Admin/Operator only)
@router.get("/logs/me", response_model=List[AuditLogResponse])
def get_my_audit_logs(
    start: datetime = Query(...),
    end: datetime = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_operator)
):
    logs = db.query(AuditLog).filter(
        AuditLog.user_id == current_user.id,
        AuditLog.created_at.between(start, end)
    ).order_by(AuditLog.created_at.desc()).all()
    return logs

# ✅ Optional: POST endpoint to create a log entry
class AuditLogCreateRequest(BaseModel):
    action: str  # "lock" or "unlock"
    details: str | None = None

@router.post("/logs")
def create_audit_log(
    payload: AuditLogCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_operator)
):
    if payload.action not in ["lock", "unlock"]:
        raise HTTPException(status_code=400, detail="Invalid action type")

    log = AuditLog(
        user_id=current_user.id,
        action=payload.action,
        role=current_user.role,
        details=payload.details
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"status": "success", "log_id": log.id}