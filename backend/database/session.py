from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# We will use sqlite for frictionless local development
SQLITE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./recruit.db"
)

# create engine instance
engine = create_engine(
    SQLITE_URL,
    connect_args={"check_same_thread": False},
    echo=False # Set to True for SQL logging
)

# create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for models
Base = declarative_base()

# Dependency func for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
