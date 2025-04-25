from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_VERSION: str = os.getenv("API_VERSION", "0.1.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    PROJECT_NAME: str = "PWC Challenge API"
    
    class Config:
        env_file = ".env"
        
settings = Settings() 