from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.dependencies import get_session
from app.schemas.user import User, UserCreate, UserUpdate, UserWithLoans
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[User])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_session)
):
    """
    Get all users with pagination
    """
    return user_service.get_all(db, skip=skip, limit=limit)

@router.get("/with-active-loans", response_model=List[User])
def get_users_with_active_loans(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_session)
):
    """
    Get users who currently have active loans
    This demonstrates business logic filtering across relationships
    """
    return user_service.get_users_with_active_loans(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Get a user by ID
    """
    return user_service.get_by_id(db, user_id)

@router.get("/{user_id}/loans", response_model=UserWithLoans)
def get_user_with_loans(
    user_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Get a user with their loan history
    """
    return user_service.get_user_with_loans(db, user_id)

@router.get("/{user_id}/activity")
def get_user_activity_summary(
    user_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Get a summary of a user's library activity
    This demonstrates business transformation of data
    """
    return user_service.get_user_activity_summary(db, user_id)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate, 
    db: Session = Depends(get_session)
):
    """
    Create a new user
    """
    return user_service.create(db, obj_in=user_in)

@router.patch("/{user_id}", response_model=User)
def update_user(
    user_id: UUID, 
    user_in: UserUpdate, 
    db: Session = Depends(get_session)
):
    """
    Update a user
    """
    db_obj = user_service.get_by_id(db, user_id)
    return user_service.update(db, db_obj=db_obj, obj_in=user_in)

@router.delete("/{user_id}", response_model=User)
def delete_user(
    user_id: UUID, 
    db: Session = Depends(get_session)
):
    """
    Delete a user
    """
    return user_service.delete(db, id=user_id) 