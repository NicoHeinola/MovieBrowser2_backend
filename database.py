import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure the database_instance directory exists
os.makedirs("database_instance", exist_ok=True)

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
