from typing import Generic, List, Optional, Type, TypeVar
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session, SQLModel, select
from app.models.base import BaseModel

# Define generic types for models
ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for services with common CRUD operations
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get_all(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Get all records with pagination
        """
        statement = select(self.model).offset(skip).limit(limit)
        results = db.exec(statement).all()
        return results
    
    def get_by_id(self, db: Session, id: UUID) -> Optional[ModelType]:
        """
        Get a record by ID
        """
        statement = select(self.model).where(self.model.id == id)
        result = db.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return result
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record
        """
        db_obj = self.model.model_validate(obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """
        Update a record
        """
        # First convert input object to dict
        obj_data = obj_in.model_dump(exclude_unset=True)
        
        # Update the model instance with the new values
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        
        # Update the updated_at field
        db_obj.updated_at = datetime.utcnow()
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, *, id: UUID) -> ModelType:
        """
        Delete a record
        """
        obj = self.get_by_id(db, id)
        db.delete(obj)
        db.commit()
        return obj 