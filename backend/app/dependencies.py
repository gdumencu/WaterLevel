# backend/app/dependencies.py

"""
🔐 dependencies.py — Common FastAPI Dependencies for WaterLevel

✅ Responsibilities:
- Provide DB session dependency
- Decode JWT tokens and validate user identity
- Enforce role-based access control (RBAC)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.config import SECRET_KEY, ALGORITHM

# -------------------------------------------------------------------
# 1️⃣ OAuth2 scheme for extracting token from Authorization header
# -------------------------------------------------------------------
# The frontend sends `Authorization: Bearer <token>`
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------------------------------------------------------------------
# 2️⃣ Database session dependency
# -------------------------------------------------------------------
def get_db():
    """
    ✅ Provides a database session for route handlers.
    Ensures proper cleanup after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------------------------------------------
# 3️⃣ Decode JWT and fetch current user from DB
# -------------------------------------------------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    ✅ Decodes JWT token and retrieves user from DB.
    🔒 Raises 401 if token is invalid or expired.
    🔍 Raises 404 if user does not exist.
    """
    try:
        # Decode JWT using SECRET_KEY and ALGORITHM from config.py
        print("[DEBUG] Decoding token...(dependencies.py)")  
        print(f"[DEBUG] SECRET_KEY: {SECRET_KEY}, ALGORITHM: {ALGORITHM}")
        
        from jose import jwt
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # ✅ Align with login logic: use "userName" instead of "sub"
        username: str = payload.get("userName")
        print(f"[DEBUG] Decoded token payload: {payload}") 
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing userName"
            )

        # Fetch user from DB
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    except JWTError:
        print("Token decoding failed")
        print(f"[DEBUG] JWTError encountered while decoding token: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

# -------------------------------------------------------------------
# 4️⃣ Role-based access control: Admin or Operator only
# -------------------------------------------------------------------
def get_current_admin_or_operator(user: User = Depends(get_current_user)) -> User:
    """
    ✅ Ensures the current user has admin or operator role.
    🔒 Raises 403 if role is not allowed.
    """
    if user.role not in ["admin", "operator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: requires admin or operator role"
        )
    return user