"""
routers/auth.py
FastAPI router for login and dashboard routes.
Uses the auth_service for clean business logic separation.
"""

from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.auth_service import login_user
from app.core.auth_utils import get_current_user

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    Login endpoint: verifies credentials and returns JWT token.
    """
    return login_user(db, username, password)

@router.get("/dashboard")
def dashboard(current_user = Depends(get_current_user)):
    """
    Example protected route: accessible only with valid JWT.
    """
    return {"message": f"Welcome {current_user.username}!", "role": current_user.role}
