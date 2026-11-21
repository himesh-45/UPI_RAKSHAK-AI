from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.db_models import ThreatReport
from ..models.schemas import ThreatReportCreate, ThreatReportResponse
from ..core.masking import mask_sensitive_data
from ..core.security import sanitize_text, rate_limiter

router = APIRouter(prefix="/report", tags=["Threat Reporting"])

@router.post("", response_model=ThreatReportResponse, dependencies=[Depends(rate_limiter)])
def submit_threat_report(req: ThreatReportCreate, db: Session = Depends(get_db)):
    content_masked = mask_sensitive_data(req.suspicious_content.strip())
    contact_masked = mask_sensitive_data(req.contact.strip()) if req.contact else None
    
    report = ThreatReport(
        analysis_id=req.analysis_id,
        input_type=req.input_type,
        suspicious_content_masked=content_masked,
        scam_category=sanitize_text(req.scam_category),
        reporter_comments=sanitize_text(req.comments) if req.comments else None,
        reporter_contact_masked=contact_masked,
        is_simulated=False,
        status="PENDING_REVIEW"
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return ThreatReportResponse(
        id=report.id,
        status=report.status,
        message="Thank you! Your threat report has been recorded for intelligence analysis."
    )
