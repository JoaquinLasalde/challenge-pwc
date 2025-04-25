from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.author import Author
    from app.models.loan import Loan

class Book(BaseModel, table=True):
    __tablename__ = "books"
    
    title: str = Field(index=True)
    isbn: str = Field(unique=True, index=True)
    publication_year: Optional[int] = Field(default=None)
    genre: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    available_copies: int = Field(default=1)
    
    # Foreign keys
    author_id: UUID = Field(foreign_key="authors.id")
    
    # Relationships
    author: "Author" = Relationship(back_populates="books")
    loans: List["Loan"] = Relationship(back_populates="book") 