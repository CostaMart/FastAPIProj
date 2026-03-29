from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# load repositories to init
import repository.MusicRepository

async def initDb():
    print("database init")
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
