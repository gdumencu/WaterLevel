# backend/app/core/jwt.py

"""
🔐 jwt.py — JWT Token Creation Utility for WaterLevel

✅ Responsibilities:
- Create access tokens with expiration
- Use centralized config values for security
- Support flexible expiration overrides
"""

from datetime import datetime, timedelta
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# -------------------------------------------------------------------
# 1️⃣ Create JWT Access Token
# -------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    ✅ Creates a JWT token with expiration.
    - `data`: dictionary of claims (e.g., userName, role)
    - `expires_delta`: optional timedelta override
    - Uses default expiration from config if not provided
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"[DEBUG] Created JWT token: {encoded_jwt}")
    return encoded_jwt