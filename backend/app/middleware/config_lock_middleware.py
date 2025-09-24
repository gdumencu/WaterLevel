# app/middleware/config_lock_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.routers.config_lock import lock_state

class ConfigLockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow lock/unlock/status endpoints to pass through
        if request.url.path.startswith("/api/config"):
            return await call_next(request)

        # Block dashboard-related routes if locked by another user
        if lock_state["is_locked"]:
            user = request.headers.get("X-User")
            if user != lock_state["locked_by"]:
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": "Dashboard is locked for configuration",
                        "locked_by": lock_state["locked_by"],
                        "role": lock_state["role"]
                    }
                )
        return await call_next(request)
