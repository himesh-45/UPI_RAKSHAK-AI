import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Ensure data directory exists if using relative sqlite path
if "sqlite" in settings.DATABASE_URL:
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def ensure_schema_migrations():
    if "sqlite" in settings.DATABASE_URL:
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_path):
            import sqlite3
            try:
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='analysis_history'")
                if cur.fetchone():
                    cur.execute("PRAGMA table_info(analysis_history)")
                    cols = [r[1] for r in cur.fetchall()]
                    if "channel" not in cols:
                        cur.execute("ALTER TABLE analysis_history ADD COLUMN channel VARCHAR(50) DEFAULT 'web'")
                        conn.commit()
                    if "sender_hash" not in cols:
                        cur.execute("ALTER TABLE analysis_history ADD COLUMN sender_hash VARCHAR(64) DEFAULT NULL")
                        conn.commit()
                conn.close()
            except Exception:
                pass

ensure_schema_migrations()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
