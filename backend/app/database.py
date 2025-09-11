from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql+psycopg2://waterlevel_svc:G1g1.supomfuop@localhost/WaterLevel"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# To create tables (if needed):
# Base.metadata.create_all(bind=engine)
