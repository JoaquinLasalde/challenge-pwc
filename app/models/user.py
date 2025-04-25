from typing import List, Optional
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

class User(BaseModel, table=True):
    __tablename__ = "users"
    
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    full_name: str
    is_active: bool = Field(default=True)
    
    # Relationships
    loans: List["Loan"] = Relationship(back_populates="user") 