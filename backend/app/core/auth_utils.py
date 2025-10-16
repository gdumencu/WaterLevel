"""
core/auth_utils.py
Utility functions for decoding and validating JWT tokens.
Used by dependencies to extract the current user and role.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.settings import SECRET_KEY, ALGORITHM
from app.models.user import User
from app.dependencies import get_db

# The frontend calls /login directly, not /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Decodes the JWT token and fetches the user from the database.
    Raises 401 if invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("userName")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def get_current_user_with_role(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Decodes JWT and extracts userName and role without DB lookup.
    Useful for lightweight role-based access checks.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("userName")
        role: str = payload.get("role")

        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        return {"userName": username, "role": role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
