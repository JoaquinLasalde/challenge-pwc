from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import date, datetime

# Base schema with common attributes
class LoanBase(BaseModel):
    loan_date: date
    due_date: date
    is_returned: bool = False
    return_date: Optional[date] = None

# Schema for creating a loan
class LoanCreate(BaseModel):
    book_id: UUID
    user_id: UUID
    due_date: date
    loan_date: Optional[date] = None

# Schema for updating a loan
class LoanUpdate(BaseModel):
    return_date: Optional[date] = None
    is_returned: Optional[bool] = None
    due_date: Optional[date] = None

# Brief loan schema (used in UserWithLoans to avoid circular references)
class LoanBrief(BaseModel):
    id: UUID
    loan_date: date
    due_date: date
    is_returned: bool
    return_date: Optional[date] = None
    book_id: UUID
    
    class Config:
        from_attributes = True

# Schema for loan response
class Loan(LoanBase):
    id: UUID
    book_id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schema for expanded loan response with book and user details
class LoanDetail(Loan):
    book: "BookBrief"
    user: "UserBrief"

# Brief book schema (used in LoanDetail to avoid circular references)
class BookBrief(BaseModel):
    id: UUID
    title: str
    isbn: str
    
    class Config:
        from_attributes = True

# Brief user schema (used in LoanDetail to avoid circular references)
class UserBrief(BaseModel):
    id: UUID
    username: str
    full_name: str
    
    class Config:
        from_attributes = True

# Import at the end to avoid circular imports
from app.schemas.book import BookBrief as BookSchema
from app.schemas.user import User as UserSchema
LoanDetail.model_rebuild() 