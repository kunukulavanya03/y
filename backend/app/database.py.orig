from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
from app.models import User, Data
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
cfg = BaseSettings()

def get_db():
    engine = create_engine(cfg.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
