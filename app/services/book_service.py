from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookCreate, BookUpdate
from app.services.base_service import BaseService
from app.core.logging import get_logger

class BookService(BaseService[Book, BookCreate, BookUpdate]):
    """
    Service for Book operations with custom business logic
    """
    def __init__(self):
        super().__init__(Book)
        self.logger = get_logger(__name__)
    
    def create(self, db: Session, *, obj_in: BookCreate) -> Book:
        """
        Create a new book with validation that the author exists
        """
        self.logger.info("Creating new book")
        # Verify the author exists
        author = db.query(Author).filter(Author.id == obj_in.author_id).first()
        if not author:
            self.logger.warning(f"Cannot create book: Author with ID {obj_in.author_id} not found")
            raise HTTPException(
                status_code=404,
                detail=f"Cannot create book: Author with ID {obj_in.author_id} not found"
            )
        
        self.logger.debug(f"Author {obj_in.author_id} found, proceeding with book creation")
        # Proceed with book creation
        return super().create(db, obj_in=obj_in)
    
    def update(self, db: Session, *, db_obj: Book, obj_in: BookUpdate) -> Book:
        """
        Update a book with validation that the author exists if author_id is being updated
        """
        self.logger.info(f"Updating book with id: {db_obj.id}")
        # Convert input object to dict
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # If author_id is being updated, verify the new author exists
        if "author_id" in update_data:
            author = db.query(Author).filter(Author.id == update_data["author_id"]).first()
            if not author:
                self.logger.warning(f"Cannot update book: Author with ID {update_data['author_id']} not found")
                raise HTTPException(
                    status_code=404,
                    detail=f"Cannot update book: Author with ID {update_data['author_id']} not found"
                )
            self.logger.debug(f"New author {update_data['author_id']} found, proceeding with book update")
        
        # Proceed with book update
        return super().update(db, db_obj=db_obj, obj_in=obj_in)
    
    # Book with author details
    def get_book_with_author(self, db: Session, book_id: UUID):
        """
        Get a book with its author details
        """
        self.logger.info(f"Getting book with author details for book_id: {book_id}")
        book = self.get_by_id(db, book_id)
        if hasattr(book, "author") and book.author:
            self.logger.debug(f"Book {book_id} has author: {book.author.id}")
        else:
            self.logger.debug(f"Book {book_id} has no associated author")
        return book
    
    # Get available books
    def get_available_books(self, db: Session, skip: int = 0, limit: int = 100):
        """
        Get books with available copies
        Business transformation: filter only available books
        """
        self.logger.info(f"Getting available books (skip={skip}, limit={limit})")
        statement = select(Book).where(Book.available_copies > 0).offset(skip).limit(limit)
        results = db.exec(statement).all()
        self.logger.debug(f"Found {len(results)} available books")
        return results
    
    # Get books by author
    def get_books_by_author(self, db: Session, author_id: UUID, skip: int = 0, limit: int = 100):
        """
        Get all books by a specific author
        """
        self.logger.info(f"Getting books by author_id: {author_id} (skip={skip}, limit={limit})")
        statement = select(Book).where(Book.author_id == author_id).offset(skip).limit(limit)
        results = db.exec(statement).all()
        self.logger.debug(f"Found {len(results)} books for author {author_id}")
        return results
    
    # Get books by genre
    def get_books_by_genre(self, db: Session, genre: str, skip: int = 0, limit: int = 100):
        """
        Get all books in a specific genre
        """
        self.logger.info(f"Getting books by genre: {genre} (skip={skip}, limit={limit})")
        statement = select(Book).where(Book.genre == genre).offset(skip).limit(limit)
        results = db.exec(statement).all()
        self.logger.debug(f"Found {len(results)} books in genre '{genre}'")
        return results
    
    # Business transformation - Create book availability summary
    def get_book_availability_summary(self, db: Session):
        """
        Get a summary of book availability by genre
        This is a business transformation that computes statistics across the database
        """
        self.logger.info("Generating book availability summary by genre")
        statement = select(Book)
        books = db.exec(statement).all()
        
        # Group books by genre and calculate availability
        genres = {}
        for book in books:
            genre_name = book.genre or "Uncategorized"
            if genre_name not in genres:
                genres[genre_name] = {"total": 0, "available": 0, "books": []}
            
            genres[genre_name]["total"] += 1
            genres[genre_name]["available"] += book.available_copies
            genres[genre_name]["books"].append({
                "id": str(book.id),
                "title": book.title,
                "available_copies": book.available_copies
            })
        
        self.logger.debug(f"Generated availability summary for {len(genres)} genres")
        return genres

# Create a singleton instance
book_service = BookService() 