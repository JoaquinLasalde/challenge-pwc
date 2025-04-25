from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

# Base schema with common attributes
class BookBase(BaseModel):
    title: str
    isbn: str
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    available_copies: int = 1

# Schema for creating a book
class BookCreate(BookBase):
    author_id: UUID

# Schema for updating a book
class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    available_copies: Optional[int] = None
    author_id: Optional[UUID] = None

# Brief book schema (used in AuthorWithBooks to avoid circular references)
class BookBrief(BaseModel):
    id: UUID
    title: str
    isbn: str
    publication_year: Optional[int] = None
    
    class Config:
        from_attributes = True

# Schema for book response
class Book(BookBase):
    id: UUID
    author_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schema for expanded book response with author details
class BookWithAuthor(Book):
    author: "AuthorBrief"

# Brief author schema (used in BookWithAuthor to avoid circular references)
class AuthorBrief(BaseModel):
    id: UUID
    name: str
    
    class Config:
        from_attributes = True

# Import at the end to avoid circular imports
from app.schemas.author import Author as AuthorSchema
BookWithAuthor.model_rebuild() 