# database.py
""" from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 
import os 
from dotenv import load_dotenv

load_dotenv()
 
DATABASE_URL = os.getenv("DATABASE_URL") 
engine = create_engine(DATABASE_URL) 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
Base = declarative_base() """

# backend/app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from app.config import DATABASE_URL

# Base class for all models
Base = declarative_base()

# Engine creation
engine = create_engine(
    DATABASE_URL,
    echo=True,          # Set to False in production
    pool_pre_ping=True  # Helps with stale connections
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency to get DB session in FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Optional helper to create all tables
def init_db():
    from app.models import Base  # Ensure all models are imported
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")
