# backend/auth/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from jose import jwt

# OAuth2 scheme for JWT bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Secret key for JWT decoding (replace with your actual secret)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def get_current_user_with_role(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Extracts user info and role from JWT token.
    Raises 401 if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        print(f"Decoded JWT payload: {payload}")  # Debugging line
        print(f"Extracted username: {username}, role: {role}")  # Debugging line
        if username is None or role is None:
            print("Username or role is None")  # Debugging line 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return {"username": username, "role": role}
    except jwt.ExpiredSignatureError:
        print("Token has expired")  # Debugging line    
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
