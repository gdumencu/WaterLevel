# backend/app/services/auth_service.py

"""
🔐 auth_service.py — Core Authentication Logic for WaterLevel

✅ Responsibilities:
- Verify user credentials against the database
- Generate JWT access tokens
- Return structured login responses
- Keep routers clean and focused on HTTP interactions
"""

from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import verify_password
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# -------------------------------------------------------------------
# 1️⃣ Authenticate user credentials
# -------------------------------------------------------------------
def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    ✅ Checks user credentials against the database.
    🔒 Raises 401 if authentication fails.
    """
    user = db.query(User).filter(User.username == username).first()
    print(f"[DEBUG] Authenticating user: {username}, Found user: {user}")   

    if not user or not verify_password(password, user.hashed_password):
        print("Authentication failed: invalid username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return user

# -------------------------------------------------------------------
# 2️⃣ Create JWT access token
# -------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    ✅ Generates a signed JWT token with optional expiration.
    - `data`: dictionary of claims (e.g., userName, role)
    - `expires_delta`: optional timedelta override
    - Uses default expiration from config if not provided
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"[DEBUG] ✅ Created JWT token in auth_service: {encoded_jwt}")  
    print(f"[DEBUG] Token data: {to_encode}")   
    print(f"[DEBUG] Token expires at: {expire}")
    print
    return encoded_jwt

# -------------------------------------------------------------------
# 3️⃣ Login process wrapper
# -------------------------------------------------------------------
def login_user(db: Session, username: str, password: str) -> dict:
    """
    ✅ Handles full login process:
      1. Verifies user credentials
      2. Generates access token
      3. Returns response payload
    """
    user = authenticate_user(db, username, password)

    token = create_access_token(data={
        "userName": user.username,
        "role": user.role
    })
    print(f"[DEBUG] Login successful for user: {username}, Token: {token}")

    return {
        "access_token": token,
        "token_type": "bearer"
    }