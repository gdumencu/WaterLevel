# backend/app/core/auth_utils.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from app.models.user import User
from app.dependencies import get_db

# -------------------------
# JWT Configuration
# -------------------------
SECRET_KEY = "your-secret-key"  # Use the same key as in your JWT creation
ALGORITHM = "HS256"

# OAuth2 scheme (corresponds to /login route)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------------------------
# Basic current user retrieval
# -------------------------
def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)) -> User:
    """
    Decodes the JWT token and returns the current user object from DB.
    Raises 401 if token is invalid or user does not exist.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# -------------------------
# Role-based user retrieval
# -------------------------
def get_current_user_with_role(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Decodes JWT and extracts username and role (without DB dependency).
    Useful for endpoints that only need role validation.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        role: str = payload.get("role")

        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        return {"username": username, "role": role}

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
