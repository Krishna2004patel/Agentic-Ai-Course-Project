import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Research Grant Management System"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Institution Branding
    DEFAULT_INSTITUTION: str = "KLE Technological University"
    DEFAULT_CAMPUS: str = "Hubballi, Karnataka"
    PRIMARY_COLOR: str = "#0f172a"
    ACCENT_COLOR: str = "#dc2626"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/grant_system.db")
    
    # LLM Settings (OpenAI / Ollama / Demo Fallback)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # Mode flag: If True or if no API key is present, system operates with smart verifiable reasoning engine
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")

    # Document Upload Directory
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./data/uploads")
    
    class Config:
        case_sensitive = True
        extra = "allow"

settings = Settings()
