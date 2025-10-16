"""
core/security.py
Handles password hashing and verification using Passlib.
"""

from passlib.context import CryptContext

# Initialize hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against its hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    """
    return pwd_context.hash(password)
