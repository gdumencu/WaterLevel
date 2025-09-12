# dependencies.py
from sqlalchemy.orm import Session
from app.models.database import SessionLocal  # adjust path if needed

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
