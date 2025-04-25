from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookCreate, BookUpdate
from app.services.base_service import BaseService

class BookService(BaseService[Book, BookCreate, BookUpdate]):
    """
    Service for Book operations with custom business logic
    """
    def __init__(self):
        super().__init__(Book)
    
    # Book with author details
    def get_book_with_author(self, db: Session, book_id: UUID):
        """
        Get a book with its author details
        """
        book = self.get_by_id(db, book_id)
        return book
    
    # Get available books
    def get_available_books(self, db: Session, skip: int = 0, limit: int = 100):
        """
        Get books with available copies
        Business transformation: filter only available books
        """
        statement = select(Book).where(Book.available_copies > 0).offset(skip).limit(limit)
        results = db.exec(statement).all()
        return results
    
    # Get books by author
    def get_books_by_author(self, db: Session, author_id: UUID, skip: int = 0, limit: int = 100):
        """
        Get all books by a specific author
        """
        statement = select(Book).where(Book.author_id == author_id).offset(skip).limit(limit)
        results = db.exec(statement).all()
        return results
    
    # Get books by genre
    def get_books_by_genre(self, db: Session, genre: str, skip: int = 0, limit: int = 100):
        """
        Get all books in a specific genre
        """
        statement = select(Book).where(Book.genre == genre).offset(skip).limit(limit)
        results = db.exec(statement).all()
        return results
    
    # Business transformation - Create book availability summary
    def get_book_availability_summary(self, db: Session):
        """
        Get a summary of book availability by genre
        This is a business transformation that computes statistics across the database
        """
        statement = select(Book)
        books = db.exec(statement).all()
        
        # Group books by genre and calculate availability
        genres = {}
        for book in books:
            if book.genre not in genres:
                genres[book.genre] = {"total": 0, "available": 0, "books": []}
            
            genres[book.genre]["total"] += 1
            genres[book.genre]["available"] += book.available_copies
            genres[book.genre]["books"].append({
                "id": str(book.id),
                "title": book.title,
                "available_copies": book.available_copies
            })
        
        return genres

# Create a singleton instance
book_service = BookService() 