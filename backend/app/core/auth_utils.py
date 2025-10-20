# backend/app/core/auth_utils.py

"""
🔐 auth_utils.py — JWT Authentication Utilities for WaterLevel

✅ Responsibilities:
- Decode and validate JWT tokens
- Extract user identity and role
- Provide reusable dependencies for FastAPI routes
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.config import SECRET_KEY, ALGORITHM
from app.models.user import User
from app.dependencies import get_db

# -------------------------------------------------------------------
# 1️⃣ OAuth2 scheme for token extraction
# -------------------------------------------------------------------
# The frontend calls /login directly, not /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
print("[DEBUG] OAuth2PasswordBearer initialized with tokenUrl='login'")
# -------------------------------------------------------------------
# 2️⃣ Dependency: Get current user from token and DB
# -------------------------------------------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    ✅ Decodes the JWT token and fetches the user from the database.
    🔒 Raises 401 if token is invalid or expired.
    🔍 Raises 404 if user is not found in DB.
    """
    try:
        print("[DEBUG] Decoding token...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("userName")
        print(f"[DEBUG] Decoded token payload: {payload}")  
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload: missing userName"
            )

        user = db.query(User).filter(User.username == username).first()
        print(f"[DEBUG] Fetched user from DB: {user}")  
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    except JWTError:
        print("[ERROR] JWT decode error")   
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

# -------------------------------------------------------------------
# 3️⃣ Dependency: Get userName and role from token only
# -------------------------------------------------------------------
def get_current_user_with_role(
    token: str = Depends(oauth2_scheme)
) -> dict:
    """
    ✅ Decodes JWT and extracts userName and role without DB lookup.
    🔍 Useful for lightweight role-based access checks.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("userName")
        role: str = payload.get("role")
        print(f"[DEBUG] Decoded token payload for role check: {payload}")
        if not username or not role:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token: missing userName or role"
            )

        return {"userName": username, "role": role}

    except JWTError:
        print("[ERROR] JWT decode error in role check")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )