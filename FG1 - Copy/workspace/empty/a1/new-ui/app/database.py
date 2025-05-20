from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# SQLAlchemy engine and session setup
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # SQLite specific config
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
