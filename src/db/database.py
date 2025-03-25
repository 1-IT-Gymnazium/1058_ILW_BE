from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import get_settings

>>>>>>> HEAD
DATABASE_URL = ""
>>>>>>>

DATABASE_URL = get_settings().neondb_string
>>>>>>> 0611f6d (changed db)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
