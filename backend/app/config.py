# backend/app/config.py
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env variables from project root
BASE_DIR = Path(__file__).resolve().parent.parent  # points to backend/
load_dotenv(dotenv_path=BASE_DIR / ".env")

# =========================
# Database configuration
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")  # e.g., postgres://user:pass@localhost/dbname

# =========================
# FastAPI settings
# =========================
APP_NAME = os.getenv("APP_NAME", "WaterLevel Dashboard")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
DEBUG = os.getenv("DEBUG", "True").lower() in ["true", "1"]

# =========================
# Security / Auth
# =========================
SECRET_KEY = os.getenv("SECRET_KEY")  # for JWT tokens
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# =========================
# CORS settings (for T9/T10)
# =========================
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# =========================
# UART / Hardware settings (for T12/T13)
# =========================
DEFAULT_UART_PORT = os.getenv("DEFAULT_UART_PORT", "COM1")  # or /dev/ttyUSB0
DEFAULT_BAUDRATE = int(os.getenv("DEFAULT_BAUDRATE", "9600"))
LINE_SEPARATOR = os.getenv("LINE_SEPARATOR", "\n")

# =========================
# Other project-wide settings
# =========================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
