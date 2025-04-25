from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import time
import uuid
from app.core.config import settings
from app.db.session import init_db
from app.api.v1 import v1_router
from app.core.logging import get_logger
from app.core.errors import http_exception_handler, validation_exception_handler, not_found_handler
from app.core.middleware import CorrelationIdMiddleware, TimingMiddleware

# Configure logger
logger = get_logger(__name__)

# Create the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="FastAPI application for library management"
)

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(404, not_found_handler)
app.add_exception_handler(Exception, http_exception_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add correlation ID middleware
app.add_middleware(CorrelationIdMiddleware)

# Add timing middleware
app.add_middleware(TimingMiddleware)

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify API is running
    """
    logger.debug("Health check endpoint called")
    return {"status": "ok"}

# Version endpoint
@app.get("/version", tags=["Health"])
def version():
    """
    Get API version
    """
    logger.debug("Version endpoint called")
    return {"version": settings.API_VERSION}

# Include API routers with versioning
app.include_router(v1_router, prefix="/api/v1")

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    logger.info(f"Starting application in {settings.ENVIRONMENT} mode")
    logger.info("Initializing database")
    init_db()
    logger.info("Application startup complete")

# Shutdown event handler
@app.on_event("shutdown")
def on_shutdown():
    logger.info("Application shutting down")

# Import and include API routes
# We'll add these in later commits

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True) 