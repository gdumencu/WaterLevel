# backend\app\dependencies.py
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, get_db


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
