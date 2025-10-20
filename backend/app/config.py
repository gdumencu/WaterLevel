# backend/app/config.py

"""
📦 config.py — Centralized Configuration Loader for WaterLevel

✅ Responsibilities:
- Load environment variables from .env
- Strip quotes from sensitive values
- Validate and parse types (str, int, bool, list)
- Centralize access to project-wide settings
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# -------------------------------------------------------------------
# 1️⃣ Load .env from backend root
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # points to backend/
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# -------------------------------------------------------------------
# 2️⃣ Utility: Strip quotes from env values
# -------------------------------------------------------------------
def clean_env(key: str, default: str = "") -> str:
    value = os.getenv(key, default)
    return value.strip('"').strip("'") if value else default

def clean_bool(key: str, default: bool = False) -> bool:
    return os.getenv(key, str(default)).lower() in ["true", "1", "yes"]

def clean_int(key: str, default: int = 0) -> int:
    try:
        return int(os.getenv(key, default))
    except ValueError:
        return default

def clean_list(key: str, default: str = "") -> list[str]:
    raw = os.getenv(key, default)
    return [item.strip() for item in raw.split(",") if item.strip()]

# -------------------------------------------------------------------
# 3️⃣ Database Configuration
# -------------------------------------------------------------------
DATABASE_URL = clean_env("DATABASE_URL")

# -------------------------------------------------------------------
# 4️⃣ FastAPI App Settings
# -------------------------------------------------------------------
APP_NAME = clean_env("APP_NAME", "WaterLevel Dashboard")
APP_VERSION = clean_env("APP_VERSION", "0.1.0")
DEBUG = clean_bool("DEBUG", True)

# -------------------------------------------------------------------
# 5️⃣ JWT / Security Settings
# -------------------------------------------------------------------
SECRET_KEY = clean_env("SECRET_KEY", "your-secret-key")
ALGORITHM = clean_env("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = clean_int("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
REFRESH_TOKEN_EXPIRE_MINUTES = clean_int("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7)

# -------------------------------------------------------------------
# 6️⃣ CORS Settings
# -------------------------------------------------------------------
ALLOWED_ORIGINS = clean_list("ALLOWED_ORIGINS", "*")

# -------------------------------------------------------------------
# 7️⃣ UART / Hardware Settings
# -------------------------------------------------------------------
DEFAULT_UART_PORT = clean_env("DEFAULT_UART_PORT", "COM1")
DEFAULT_BAUDRATE = clean_int("DEFAULT_BAUDRATE", 9600)
LINE_SEPARATOR = clean_env("LINE_SEPARATOR", "\n")

# -------------------------------------------------------------------
# 8️⃣ Logging & Audit
# -------------------------------------------------------------------
LOG_LEVEL = clean_env("LOG_LEVEL", "INFO")
AUDIT_LOGGING_ENABLED = clean_bool("AUDIT_LOGGING_ENABLED", True)