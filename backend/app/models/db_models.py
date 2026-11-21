import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    input_type = Column(String, nullable=False)  # "text", "url", "image", "qr"
    raw_input_masked = Column(Text, nullable=False)
    verdict = Column(String, nullable=False)      # "SAFE", "SUSPICIOUS", "HIGH RISK"
    risk_score = Column(Integer, nullable=False)   # 0 to 100
    detected_category = Column(String, nullable=False)
    language = Column(String, default="en")
    evidence_json = Column(Text, default="[]")    # JSON serialized list of EvidenceItem
    actions_json = Column(Text, default="[]")     # JSON serialized list of strings
    is_simulated = Column(Boolean, default=False) # Distinguishes demo seed from real user queries
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    reports = relationship("ThreatReport", back_populates="analysis")
    feedbacks = relationship("Feedback", back_populates="analysis")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_history.id"), nullable=True)
    input_text_masked = Column(Text, nullable=True)
    reported_verdict = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    correct_category = Column(String, nullable=True)
    feedback_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    analysis = relationship("AnalysisHistory", back_populates="feedbacks")

class ThreatReport(Base):
    __tablename__ = "threat_reports"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_history.id"), nullable=True)
    input_type = Column(String, nullable=False)
    suspicious_content_masked = Column(Text, nullable=False)
    scam_category = Column(String, nullable=False)
    reporter_comments = Column(Text, nullable=True)
    reporter_contact_masked = Column(String, nullable=True)
    is_simulated = Column(Boolean, default=False)
    status = Column(String, default="PENDING_REVIEW")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    analysis = relationship("AnalysisHistory", back_populates="reports")
