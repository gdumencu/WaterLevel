# main.py
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Read DB connection from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://youruser:yourpassword@db/WaterLevel")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            return {"db_connection": "success", "result": [row[0] for row in result]}
    except Exception as e:
        return {"db_connection": "failed", "error": str(e)}
