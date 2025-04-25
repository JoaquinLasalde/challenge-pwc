from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.dependencies import get_session
from app.schemas.loan import Loan, LoanCreate, LoanUpdate, LoanDetail
from app.services.loan_service import loan_service

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.get("/", response_model=List[Loan])
def get_loans(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_session)
):
    """
    Get all loans with pagination
    """
    return loan_service.get_all(db, skip=skip, limit=limit)

@router.get("/overdue", response_model=List[Loan])
def get_overdue_loans(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_session)
):
    """
    Get overdue loans (due date is before today and not returned)
    This demonstrates business logic filtering
    """
    return loan_service.get_overdue_loans(db, skip=skip, limit=limit)

@router.get("/statistics")
def get_loan_statistics(
    db: Session = Depends(get_session)
):
    """
    Get statistics about loans
    This demonstrates business transformation of data
    """
    return loan_service.get_loan_statistics(db)

@router.get("/{loan_id}", response_model=Loan)
def get_loan(
    loan_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Get a loan by ID
    """
    return loan_service.get_by_id(db, loan_id)

@router.get("/{loan_id}/details", response_model=LoanDetail)
def get_loan_with_details(
    loan_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Get a loan with book and user details
    """
    return loan_service.get_loan_with_details(db, loan_id)

@router.post("/", response_model=Loan, status_code=status.HTTP_201_CREATED)
def create_loan(
    loan_in: LoanCreate, 
    db: Session = Depends(get_session)
):
    """
    Create a new loan
    Business logic:
    - Checks if book exists and has available copies
    - Sets default loan date to today if not provided
    - Updates book availability
    """
    return loan_service.create(db, obj_in=loan_in)

@router.post("/{loan_id}/return", response_model=Loan)
def return_book(
    loan_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Return a book
    Business logic:
    - Marks loan as returned
    - Sets return date to today
    - Increases book available copies
    """
    return loan_service.return_book(db, loan_id)

@router.patch("/{loan_id}", response_model=Loan)
def update_loan(
    loan_id: UUID, 
    loan_in: LoanUpdate, 
    db: Session = Depends(get_session)
):
    """
    Update a loan
    """
    db_obj = loan_service.get_by_id(db, loan_id)
    return loan_service.update(db, db_obj=db_obj, obj_in=loan_in)

@router.delete("/{loan_id}", response_model=Loan)
def delete_loan(
    loan_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Delete a loan
    """
    return loan_service.delete(db, id=loan_id) 