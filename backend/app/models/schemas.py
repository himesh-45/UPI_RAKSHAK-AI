from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class EvidenceItem(BaseModel):
    signal: str
    source_module: str  # "NLP_CLASSIFIER", "RULE_SAFETY_LAYER", "URL_SCANNER", "QR_PARSER", "OCR_EXTRACTOR"
    weight: float
    severity: str = "MEDIUM"  # "INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"

class HighlightSpan(BaseModel):
    start: int
    end: int
    text: str
    label: str  # e.g., "CREDENTIAL_THEFT", "SUSPICIOUS_LINK", "URGENCY_THREAT", "COLLECT_TRICK", "PHONE_NUMBER"
    severity: str = "MEDIUM"

class WaterfallStep(BaseModel):
    component: str
    points: float
    running_total: float
    explanation: str

class ScamStoryStep(BaseModel):
    step_number: int
    stage: str  # e.g., "Initial Contact", "Psychological Coercion", "Financial Execution"
    title: str
    description: str
    warning_sign: str

class ScamStoryTimeline(BaseModel):
    category: str
    category_name: str
    overview: str
    steps: List[ScamStoryStep] = []

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
    highlight_spans: List[HighlightSpan] = []
    waterfall: List[WaterfallStep] = []
    scam_story: Optional[ScamStoryTimeline] = None
    prefilled_1930_summary: Optional[Dict[str, Any]] = None
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

class BatchAnalysisRequest(BaseModel):
    items: List[TextAnalysisRequest] = Field(min_length=1, max_length=50)

class BatchAnalysisResponse(BaseModel):
    total_processed: int
    reports: List[SafetyReport]

class VpaAnalysisRequest(BaseModel):
    vpa: str = Field(min_length=3, max_length=100)
    payee_name: Optional[str] = ""
    amount: Optional[float] = None
    note: Optional[str] = ""
    is_collect: bool = False

class VpaAnalysisResponse(BaseModel):
    vpa: str
    handle: str
    provider: str
    is_valid_format: bool
    is_collect_request: bool
    risk_score: int
    verdict: str
    reasons: List[str]
    warning_notice: str

class UserFeedbackRequest(BaseModel):
    analysis_id: Optional[int] = None
    input_text: Optional[str] = ""
    reported_verdict: str
    is_correct: bool
    correct_category: Optional[str] = None
    feedback_notes: Optional[str] = ""

class UserFeedbackResponse(BaseModel):
    id: int
    status: str
    message: str

class AssistantChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    language: str = "en"  # "en", "hi", "te"
    context_report_id: Optional[int] = None
    history: Optional[List[Dict[str, str]]] = None

class AssistantChatResponse(BaseModel):
    reply: str
    language: str
    verdict: Optional[str] = None
    risk_score: Optional[int] = None
    citations: List[RAGCitation] = []
    recommended_actions: List[str] = []
    intent: Optional[str] = None
    quick_replies: List[str] = []
    action_buttons: List[Dict[str, str]] = []

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
    channel_breakdown: Optional[Dict[str, int]] = None

class StudyItemOut(BaseModel):
    item_id: str
    text: str
    language: str

class StudySubmitItem(BaseModel):
    item_id: str
    user_guess: str          # "scam" or "genuine"
    user_confidence: int     # 1 to 5
    would_change: str        # "yes", "no", "already_agreed"
    revised_guess: Optional[str] = None
    clarity_rating: Optional[int] = 5
    feedback: Optional[str] = ""

class StudyBatchSubmit(BaseModel):
    session_id: str
    responses: List[StudySubmitItem]

class CommunityReportCreate(BaseModel):
    entity_type: str        # "vpa", "phone", "url", "domain"
    entity_value: str
    scam_category: str
    evidence_text: Optional[str] = ""

class CommunityDisputeCreate(BaseModel):
    entity_type: str
    entity_value: str
    dispute_reason: str
    contact_email: Optional[str] = ""
