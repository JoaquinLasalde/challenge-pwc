from typing import List, Optional
from uuid import UUID
from datetime import date, datetime, timedelta
from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.loan import Loan
from app.models.book import Book
from app.schemas.loan import LoanCreate, LoanUpdate
from app.services.base_service import BaseService

class LoanService(BaseService[Loan, LoanCreate, LoanUpdate]):
    """
    Service for Loan operations with custom business logic
    """
    def __init__(self):
        super().__init__(Loan)
    
    def create(self, db: Session, *, obj_in: LoanCreate) -> Loan:
        """
        Create a new loan with business logic
        - Check if book exists and has available copies
        - Set default loan date to today if not provided
        - Calculate due date if not provided (14 days from loan date)
        """
        # Check if book exists and has available copies
        statement = select(Book).where(Book.id == obj_in.book_id)
        book = db.exec(statement).first()
        
        if not book:
            raise HTTPException(
                status_code=404,
                detail=f"Book with id {obj_in.book_id} not found"
            )
        
        if book.available_copies <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"Book '{book.title}' has no available copies"
            )
        
        # Set default loan date to today if not provided
        loan_date = obj_in.loan_date or date.today()
        
        # If due date is not provided, set it to 14 days from loan date
        due_date = obj_in.due_date
        
        # Create the loan
        loan_data = obj_in.model_dump()
        loan_data["loan_date"] = loan_date
        loan_data["due_date"] = due_date
        
        db_obj = self.model(**loan_data)
        
        # Update book available copies
        book.available_copies -= 1
        
        db.add(db_obj)
        db.add(book)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj
    
    def return_book(self, db: Session, loan_id: UUID) -> Loan:
        """
        Return a book
        - Mark loan as returned
        - Set return date to today
        - Increase book available copies
        """
        # Get the loan
        loan = self.get_by_id(db, loan_id)
        
        if loan.is_returned:
            raise HTTPException(
                status_code=400,
                detail="This book has already been returned"
            )
        
        # Get the book
        statement = select(Book).where(Book.id == loan.book_id)
        book = db.exec(statement).first()
        
        if not book:
            raise HTTPException(
                status_code=404,
                detail=f"Book with id {loan.book_id} not found"
            )
        
        # Update the loan
        loan.is_returned = True
        loan.return_date = date.today()
        loan.updated_at = datetime.utcnow()
        
        # Update the book
        book.available_copies += 1
        
        db.add(loan)
        db.add(book)
        db.commit()
        db.refresh(loan)
        
        return loan
    
    def get_overdue_loans(self, db: Session, skip: int = 0, limit: int = 100):
        """
        Get all overdue loans (due date is before today and not returned)
        Business transformation: filter by complex condition
        """
        today = date.today()
        statement = select(Loan).where(
            (Loan.due_date < today) & (Loan.is_returned == False)
        ).offset(skip).limit(limit)
        
        results = db.exec(statement).all()
        return results
    
    def get_loan_with_details(self, db: Session, loan_id: UUID):
        """
        Get a loan with book and user details
        """
        loan = self.get_by_id(db, loan_id)
        return loan
    
    # Business transformation - Get loan statistics
    def get_loan_statistics(self, db: Session):
        """
        Get statistics about loans
        This is a business transformation that computes various statistics
        """
        # Get all loans
        statement = select(Loan)
        loans = db.exec(statement).all()
        
        # Calculate statistics
        total_loans = len(loans)
        active_loans = sum(1 for loan in loans if not loan.is_returned)
        completed_loans = total_loans - active_loans
        
        today = date.today()
        overdue_loans = sum(1 for loan in loans if not loan.is_returned and loan.due_date < today)
        
        # Calculate average loan duration for completed loans
        completed_loan_days = [
            (loan.return_date - loan.loan_date).days
            for loan in loans if loan.is_returned and loan.return_date
        ]
        
        avg_loan_duration = sum(completed_loan_days) / len(completed_loan_days) if completed_loan_days else 0
        
        # Create statistics object
        stats = {
            "total_loans": total_loans,
            "active_loans": active_loans,
            "completed_loans": completed_loans,
            "overdue_loans": overdue_loans,
            "average_loan_duration_days": round(avg_loan_duration, 1),
            "on_time_return_rate": round((completed_loans - overdue_loans) / completed_loans * 100, 1) if completed_loans else 0
        }
        
        return stats

# Create a singleton instance
loan_service = LoanService() 