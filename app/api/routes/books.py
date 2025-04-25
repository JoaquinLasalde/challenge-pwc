from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.api.dependencies import get_session
from app.schemas.book import Book, BookCreate, BookUpdate, BookWithAuthor
from app.services.book_service import book_service

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[Book])
def get_books(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_session)
):
    """
    Get all books with pagination
    """
    return book_service.get_all(db, skip=skip, limit=limit)

@router.get("/available", response_model=List[Book])
def get_available_books(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_session)
):
    """
    Get available books (copies > 0)
    This demonstrates business logic filtering
    """
    return book_service.get_available_books(db, skip=skip, limit=limit)

@router.get("/by-author/{author_id}", response_model=List[Book])
def get_books_by_author(
    author_id: UUID, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_session)
):
    """
    Get all books by a specific author
    """
    return book_service.get_books_by_author(db, author_id, skip=skip, limit=limit)

@router.get("/by-genre/{genre}", response_model=List[Book])
def get_books_by_genre(
    genre: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_session)
):
    """
    Get all books in a specific genre
    """
    return book_service.get_books_by_genre(db, genre, skip=skip, limit=limit)

@router.get("/availability-summary")
def get_book_availability_summary(
    db: Session = Depends(get_session)
):
    """
    Get a summary of book availability by genre
    This demonstrates business transformation of data
    """
    return book_service.get_book_availability_summary(db)

@router.get("/{book_id}", response_model=Book)
def get_book(
    book_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Get a book by ID
    """
    return book_service.get_by_id(db, book_id)

@router.get("/{book_id}/with-author", response_model=BookWithAuthor)
def get_book_with_author(
    book_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Get a book with its author details
    """
    return book_service.get_book_with_author(db, book_id)

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: BookCreate, 
    db: Session = Depends(get_session)
):
    """
    Create a new book
    """
    return book_service.create(db, obj_in=book_in)

@router.patch("/{book_id}", response_model=Book)
def update_book(
    book_id: UUID, 
    book_in: BookUpdate, 
    db: Session = Depends(get_session)
):
    """
    Update a book
    """
    db_obj = book_service.get_by_id(db, book_id)
    return book_service.update(db, db_obj=db_obj, obj_in=book_in)

@router.delete("/{book_id}", response_model=Book)
def delete_book(
    book_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Delete a book
    """
    return book_service.delete(db, id=book_id) 