# backend/app/routers/config_lock.py

"""
🔐 Config Lock Router for WaterLevel

✅ Responsibilities:
- Track lock/unlock state of configuration
- Enforce single-user locking
- Log lock/unlock actions to audit_logs table
"""

from fastapi import APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
# from app.db import get_db
from app.db.database import get_db
from app.models.audit_logs import AuditLog
from app.models.user import User
from app.dependencies import get_current_user


# -------------------------------------------------------------------
# 1️⃣ Router Setup
# -------------------------------------------------------------------
router = APIRouter(prefix="/api/config", tags=["Config Lock"])
# router = APIRouter(tags=["Config Lock"])

# -------------------------------------------------------------------
# 2️⃣ In-memory Lock State (temporary, not persisted)
# -------------------------------------------------------------------
lock_state = {
    "is_locked": False,
    "locked_by": None,
    "role": None,
    "timestamp": None
}

# -------------------------------------------------------------------
# 3️⃣ Request Schema
# -------------------------------------------------------------------
class LockRequest(BaseModel):
    userName: str
    role: str

# -------------------------------------------------------------------
# 4️⃣ Audit Log Helper
# -------------------------------------------------------------------
def log_action(db: Session, user: User, action: str, details: str = ""):
    """
    Create an audit log entry for lock/unlock actions.
    """
    log = AuditLog(
        user_id=user.id,
        action=action,
        role=user.role,
        details=details,
        created_at=datetime.utcnow()
    )
    print(f"[LOG ACTION] User: {user.username}, Action: {action}, Role: {user.role}, Details: {details}")
    db.add(log)
    db.commit()
    db.refresh(log)
    print(f"[AUDIT LOG] User: {user.username}, Action: {action}, Role: {user.role}, Details: {details}")
    return log

# -------------------------------------------------------------------
# 5️⃣ GET Lock Status
# -------------------------------------------------------------------
@router.get("/status")
async def get_lock_status(
    authorization: str = Header(None),
    x_user: str = Header(None)
):
    print(f"[STATUS] Auth: {authorization}, X-User: {x_user}")
    return lock_state

# -------------------------------------------------------------------
# 6️⃣ POST Lock Config
# -------------------------------------------------------------------
@router.post("/lock")
async def lock_config(
    req: LockRequest,
    authorization: str = Header(None),
    x_user: str = Header(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    
):
    print(f"[LOCK] Auth: {authorization}, X-User: {x_user}")
    if lock_state["is_locked"]:
        raise HTTPException(status_code=403, detail="Dashboard is already locked.")

    lock_state.update({
        "is_locked": True,
        "locked_by": req.userName,
        "role": req.role,
        "timestamp": datetime.utcnow().isoformat()
    })

    # ✅ Log the lock action
    log_action(db, current_user, "lock", "User locked configuration")

    return {
        "message": "Lock acquired",
        "locked_by": req.userName,
        "role": req.role,
        "timestamp": lock_state["timestamp"]
    }

# -------------------------------------------------------------------
# 7️⃣ POST Unlock Config
# -------------------------------------------------------------------
@router.post("/unlock")
async def unlock_config(
    req: LockRequest,
    authorization: str = Header(None),
    x_user: str = Header(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"[UNLOCK] Auth: {authorization}, X-User: {x_user}")
    if lock_state["locked_by"] != req.userName:
        raise HTTPException(status_code=403, detail="Only the locker can unlock.")

    lock_state.update({
        "is_locked": False,
        "locked_by": None,
        "role": None,
        "timestamp": None
    })

    # ✅ Log the unlock action
    log_action(db, current_user, "unlock", "User unlocked configuration")

    return {"message": "Lock released"}