from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from app.models.author import Author
from app.models.book import Book
from app.schemas.author import AuthorCreate, AuthorUpdate
from app.services.base_service import BaseService

class AuthorService(BaseService[Author, AuthorCreate, AuthorUpdate]):
    """
    Service for Author operations with custom business logic
    """
    def __init__(self):
        super().__init__(Author)
    
    # Business transformation - Get author with book stats (count and average publication year)
    def get_author_with_book_stats(self, db: Session, author_id: UUID):
        """
        Get an author with additional statistics about their books.
        This is a business transformation that adds computed fields not present in the database.
        """
        author = self.get_by_id(db, author_id)
        
        # Get all books by this author
        statement = select(Book).where(Book.author_id == author_id)
        books = db.exec(statement).all()
        
        # Calculate statistics
        book_count = len(books)
        pub_years = [book.publication_year for book in books if book.publication_year]
        avg_pub_year = sum(pub_years) / len(pub_years) if pub_years else None
        
        # Convert author to dict and add the stats
        author_dict = author.model_dump()
        author_dict["book_count"] = book_count
        author_dict["average_publication_year"] = avg_pub_year
        
        return author_dict
    
    # Get author with all their books
    def get_author_with_books(self, db: Session, author_id: UUID):
        """
        Get an author with all their books
        """
        author = self.get_by_id(db, author_id)
        return author

# Create a singleton instance
author_service = AuthorService() 