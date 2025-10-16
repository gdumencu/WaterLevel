"""
services/auth_service.py
Handles core authentication logic — verifying users and generating tokens.
Keeps routers clean and focused only on HTTP interactions.
"""

from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import verify_password
from app.core.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    Checks user credentials against the database.
    Raises HTTP 401 if authentication fails.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generates a signed JWT token with optional expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login_user(db: Session, username: str, password: str) -> dict:
    """
    Handles full login process:
      1. Verifies user credentials
      2. Generates access token
      3. Returns response payload
    """
    user = authenticate_user(db, username, password)
    token = create_access_token(data={"userName": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
