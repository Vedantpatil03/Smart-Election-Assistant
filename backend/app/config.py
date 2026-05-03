"""
Configuration settings for the Election Assistant application
"""
import os
from functools import lru_cache
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./election_assistant.db")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Languages
    SUPPORTED_LANGUAGES: List[str] = ["en", "hi", "mr"]
    DEFAULT_LANGUAGE: str = "en"
    
    # Gemini Model
    GEMINI_MODEL: str = "gemini-pro"
    
    # API Settings
    MAX_INPUT_LENGTH: int = 1000
    MAX_RESPONSE_LENGTH: int = 2000
    CHAT_TIMEOUT: int = 30


@lru_cache()
def get_settings() -> Settings:
    """Get application settings"""
    return Settings()


settings = get_settings()
