from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Application settings
    """
    # API information
    PROJECT_NAME: str = "Library Management API"
    API_VERSION: str = "1.0.0"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./library.db")
    
    class Config:
        env_file = ".env"

# Create a settings object
settings = Settings() 