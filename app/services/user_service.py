from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from app.models.user import User
from app.models.loan import Loan
from app.schemas.user import UserCreate, UserUpdate
from app.services.base_service import BaseService

class UserService(BaseService[User, UserCreate, UserUpdate]):
    """
    Service for User operations with custom business logic
    """
    def __init__(self):
        super().__init__(User)
    
    # Get user with loans
    def get_user_with_loans(self, db: Session, user_id: UUID):
        """
        Get a user with their loan history
        """
        user = self.get_by_id(db, user_id)
        return user
    
    # Get users with active loans
    def get_users_with_active_loans(self, db: Session, skip: int = 0, limit: int = 100):
        """
        Get users who have active loans
        Business transformation: filter users based on related records
        """
        # First get all active loans
        statement = select(Loan).where(Loan.is_returned == False)
        loans = db.exec(statement).all()
        
        # Extract unique user IDs from active loans
        user_ids = set(loan.user_id for loan in loans)
        
        # Get users with those IDs
        statement = select(User).where(User.id.in_(user_ids)).offset(skip).limit(limit)
        results = db.exec(statement).all()
        
        return results
    
    # Business transformation - Create user activity summary
    def get_user_activity_summary(self, db: Session, user_id: UUID):
        """
        Get a summary of a user's library activity
        This is a business transformation that computes statistics for a user
        """
        user = self.get_by_id(db, user_id)
        
        # Get all loans for this user
        statement = select(Loan).where(Loan.user_id == user_id)
        loans = db.exec(statement).all()
        
        # Calculate statistics
        total_loans = len(loans)
        active_loans = sum(1 for loan in loans if not loan.is_returned)
        returned_loans = total_loans - active_loans
        unique_books = len(set(loan.book_id for loan in loans))
        
        # Create summary
        summary = {
            "user": {
                "id": str(user.id),
                "username": user.username,
                "full_name": user.full_name
            },
            "activity": {
                "total_loans": total_loans,
                "active_loans": active_loans,
                "returned_loans": returned_loans,
                "unique_books_borrowed": unique_books
            }
        }
        
        return summary

# Create a singleton instance
user_service = UserService() 