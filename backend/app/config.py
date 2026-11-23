import os
import secrets
from pydantic_settings import BaseSettings
from typing import Optional

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PROJECT_ROOT = os.path.dirname(_BASE_DIR)
_BACKEND_SECRET_PATH = os.path.join(_BASE_DIR, "data", ".admin_secret")
_ROOT_SECRET_PATH = os.path.join(_PROJECT_ROOT, "data", ".admin_secret")
_IN_MEM_ADMIN_PASSWORD = None

def _resolve_admin_password() -> str:
    global _IN_MEM_ADMIN_PASSWORD
    if _IN_MEM_ADMIN_PASSWORD:
        return _IN_MEM_ADMIN_PASSWORD

    env_pwd = os.getenv("ADMIN_PASSWORD")
    if env_pwd and env_pwd.strip():
        _IN_MEM_ADMIN_PASSWORD = env_pwd.strip()
        for p in [_BACKEND_SECRET_PATH, _ROOT_SECRET_PATH]:
            try:
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "w", encoding="utf-8") as f:
                    f.write(_IN_MEM_ADMIN_PASSWORD + "\n")
            except Exception:
                pass
        return _IN_MEM_ADMIN_PASSWORD

    # Check if existing .admin_secret already exists
    for p in [_BACKEND_SECRET_PATH, _ROOT_SECRET_PATH]:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    saved = f.read().strip()
                    if saved:
                        _IN_MEM_ADMIN_PASSWORD = saved
                        return _IN_MEM_ADMIN_PASSWORD
            except Exception:
                pass

    # Generate a cryptographically secure 16-character token on first run
    gen_pwd = secrets.token_urlsafe(16)
    _IN_MEM_ADMIN_PASSWORD = gen_pwd

    # Persist to disk so that restarts/reloads keep the exact same password
    for p in [_BACKEND_SECRET_PATH, _ROOT_SECRET_PATH]:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(gen_pwd + "\n")
        except Exception:
            pass

    print("\n" + "=" * 68)
    print(" [SECURITY] Admin password generated and saved to backend/data/.admin_secret")
    print("   Admin Email: admin@upirakshak.ai")
    print(f"   Password:    {gen_pwd}")
    print("=" * 68 + "\n")
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

    # Channel bot configuration (Telegram Bot)
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN", None)
    TELEGRAM_WEBHOOK_SECRET: Optional[str] = os.getenv("TELEGRAM_WEBHOOK_SECRET", None)

    # Channel privacy & rate limiting
    SENDER_HASH_SALT: str = os.getenv("SENDER_HASH_SALT", "upi_rakshak_salt_2026_demo")
    CHANNEL_RATE_LIMIT_PER_HOUR: int = int(os.getenv("CHANNEL_RATE_LIMIT_PER_HOUR", "20"))

    # Optional Speech-To-Text for channel voice notes
    ENABLE_OFFLINE_STT: bool = os.getenv("ENABLE_OFFLINE_STT", "false").lower() == "true"

    # Conversational Assistant Brain settings
    ASSISTANT_BACKEND: str = os.getenv("ASSISTANT_BACKEND", "template")
    ASSISTANT_PROVIDER: str = os.getenv("ASSISTANT_PROVIDER", "anthropic")
    ASSISTANT_MODEL: str = os.getenv("ASSISTANT_MODEL", "claude-3-5-haiku-20241022")
    ASSISTANT_DAILY_CAP: int = int(os.getenv("ASSISTANT_DAILY_CAP", "1000"))
    ASSISTANT_TIMEOUT_SECONDS: int = int(os.getenv("ASSISTANT_TIMEOUT_SECONDS", "15"))
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Model architecture selection: Classical TF-IDF Ensemble (default) vs Fine-Tuned Transformer
    USE_TRANSFORMER_NLP: bool = os.getenv("USE_TRANSFORMER_NLP", "false").lower() == "true"
    TRANSFORMER_MODEL_PATH: str = os.getenv("TRANSFORMER_MODEL_PATH", "backend/app/data/indic_transformer_model")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
