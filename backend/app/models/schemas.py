from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class EvidenceItem(BaseModel):
    signal: str
    source_module: str  # "NLP_CLASSIFIER", "RULE_SAFETY_LAYER", "URL_SCANNER", "QR_PARSER", "OCR_EXTRACTOR"
    weight: float
    severity: str = "MEDIUM"  # "INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"

class RAGCitation(BaseModel):
    title: str
    content: str
    source: str
    relevance_score: Optional[float] = None

class SafetyReport(BaseModel):
    id: Optional[int] = None
    verdict: str  # "SAFE", "SUSPICIOUS", "HIGH RISK"
    risk_score: int = Field(ge=0, le=100)
    detected_category: str
    language: str = "en"
    confidence: float = 0.0
    evidence: List[EvidenceItem] = []
    recommended_actions: List[str] = []
    citations: List[RAGCitation] = []
    plain_language_explanation: str = ""
    masked_input: str = ""
    disclaimer: str = (
        "Heuristic risk indicator based on independent pattern detectors. "
        "Not a calibrated statistical probability and not a guarantee of safety. "
        "SAFE denotes no strong scam signals found. Always verify directly with your bank. "
        "In case of fraud, immediately call national helpline 1930 or visit cybercrime.gov.in."
    )
    is_simulated: bool = False

class TextAnalysisRequest(BaseModel):
    text: str = Field(min_length=1, max_length=10000)
    language: Optional[str] = "auto"
    save_history: bool = True

class UrlAnalysisRequest(BaseModel):
    url: str = Field(min_length=3, max_length=2048)
    save_history: bool = True

class AssistantChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    language: str = "en"  # "en", "hi", "te"
    context_report_id: Optional[int] = None

class AssistantChatResponse(BaseModel):
    reply: str
    language: str
    verdict: Optional[str] = None
    risk_score: Optional[int] = None
    citations: List[RAGCitation] = []
    recommended_actions: List[str] = []

class ThreatReportCreate(BaseModel):
    analysis_id: Optional[int] = None
    input_type: str = "text"
    suspicious_content: str
    scam_category: str
    comments: Optional[str] = ""
    contact: Optional[str] = ""

class ThreatReportResponse(BaseModel):
    id: int
    status: str
    message: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: str

class DashboardStatsResponse(BaseModel):
    total_analyses: int
    safe_count: int
    suspicious_count: int
    high_risk_count: int
    category_distribution: Dict[str, int]
    top_signals: List[Dict[str, Any]]
    language_breakdown: Dict[str, int]
    risk_score_distribution: Dict[str, int]
    timeline_trend: List[Dict[str, Any]]
    recent_analyses: List[Dict[str, Any]]
    total_threat_reports: int
    seeded_vs_live: Dict[str, int]
