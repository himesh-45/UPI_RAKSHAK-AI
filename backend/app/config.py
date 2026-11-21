import os
import secrets
from pydantic_settings import BaseSettings
from typing import Optional

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SECRET_FILE = os.path.join(_BASE_DIR, "data", ".admin_secret")

def _resolve_admin_password() -> str:
    env_pwd = os.getenv("ADMIN_PASSWORD")
    if env_pwd and env_pwd.strip():
        return env_pwd.strip()
    
    os.makedirs(os.path.dirname(_SECRET_FILE), exist_ok=True)
    if os.path.exists(_SECRET_FILE):
        try:
            with open(_SECRET_FILE, "r", encoding="utf-8") as f:
                saved = f.read().strip()
                if saved:
                    return saved
        except Exception:
            pass

    gen_pwd = secrets.token_urlsafe(16)
    try:
        with open(_SECRET_FILE, "w", encoding="utf-8") as f:
            f.write(gen_pwd)
        print("\n" + "=" * 68)
        print(" [SECURITY] Ephemeral ADMIN_PASSWORD generated & stored in data/.admin_secret")
        print(f"   Admin Email: admin@upirakshak.ai")
        print(f"   Password:    {gen_pwd}")
        print("=" * 68 + "\n")
    except Exception:
        pass
    return gen_pwd

class Settings(BaseSettings):
    PROJECT_NAME: str = "UPI Rakshak AI"
    VERSION: str = "2.0.0"
    API_PREFIX: str = "/api"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/upi_rakshak.db")
    
    # Security & Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "upi_rakshak_super_secret_jwt_key_2026_demo_key_999")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24  # 24 hours
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@upirakshak.ai")
    ADMIN_PASSWORD: str = _resolve_admin_password()
    
    # Risk Fusion Thresholds (Configurable)
    SAFE_MAX_SCORE: int = int(os.getenv("SAFE_MAX_SCORE", "34"))
    SUSPICIOUS_MAX_SCORE: int = int(os.getenv("SUSPICIOUS_MAX_SCORE", "69"))
    
    # Pluggable external providers
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY", None)
    GOOGLE_SAFE_BROWSING_KEY: Optional[str] = os.getenv("GOOGLE_SAFE_BROWSING_KEY", None)
    VIRUSTOTAL_API_KEY: Optional[str] = os.getenv("VIRUSTOTAL_API_KEY", None)

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
