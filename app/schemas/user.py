from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Base schema with common attributes
class UserBase(BaseModel):
    username: str
    email: str
    full_name: str
    is_active: bool = True

# Schema for creating a user
class UserCreate(UserBase):
    pass

# Schema for updating a user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

# Schema for user response
class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schema for expanded user response with loan history
class UserWithLoans(User):
    loans: List["LoanBrief"] = []

# Import at the end to avoid circular imports
from app.schemas.loan import LoanBrief
UserWithLoans.model_rebuild() 