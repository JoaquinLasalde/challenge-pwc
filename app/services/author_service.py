from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.author import Author
from app.models.book import Book
from app.schemas.author import AuthorCreate, AuthorUpdate
from app.services.base_service import BaseService
from app.core.logging import get_logger

class AuthorService(BaseService[Author, AuthorCreate, AuthorUpdate]):
    """
    Service for Author operations with custom business logic
    """
    def __init__(self):
        super().__init__(Author)
        self.logger = get_logger(__name__)
    
    # Business transformation - Get author with book stats (count and average publication year)
    def get_author_with_book_stats(self, db: Session, author_id: UUID):
        """
        Get an author with additional statistics about their books.
        This is a business transformation that adds computed fields not present in the database.
        """
        self.logger.info(f"Getting author stats for author_id: {author_id}")
        author = self.get_by_id(db, author_id)
        
        # Get all books by this author
        statement = select(Book).where(Book.author_id == author_id)
        books = db.exec(statement).all()
        
        # Calculate statistics
        book_count = len(books)
        pub_years = [book.publication_year for book in books if book.publication_year]
        avg_pub_year = sum(pub_years) / len(pub_years) if pub_years else None
        
        self.logger.debug(f"Author {author_id} has {book_count} books with average publication year: {avg_pub_year}")
        
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
        self.logger.info(f"Getting author with books for author_id: {author_id}")
        author = self.get_by_id(db, author_id)
        book_count = len(author.books) if hasattr(author, "books") else 0
        self.logger.debug(f"Author {author_id} has {book_count} books")
        return author

    def get_with_books(self, db: Session, id: UUID):
        self.logger.info(f"Getting author with books for id: {id}")
        author = db.query(Author).filter(Author.id == id).first()
        if author:
            self.logger.debug(f"Found author {id}")
        else:
            self.logger.warning(f"Author with id {id} not found")
        return author
    
    def delete(self, db: Session, id: UUID):
        # Check if author has books
        self.logger.info(f"Attempting to delete author with id: {id}")
        books_count = db.query(Book).filter(Book.author_id == id).count()
        
        if books_count > 0:
            self.logger.warning(f"Cannot delete author {id}: Has {books_count} associated books")
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete author with ID {id} because they have {books_count} books associated. Delete the books first or reassign them to another author."
            )
        
        self.logger.info(f"Author {id} has no books, proceeding with deletion")
        return super().delete(db, id=id)
    
    def get_author_stats(self, db: Session, id: UUID):
        self.logger.info(f"Generating statistics for author with id: {id}")
        author = db.query(Author).filter(Author.id == id).first()
        if not author:
            self.logger.warning(f"Author with id {id} not found")
            raise HTTPException(status_code=404, detail="Author not found")
        
        books = db.query(Book).filter(Book.author_id == id).all()
        
        total_books = len(books)
        genres = set([book.genre for book in books if book.genre])
        oldest_book = min(books, key=lambda x: x.publication_year).publication_year if books and any(b.publication_year for b in books) else None
        newest_book = max(books, key=lambda x: x.publication_year).publication_year if books and any(b.publication_year for b in books) else None
        
        self.logger.debug(f"Author {id} stats: {total_books} books, {len(genres)} genres, year range: {oldest_book}-{newest_book}")
        
        return {
            "author_id": author.id,
            "author_name": author.name,
            "total_books": total_books,
            "genres": list(genres),
            "publication_year_range": [oldest_book, newest_book] if oldest_book else None,
            "average_books_per_year": total_books / (newest_book - oldest_book + 1) if oldest_book and newest_book and oldest_book != newest_book else total_books
        }

# Create a singleton instance
author_service = AuthorService() 