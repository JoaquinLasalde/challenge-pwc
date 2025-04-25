from sqlmodel import Session, SQLModel, create_engine
from app.core.config import settings
import os

# Create the database engine
engine = create_engine(
    settings.DATABASE_URL, 
    echo=settings.ENVIRONMENT == "development",
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

def get_session():
    """
    Dependency for getting a SQLModel session
    """
    with Session(engine) as session:
        yield session

def init_db():
    """
    Initialize database tables
    """
    # Import all models here to ensure they are registered with SQLModel
    from app.models import Author, Book, Loan, User
    
    # Create tables in database
    SQLModel.metadata.create_all(engine) 