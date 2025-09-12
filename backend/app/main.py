# main.py
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()
from .models.database import Base,engine
from .models import user,job,auditLog,device,telemetry
# Read DB connection from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://waterlevel_svc:G1g1.supomfuop@db/WaterLevel")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get("/health")
def health_check():
    return {"status": "ok Health from main.py in backend folder...."}


@app.get("/")
def read_root():
    return {"message": "Backend is running! - from mainin the backend folder........."}

@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            return {"db_connection": "success", "result": [row[0] for row in result]}
    except Exception as e:
        return {"db_connection": "failed", "error": str(e)}
