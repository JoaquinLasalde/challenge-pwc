from datetime import date, datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from uuid import UUID
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.book import Book
    from app.models.user import User

class Loan(BaseModel, table=True):
    __tablename__ = "loans"
    
    loan_date: date = Field(default_factory=lambda: date.today())
    return_date: Optional[date] = Field(default=None)
    due_date: date
    is_returned: bool = Field(default=False)
    
    # Foreign keys
    book_id: UUID = Field(foreign_key="books.id")
    user_id: UUID = Field(foreign_key="users.id")
    
    # Relationships
    book: "Book" = Relationship(back_populates="loans")
    user: "User" = Relationship(back_populates="loans") 