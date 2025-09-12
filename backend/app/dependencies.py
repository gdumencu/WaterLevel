# dependencies.py
from sqlalchemy.orm import Session
from models.database import SessionLocal  # adjust path if needed

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
