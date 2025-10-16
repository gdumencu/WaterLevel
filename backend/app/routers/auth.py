# backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import verify_password, get_password_hash
from app.core.auth_utils import get_current_user  # for protected routes
from app.dependencies import get_db
from app.models.user import User

router = APIRouter(tags=["Authentication"])  # No prefix

# ----------------------
# Login endpoint
# ----------------------
@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    """
    user: User = db.query(User).filter(User.username == form_data.username).first()
    print(f"[DEBUG] Attempting login for user: {form_data.username}")

    if not user or not verify_password(form_data.password, user.hashed_password):
        print("[DEBUG] Invalid credentials")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

    # Include username and role in JWT token
    from app.core.jwt import create_access_token
    token = create_access_token(data={"username": user.username, "role": user.role})
    print(f"[DEBUG] Login successful for user: {user.username}")

    return {"access_token": token, "token_type": "bearer"}

# ----------------------
# Dashboard endpoint
# ----------------------
@router.get("/dashboard", response_model=dict)
def dashboard(current_user: User = Depends(get_current_user)):
    """
    Example protected endpoint.
    """
    print(f"[DEBUG] Accessing dashboard for user: {current_user.username}")
    return {"message": f"Welcome {current_user.username}!", "role": current_user.role}
