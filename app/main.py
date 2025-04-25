from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import init_db
from app.api import authors_router

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

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {"status": "ok"}

# Version endpoint
@app.get("/version", tags=["Health"])
def version():
    """
    Get API version
    """
    return {"version": settings.API_VERSION}

# Include API routers
app.include_router(authors_router, prefix="/api")

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Import and include API routes
# We'll add these in later commits

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 