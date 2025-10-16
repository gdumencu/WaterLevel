"""
core/settings.py
Holds configuration constants like SECRET_KEY and JWT settings.
Keeps secrets and algorithms centralized.
"""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

# Secret key for JWT encoding/decoding
SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")

# JWT signing algorithm
ALGORITHM = "HS256"

# Token expiration in minutes (used in auth_service)
ACCESS_TOKEN_EXPIRE_MINUTES = 60
