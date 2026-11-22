from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.db_models import CommunityReport, CommunityDispute, User
from ..core.auth import get_current_admin
from ..core.community_reputation import (
    submit_community_report,
    lookup_community_reputation,
    submit_dispute,
    moderate_report
)

router = APIRouter(prefix="/reputation", tags=["Community Reputation"])

class ReputationReportRequest(BaseModel):
    entity_type: str = Field(..., description="'vpa', 'phone', or 'url'")
    entity_value: str = Field(..., min_length=3)
    scam_category: str = Field(..., description="Suspected fraud category")
    evidence_text: Optional[str] = None

class ReputationDisputeRequest(BaseModel):
    entity_type: str = Field(..., description="'vpa', 'phone', or 'url'")
    entity_value: str = Field(..., min_length=3)
    claimant_email: str = Field(..., min_length=5)
    dispute_reason: str = Field(..., min_length=10)
    proof_url: Optional[str] = None

class ModerationActionRequest(BaseModel):
    report_id: int
    action: str = Field(..., description="'DISMISS' or 'CONFIRM'")

@router.post("/report")
def report_scam_entity(
    req: ReputationReportRequest,
    request: Request
):
    """
    Submits a community scam report for a suspicious VPA, phone number, or URL.
    Enforces anti-poisoning whitelist checks and 24h reporter rate limiting.
    """
    client_ip = request.client.host if request.client else "127.0.0.1"
    res = submit_community_report(
        entity_type=req.entity_type,
        entity_value=req.entity_value,
        scam_category=req.scam_category,
        reporter_id=client_ip,
        evidence_text=req.evidence_text
    )
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error", "Failed to submit report"))
    return res

@router.get("/lookup")
def lookup_entity_reputation(
    entity_type: str = Query(..., pattern="^(vpa|phone|url|domain)$"),
    entity_value: str = Query(..., min_length=2)
):
    """
    Public lookup for community reputation score, consensus status, and report count.
    """
    return lookup_community_reputation(entity_type, entity_value)

@router.post("/dispute")
def file_reputation_dispute(req: ReputationDisputeRequest):
    """
    Public dispute submission for legitimate merchants or consumers to appeal false flags.
    """
    res = submit_dispute(
        entity_type=req.entity_type,
        entity_value=req.entity_value,
        claimant_email=req.claimant_email,
        dispute_reason=req.dispute_reason,
        proof_url=req.proof_url
    )
    return res

@router.get("/admin/pending")
def get_pending_moderation_items(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Admin-only list of active reports and pending disputes for human review.
    """
    reports = db.query(CommunityReport).filter(CommunityReport.status == "ACTIVE").order_by(CommunityReport.created_at.desc()).limit(50).all()
    disputes = db.query(CommunityDispute).filter(CommunityDispute.status == "PENDING").order_by(CommunityDispute.created_at.desc()).limit(50).all()

    return {
        "active_reports": [
            {
                "id": r.id,
                "entity_type": r.entity_type,
                "masked_display": r.masked_display,
                "scam_category": r.scam_category,
                "evidence_text": r.evidence_text,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in reports
        ],
        "pending_disputes": [
            {
                "id": d.id,
                "claimant_email_masked": d.claimant_email_masked,
                "dispute_reason": d.dispute_reason,
                "proof_url": d.proof_url,
                "created_at": d.created_at.isoformat() if d.created_at else None
            }
            for d in disputes
        ]
    }

@router.post("/admin/resolve")
def resolve_moderation_action(
    req: ModerationActionRequest,
    current_admin: User = Depends(get_current_admin)
):
    """
    Admin-only moderation action to CONFIRM or DISMISS a community report.
    """
    if req.action not in ["DISMISS", "CONFIRM"]:
        raise HTTPException(status_code=400, detail="Invalid action. Must be 'DISMISS' or 'CONFIRM'")
    
    success = moderate_report(req.report_id, req.action)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"success": True, "report_id": req.report_id, "new_status": req.action}
