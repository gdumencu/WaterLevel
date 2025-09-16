# backend\app\main.py
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import app.models  # This triggers __init__.py and registers all models

import os
from dotenv import load_dotenv
load_dotenv()

from app.models.database import Base,engine
from app.dependencies import get_db
from app.models import base
from app.models import audit_logs, jobs, user, device, telemetry, reports
from app.routers import auth
from fastapi.middleware.cors import CORSMiddleware

# Read DB connection from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or ["*"] for all origins (less secure)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register routers
# -----------------------------
app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok Health from main.py in backend folder ___"}


@app.get("/")
def read_root():
    return {"message": "Backend is running! - from mainin the backend folder........."}


@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"db_connection": "success ***", "result": [row[0] for row in result]}
    except Exception as e:
        return {"db_connection": "failed", "error": str(e)}

