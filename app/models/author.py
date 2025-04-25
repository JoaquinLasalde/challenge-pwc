from typing import List, Optional
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

class Author(BaseModel, table=True):
    __tablename__ = "authors"
    
    name: str = Field(index=True)
    biography: Optional[str] = Field(default=None)
    birth_year: Optional[int] = Field(default=None)
    
    # Relationships
    books: List["Book"] = Relationship(back_populates="author") 