"""
Database module. To create database run python db.py.
"""
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

from models import Movie  # noqa

__all__ = (
    "DATABASE_URL",
    "ENGINE",
    "SessionLocal",
    "create_tables",
    "get_db",
)


# Initialize SQLite database
DATABASE_URL = "sqlite:///./test.db"
ENGINE = create_engine(DATABASE_URL)

# Session to work with
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=ENGINE,
)


def create_tables():
    """Create tables."""
    SQLModel.metadata.create_all(ENGINE)


def get_db():
    """Get database connection."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    create_tables()
