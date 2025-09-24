from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/config", tags=["Config Lock"])

lock_state = {
    "is_locked": False,
    "locked_by": None,
    "role": None,
    "timestamp": None
}

class LockRequest(BaseModel):
    userName: str
    role: str

@router.get("/status")
async def get_lock_status(
    authorization: str = Header(None),
    x_user: str = Header(None)
):
    print(f"[STATUS] Auth: {authorization}, X-User: {x_user}")
    return lock_state

@router.post("/lock")
async def lock_config(
    req: LockRequest,
    authorization: str = Header(None),
    x_user: str = Header(None)
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
    return {
        "message": "Lock acquired",
        "locked_by": req.userName,
        "role": req.role,
        "timestamp": lock_state["timestamp"]
    }

@router.post("/unlock")
async def unlock_config(
    req: LockRequest,
    authorization: str = Header(None),
    x_user: str = Header(None)
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
    return {"message": "Lock released"}
