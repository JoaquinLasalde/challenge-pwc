from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid
from app.core.config import settings
from app.db.session import init_db
from app.api import authors_router, books_router, users_router, loans_router
from app.core.logging import get_logger

# Configure logger
logger = get_logger(__name__)

# Create the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description="FastAPI application for library management"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Log request
    logger.info(
        f"Request started | {request_id} | {request.method} {request.url.path}"
    )
    
    # Measure request processing time
    start_time = time.time()
    
    try:
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Request completed | {request_id} | {request.method} {request.url.path} | "
            f"Status: {response.status_code} | Time: {process_time:.3f}s"
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as e:
        # Log exception
        logger.error(
            f"Request failed | {request_id} | {request.method} {request.url.path} | {str(e)}"
        )
        raise

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

# Include API routers
app.include_router(authors_router, prefix="/api")
app.include_router(books_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(loans_router, prefix="/api")

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