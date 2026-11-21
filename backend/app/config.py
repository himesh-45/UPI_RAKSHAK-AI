import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "UPI Rakshak AI"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/upi_rakshak.db")
    
    # Security & Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "upi_rakshak_super_secret_jwt_key_2026_demo_key_999")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24  # 24 hours
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@upirakshak.ai")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "AdminRakshak#2026")
    
    # Risk Fusion Thresholds (Configurable)
    SAFE_MAX_SCORE: int = 34
    SUSPICIOUS_MAX_SCORE: int = 69
    # Scores >= 70 are HIGH RISK
    
    # Pluggable external providers (optional, graceful fallback if missing)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY", None)
    GOOGLE_SAFE_BROWSING_KEY: Optional[str] = os.getenv("GOOGLE_SAFE_BROWSING_KEY", None)
    VIRUSTOTAL_API_KEY: Optional[str] = os.getenv("VIRUSTOTAL_API_KEY", None)

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
