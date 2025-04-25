from fastapi import APIRouter

from app.api.routes.authors import router as authors_router
from app.api.routes.books import router as books_router
from app.api.routes.users import router as users_router
from app.api.routes.loans import router as loans_router

# Create v1 router
v1_router = APIRouter()

# Include all route modules
v1_router.include_router(authors_router)
v1_router.include_router(books_router)
v1_router.include_router(users_router)
v1_router.include_router(loans_router)

__all__ = ["v1_router"] 