import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.show import Base

# Ensure the database_instance directory exists
os.makedirs("database_instance", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./database_instance/movies.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
