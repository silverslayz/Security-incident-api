"""
Database configuration and session management.
Uses SQLAlchemy for ORM and connection pooling.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
# echo=True logs all SQL queries (useful for learning/debugging)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Verifies connections before using them
)

# Session factory - creates database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()


def get_db():
    """
    Dependency function that provides a database session.
    Automatically closes the session when done.

    Usage in FastAPI:
        @app.get("/endpoint")
        def my_endpoint(db: Session = Depends(get_db)):
            # use db here
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
