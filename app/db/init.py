from sqlmodel import Session
from app.db.session import engine, init_db
from app.db.init_data.data import init_db_data

def init_database():
    """Initialize the database schema and load sample data"""
    # Initialize database schema
    init_db()
    
    # Add sample data
    with Session(engine) as db:
        stats = init_db_data(db)
        print(f"Database initialized with: {stats}")

if __name__ == "__main__":
    init_database() 