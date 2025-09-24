# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import models to trigger registration
import app.models  # Triggers __init__.py
from app.models.database import Base, engine
from app.models import base, audit_logs, jobs, user, device, telemetry, reports

# Routers
from app.routers.panels import router as panels_router
from app.routers import auth
from app.routers import config_lock

# Middleware
from app.middleware.config_lock_middleware import ConfigLockMiddleware

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI(
    title="WaterLevel Dashboard API",
    description="Backend API for role-based dashboard panels",
    version="1.0.0"
)

# Middleware: Config Lock
app.add_middleware(ConfigLockMiddleware)

# Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(panels_router)
app.include_router(auth.router)
app.include_router(config_lock.router)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Health check from backend main.py"}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Backend is running - main.py"}

# DB connection test
@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"db_connection": "success", "result": [row[0] for row in result]}
    except Exception as e:
        return {"db_connection": "failed", "error": str(e)}
