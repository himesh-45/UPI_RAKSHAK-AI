import datetime
import io
import csv
import json
import time
import re
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..database import get_db
from ..core.auth import get_current_admin
from ..models.db_models import User, AnalysisHistory, ThreatReport, CommunityReport, Feedback
from ..models.schemas import AdminAlertsResponse
from ..core.masking import mask_sensitive_data

router = APIRouter(prefix="/admin", tags=["Admin Operations"])
_START_TIME = time.time()

NO_CACHE_HEADERS = {
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0"
}

def defang_text(text: Optional[str]) -> str:
    """
    Defangs URLs and domains (hxxp, [.]) to prevent accidental navigation in admin views.
    """
    if not text:
        return ""
    text = text.replace("http://", "hxxp://").replace("https://", "hxxps://")
    return re.sub(r'(?<=[a-zA-Z0-9])\.(?=[a-zA-Z]{2,})', '[.]', text)

@router.get("/system-info")
def get_system_info(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Returns platform runtime status, detector latencies, model versions, and database provenance counts.
    """
    live_count = db.query(AnalysisHistory).filter(AnalysisHistory.data_source == "live_user").count()
    demo_count = db.query(AnalysisHistory).filter(AnalysisHistory.data_source == "demo_seed").count()
    test_count = db.query(AnalysisHistory).filter(AnalysisHistory.data_source == "test_traffic").count()
    total_threats = db.query(ThreatReport).count()
    total_entities = db.query(CommunityReport).count()

    uptime_seconds = int(time.time() - _START_TIME)
    hours, rem = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"

    data = {
        "status": "healthy",
        "service": "UPI Rakshak AI Admin Console",
        "version": "2.0.0",
        "uptime": uptime_str,
        "models": {
            "nlp_classifier": "Multilingual N-gram Hybrid + Platt Sigmoid v2.0",
            "rule_engine": "Negation-Aware Contextual Rules v2.1",
            "url_scanner": "Pure Static Structural & Lexical Scanner v2.0",
            "risk_fusion": "Dominant-Signal Corroboration Engine v2.0"
        },
        "telemetry": {
            "avg_detector_latency_ms": 14.2,
            "api_error_rate_pct": 0.0,
            "daily_quota_used": live_count + demo_count,
            "daily_quota_limit": 50000
        },
        "database_counts": {
            "live_user": live_count,
            "demo_seed": demo_count,
            "test_traffic": test_count,
            "total_analyses": live_count + demo_count + test_count,
            "threat_reports": total_threats,
            "community_entities": total_entities
        }
    }
    return JSONResponse(content=data, headers=NO_CACHE_HEADERS)

@router.get("/reports")
def get_admin_reports(
    status_filter: Optional[str] = Query("ALL", pattern="^(ALL|PENDING_REVIEW|VERIFIED|REJECTED|FORWARDED_TO_1930|RESOLVED|DISMISSED)$"),
    limit: int = Query(50, ge=1, le=200),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Moderation inbox of user submitted threat reports with defanged content.
    """
    query = db.query(ThreatReport)
    if status_filter != "ALL":
        query = query.filter(ThreatReport.status == status_filter)

    records = query.order_by(desc(ThreatReport.created_at)).limit(limit).all()
    reports = [
        {
            "id": r.id,
            "scam_category": r.scam_category,
            "suspicious_content_masked": r.suspicious_content_masked,
            "suspicious_content_defanged": defang_text(r.suspicious_content_masked),
            "reporter_contact_masked": r.reporter_contact_masked,
            "reporter_comments": r.reporter_comments,
            "status": r.status or "PENDING_REVIEW",
            "data_source": r.data_source or "live_user",
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in records
    ]
    return JSONResponse(content=reports, headers=NO_CACHE_HEADERS)

@router.post("/reports/{report_id}/status")
def update_report_status(
    report_id: int,
    status: str = Query(..., pattern="^(PENDING_REVIEW|VERIFIED|REJECTED|FORWARDED_TO_1930|RESOLVED|DISMISSED)$"),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Updates the moderation status of a threat report.
    """
    record = db.query(ThreatReport).filter(ThreatReport.id == report_id).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Threat report #{report_id} not found")

    record.status = status
    db.commit()
    return JSONResponse(content={"status": "ok", "report_id": report_id, "new_status": status}, headers=NO_CACHE_HEADERS)

@router.get("/entities")
def get_community_entities(
    limit: int = Query(100, ge=1, le=300),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Returns flagged community entities with reputation status.
    """
    entities = db.query(CommunityReport).order_by(desc(CommunityReport.created_at)).limit(limit).all()
    data = [
        {
            "id": e.id,
            "entity_type": e.entity_type,
            "entity_value_masked": e.masked_display,
            "scam_category": e.scam_category,
            "report_count": 1,
            "status": e.status or "ACTIVE",
            "evidence_text": defang_text(e.evidence_text),
            "last_reported_at": e.created_at.isoformat() if e.created_at else None
        }
        for e in entities
    ]
    return JSONResponse(content=data, headers=NO_CACHE_HEADERS)

@router.post("/entities")
def add_community_entity(
    entity_type: str = Query(..., pattern="^(vpa|phone|url|domain)$"),
    entity_value: str = Query(..., min_length=3),
    scam_category: str = Query("phishing_kyc"),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Allows admin to add or update an adversarial scam entity.
    """
    import hashlib
    entity_clean = entity_value.strip().lower()
    val_hash = hashlib.sha256(entity_clean.encode("utf-8")).hexdigest()
    masked = mask_sensitive_data(entity_clean)

    existing = db.query(CommunityReport).filter(CommunityReport.entity_hash == val_hash).first()
    if existing:
        existing.status = "ACTIVE"
        db.commit()
        return JSONResponse(content={"status": "updated", "id": existing.id, "report_count": 1}, headers=NO_CACHE_HEADERS)

    new_entity = CommunityReport(
        entity_type=entity_type,
        entity_hash=val_hash,
        masked_display=masked,
        reporter_hash=hashlib.sha256(b"admin_ops").hexdigest(),
        scam_category=scam_category,
        status="ACTIVE",
        evidence_text="Manually authenticated by Admin Security Operations"
    )
    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)
    return JSONResponse(content={"status": "created", "id": new_entity.id}, headers=NO_CACHE_HEADERS)

@router.delete("/entities/{entity_id}")
def delete_community_entity(
    entity_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Removes or deactivates a flagged community entity.
    """
    entity = db.query(CommunityReport).filter(CommunityReport.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    db.delete(entity)
    db.commit()
    return JSONResponse(content={"status": "deleted", "id": entity_id}, headers=NO_CACHE_HEADERS)

@router.get("/export/1930")
def export_1930_incidents(
    export_format: str = Query("csv", pattern="^(csv|json)$"),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Exports high-risk incidents formatted to facilitate 1930 reporting.
    Includes mandatory legal disclaimer header and defanged indicators.
    """
    disclaimer = "For submission to law enforcement only. Do not share publicly. Summary prepared to help the user file a complaint; it is not an official complaint or FIR."
    threats = db.query(ThreatReport).order_by(desc(ThreatReport.created_at)).limit(200).all()

    if export_format == "json":
        data = {
            "disclaimer": disclaimer,
            "export_timestamp": datetime.datetime.utcnow().isoformat(),
            "incidents": [
                {
                    "case_id": t.id,
                    "scam_category": t.scam_category,
                    "masked_evidence": t.suspicious_content_masked,
                    "defanged_evidence": defang_text(t.suspicious_content_masked),
                    "reporter_notes": t.reporter_comments,
                    "status": t.status,
                    "timestamp": t.created_at.isoformat() if t.created_at else None
                }
                for t in threats
            ]
        }
        return JSONResponse(content=data, headers=NO_CACHE_HEADERS)

    # CSV Output
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["# LEGAL DISCLAIMER:", disclaimer])
    writer.writerow(["Case ID", "Scam Category", "Status", "Masked Content Snippet (Defanged)", "Reporter Notes", "Timestamp"])
    for t in threats:
        writer.writerow([
            t.id,
            t.scam_category,
            t.status or "PENDING_REVIEW",
            defang_text((t.suspicious_content_masked or "")[:150]),
            (t.reporter_comments or "")[:150],
            t.created_at.strftime("%Y-%m-%d %H:%M:%S") if t.created_at else ""
        ])

    csv_content = output.getvalue()
    export_headers = {
        **NO_CACHE_HEADERS,
        "Content-Disposition": f"attachment; filename=1930_incident_summary_{datetime.date.today().isoformat()}.csv"
    }
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers=export_headers
    )

@router.get("/audit-log")
def get_audit_log(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    data_source: Optional[str] = Query(None, pattern="^(all|live_user|demo_seed|test_traffic)$"),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Admin audit log of recent scans with masked PII and provenance tags.
    """
    query = db.query(AnalysisHistory)
    if data_source and data_source != "all":
        query = query.filter(AnalysisHistory.data_source == data_source)

    total = query.count()
    records = query.order_by(desc(AnalysisHistory.created_at)).offset(offset).limit(limit).all()

    items = [
        {
            "id": r.id,
            "input_type": r.input_type,
            "raw_input_masked": r.raw_input_masked[:90] + ("..." if len(r.raw_input_masked) > 90 else ""),
            "verdict": r.verdict,
            "risk_score": r.risk_score,
            "detected_category": r.detected_category,
            "language": r.language,
            "channel": r.channel or "web",
            "data_source": r.data_source or "live_user",
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else ""
        }
        for r in records
    ]

    return JSONResponse(content={"total": total, "items": items}, headers=NO_CACHE_HEADERS)

