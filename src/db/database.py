from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_settings


DATABASE_URL = get_settings().neondb_string

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
