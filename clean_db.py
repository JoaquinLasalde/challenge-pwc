from sqlmodel import Session, delete
from app.db.session import engine
from app.models.loan import Loan
from app.models.book import Book
from app.models.author import Author
from app.models.user import User

def clean_database():
    """
    Clean all data from the database tables in the correct order to respect foreign key constraints.
    """
    print("Cleaning database...")
    
    with Session(engine) as session:
        # Delete in proper order to respect foreign key constraints
        
        # First delete loans (they depend on books and users)
        print("Deleting all loans...")
        session.exec(delete(Loan))
        
        # Then delete books (they depend on authors)
        print("Deleting all books...")
        session.exec(delete(Book))
        
        # Now delete authors
        print("Deleting all authors...")
        session.exec(delete(Author))
        
        # Finally delete users
        print("Deleting all users...")
        session.exec(delete(User))
        
        # Commit the changes
        session.commit()
    
    print("Database cleaned successfully!")

if __name__ == "__main__":
    clean_database() 