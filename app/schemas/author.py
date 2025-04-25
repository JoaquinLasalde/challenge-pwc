from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

# Base schema with common attributes
class AuthorBase(BaseModel):
    name: str
    biography: Optional[str] = None
    birth_year: Optional[int] = None

# Schema for creating an author
class AuthorCreate(AuthorBase):
    pass

# Schema for updating an author
class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    biography: Optional[str] = None
    birth_year: Optional[int] = None

# Schema for author response
class Author(AuthorBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schema for expanded author response with book details
class AuthorWithBooks(Author):
    books: List["BookBrief"] = []

# Import this at the end to avoid circular imports
from app.schemas.book import BookBrief
AuthorWithBooks.model_rebuild() 