import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base, SessionLocal
from .models.db_models import User
from .core.auth import get_password_hash

def init_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                email=settings.ADMIN_EMAIL,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD)
            )
            db.add(admin)
            db.commit()
        else:
            admin.hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
            db.commit()
    finally:
        db.close()

# Create DB tables & seed admin user
Base.metadata.create_all(bind=engine)
init_admin()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multilingual Evidence-Based Digital-Payment Scam Detection & Prevention Platform",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Demo/local environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_admin()

@app.get("/api/health", tags=["Health"])
def health_check():
    from .detectors.nlp_classifier import nlp_classifier
    from .detectors.ocr_pipeline import ocr_pipeline
    from .detectors.url_scanner import url_scanner
    from .rag.retriever import rag_retriever

    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "offline_ready": True,
        "engines": {
            "nlp_loaded": nlp_classifier.model is not None,
            "ocr_available": ocr_pipeline.ocr_available,
            "ocr_engine": ocr_pipeline.ocr_engine,
            "url_brands_indexed": len(url_scanner.all_legitimate_domains),
            "rag_knowledge_entries": len(rag_retriever.chunks)
        },
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

from .routes import analyze, assistant, report, dashboard, history, auth
from .database import get_db
from fastapi import Depends

@app.post("/api/feedback", response_model=analyze.UserFeedbackResponse, tags=["Threat Analysis"])
def api_feedback_alias(req: analyze.UserFeedbackRequest, db: SessionLocal = Depends(get_db)):
    return analyze.submit_feedback(req, db)

# Include Routers
app.include_router(analyze.router, prefix=settings.API_PREFIX)
app.include_router(assistant.router, prefix=settings.API_PREFIX)
app.include_router(report.router, prefix=settings.API_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_PREFIX)
app.include_router(history.router, prefix=settings.API_PREFIX)
app.include_router(auth.router, prefix=settings.API_PREFIX)
