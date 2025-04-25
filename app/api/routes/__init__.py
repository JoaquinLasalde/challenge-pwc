from app.api.routes.authors import router as authors_router
from app.api.routes.books import router as books_router
from app.api.routes.users import router as users_router
from app.api.routes.loans import router as loans_router

__all__ = ["authors_router", "books_router", "users_router", "loans_router"] 