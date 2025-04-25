from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.dependencies import get_session
from app.schemas.author import Author, AuthorCreate, AuthorUpdate, AuthorWithBooks
from app.services.author_service import author_service

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("/", response_model=List[Author])
def get_authors(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_session)
):
    """
    Get all authors with pagination
    """
    return author_service.get_all(db, skip=skip, limit=limit)

@router.get("/{author_id}", response_model=Author)
def get_author(
    author_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Get an author by ID
    """
    return author_service.get_by_id(db, author_id)

@router.get("/{author_id}/books", response_model=AuthorWithBooks)
def get_author_with_books(
    author_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Get an author with all their books
    """
    return author_service.get_author_with_books(db, author_id)

@router.get("/{author_id}/stats")
def get_author_with_stats(
    author_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Get an author with additional book statistics
    This demonstrates business transformation of data
    """
    return author_service.get_author_with_book_stats(db, author_id)

@router.post("/", response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(
    author_in: AuthorCreate, 
    db: Session = Depends(get_session)
):
    """
    Create a new author
    """
    return author_service.create(db, obj_in=author_in)

@router.patch("/{author_id}", response_model=Author)
def update_author(
    author_id: UUID, 
    author_in: AuthorUpdate, 
    db: Session = Depends(get_session)
):
    """
    Update an author
    """
    db_obj = author_service.get_by_id(db, author_id)
    return author_service.update(db, db_obj=db_obj, obj_in=author_in)

@router.delete("/{author_id}", response_model=Author)
def delete_author(
    author_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Delete an author
    """
    return author_service.delete(db, id=author_id) 