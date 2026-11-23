import json
from collections import Counter, defaultdict
import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db
from ..models.db_models import AnalysisHistory, ThreatReport, Feedback, CommunityReport
from ..models.schemas import DashboardStatsResponse, AdminAlertsResponse, AdminAlertItem

router = APIRouter(prefix="/dashboard", tags=["Admin Intelligence"])

def format_time_ago(dt: datetime.datetime) -> str:
    if not dt:
        return "Just now"
    now = datetime.datetime.utcnow()
    diff = now - dt
    seconds = int(diff.total_seconds())
    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        mins = seconds // 60
        return f"{mins}m ago"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours}h ago"
    else:
        days = seconds // 86400
        return f"{days}d ago"

@router.get("/alerts", response_model=AdminAlertsResponse)
def get_admin_alerts(
    limit: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Fetches live admin incident and user feedback alerts for the Navbar alarm bell and moderation dashboard.
    Combines cases filed (ThreatReport), user feedback (Feedback), and community flags.
    """
    limit_val = 30
    if isinstance(limit, int):
        limit_val = limit
    elif hasattr(limit, 'default') and isinstance(limit.default, int):
        limit_val = limit.default

    threat_records = db.query(ThreatReport).order_by(desc(ThreatReport.created_at)).limit(limit_val).all()
    feedback_records = db.query(Feedback).order_by(desc(Feedback.created_at)).limit(limit_val).all()
    community_records = db.query(CommunityReport).order_by(desc(CommunityReport.created_at)).limit(limit_val).all()

    alerts = []
    cases_count = len(threat_records)
    feedback_count = len(feedback_records)
    unread_count = 0

    for r in threat_records:
        is_pending = (r.status == "PENDING_REVIEW")
        if is_pending:
            unread_count += 1
        alerts.append({
            "id": f"case-{r.id}",
            "source_id": r.id,
            "type": "case_filed",
            "category": r.scam_category,
            "title": f"🚨 Case Filed: {r.scam_category.replace('_', ' ').title()}",
            "content": r.suspicious_content_masked[:120] if r.suspicious_content_masked else "No content preview",
            "comments": r.reporter_comments or "Reported via Consumer Incident Portal",
            "status": r.status or "PENDING_REVIEW",
            "severity": "CRITICAL" if r.scam_category in ["electricity_disconnection", "courier_customs_scam", "remote_access_scam", "digital_arrest"] else "HIGH",
            "created_at": r.created_at.isoformat() if r.created_at else datetime.datetime.utcnow().isoformat(),
            "time_ago": format_time_ago(r.created_at) if r.created_at else "Recently"
        })

    for f in feedback_records:
        is_correction = not f.is_correct
        if is_correction:
            unread_count += 1
        cat_disp = f.correct_category or "Flagged"
        title_text = "Confirmed Safe/Accurate" if f.is_correct else f"Reported Misclassification ({f.reported_verdict} → {cat_disp})"
        alerts.append({
            "id": f"feedback-{f.id}",
            "source_id": f.id,
            "type": "user_feedback",
            "category": f.correct_category or "feedback",
            "title": f"💬 User Feedback: {title_text}",
            "content": f.input_text_masked[:120] if f.input_text_masked else "No input text provided",
            "comments": f.feedback_notes or ("User verified analysis as correct." if f.is_correct else "Correction requested by user"),
            "status": "VERIFIED" if f.is_correct else "NEEDS_AUDIT",
            "severity": "INFO" if f.is_correct else "WARNING",
            "created_at": f.created_at.isoformat() if f.created_at else datetime.datetime.utcnow().isoformat(),
            "time_ago": format_time_ago(f.created_at) if f.created_at else "Recently"
        })

    for c in community_records:
        alerts.append({
            "id": f"comm-{c.id}",
            "source_id": c.id,
            "type": "community_flag",
            "category": c.scam_category,
            "title": f"⚠️ Community Flag: {c.masked_display} ({c.entity_type.upper()})",
            "content": f"Entity flagged as {c.scam_category.replace('_', ' ')}",
            "comments": c.evidence_text or "Crowdsourced reputation report",
            "status": c.status or "ACTIVE",
            "severity": "HIGH",
            "created_at": c.created_at.isoformat() if c.created_at else datetime.datetime.utcnow().isoformat(),
            "time_ago": format_time_ago(c.created_at) if c.created_at else "Recently"
        })

    alerts.sort(key=lambda a: a["created_at"], reverse=True)
    alerts = alerts[:limit_val]

    return AdminAlertsResponse(
        total_alerts=len(alerts),
        unread_count=unread_count,
        cases_count=cases_count,
        feedback_count=feedback_count,
        alerts=alerts
    )

@router.post("/alerts/mark-read")
def mark_admin_alerts_read(db: Session = Depends(get_db)):
    """
    Marks pending threat reports as reviewed to update the alarm status.
    """
    db.query(ThreatReport).filter(ThreatReport.status == "PENDING_REVIEW").update({"status": "REVIEWED"})
    db.commit()
    return {"status": "ok", "message": "All pending alerts marked as reviewed."}

@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    scope: str = Query("all", pattern="^(all|live|simulated)$"),
    data_source: str = Query("live_user", pattern="^(all|live_user|demo_seed|test_traffic)$"),
    db: Session = Depends(get_db)
):
    query = db.query(AnalysisHistory)

    # Prioritize data_source filtering (Phase 2 truthfulness)
    if data_source != "all":
        query = query.filter(AnalysisHistory.data_source == data_source)
    elif scope == "live":
        query = query.filter(AnalysisHistory.data_source == "live_user")
    elif scope == "simulated":
        query = query.filter(AnalysisHistory.data_source.in_(["demo_seed", "test_traffic"]))

    # By default, exclude legacy removed channels unless explicitly viewing all
    if data_source != "all":
        query = query.filter(AnalysisHistory.channel != "legacy_removed")

    all_records = query.all()
    total_analyses = len(all_records)

    safe_count = sum(1 for r in all_records if r.verdict == "SAFE")
    suspicious_count = sum(1 for r in all_records if r.verdict == "SUSPICIOUS")
    high_risk_count = sum(1 for r in all_records if r.verdict == "HIGH RISK")

    # Category distribution
    cat_counter = Counter(r.detected_category for r in all_records)
    category_distribution = dict(cat_counter.most_common(12))

    # Language breakdown
    lang_counter = Counter(r.language for r in all_records)
    language_breakdown = dict(lang_counter)

    # Risk score distribution buckets
    risk_score_dist = {
        "0-34 (Safe)": sum(1 for r in all_records if r.risk_score <= 34),
        "35-69 (Suspicious)": sum(1 for r in all_records if 35 <= r.risk_score <= 69),
        "70-100 (High Risk)": sum(1 for r in all_records if r.risk_score >= 70)
    }

    # Top signals extracted from evidence_json
    signal_counter = Counter()
    signal_severity = {}
    for r in all_records:
        if r.evidence_json:
            try:
                evidence_list = json.loads(r.evidence_json)
                for item in evidence_list:
                    sig = item.get("signal", "")
                    # Shorten signal key for clean charts
                    sig_key = sig.split(":")[0] if ":" in sig else sig[:45]
                    signal_counter[sig_key] += 1
                    signal_severity[sig_key] = item.get("severity", "MEDIUM")
            except Exception:
                pass

    top_signals = [
        {"signal": k, "count": v, "severity": signal_severity.get(k, "MEDIUM")}
        for k, v in signal_counter.most_common(8)
    ]

    # Channel breakdown (Web and Telegram only; legacy_removed excluded)
    channel_counter = Counter(r.channel or "web" for r in all_records if r.channel != "legacy_removed")
    channel_breakdown = {
        "web": channel_counter.get("web", 0),
        "telegram": channel_counter.get("telegram", 0)
    }

    # Timeline trend (last 7 days)
    today = datetime.datetime.utcnow().date()
    trend_dict = defaultdict(lambda: {"safe": 0, "suspicious": 0, "high_risk": 0})
    for i in range(6, -1, -1):
        day_str = (today - datetime.timedelta(days=i)).strftime("%b %d")
        trend_dict[day_str]  # initialize

    for r in all_records:
        if r.created_at:
            day_str = r.created_at.strftime("%b %d")
            if day_str in trend_dict:
                if r.verdict == "SAFE": trend_dict[day_str]["safe"] += 1
                elif r.verdict == "SUSPICIOUS": trend_dict[day_str]["suspicious"] += 1
                elif r.verdict == "HIGH RISK": trend_dict[day_str]["high_risk"] += 1

    timeline_trend = [
        {"date": day, "safe": counts["safe"], "suspicious": counts["suspicious"], "high_risk": counts["high_risk"]}
        for day, counts in trend_dict.items()
    ]

    # Recent analyses matching query filters
    recent_query = db.query(AnalysisHistory)
    if data_source != "all":
        recent_query = recent_query.filter(AnalysisHistory.data_source == data_source, AnalysisHistory.channel != "legacy_removed")
    elif scope == "live":
        recent_query = recent_query.filter(AnalysisHistory.data_source == "live_user", AnalysisHistory.channel != "legacy_removed")
    elif scope == "simulated":
        recent_query = recent_query.filter(AnalysisHistory.data_source.in_(["demo_seed", "test_traffic"]))

    recent_records = recent_query.order_by(desc(AnalysisHistory.created_at)).limit(10).all()
    recent_analyses = [
        {
            "id": r.id,
            "input_type": r.input_type,
            "raw_input_masked": r.raw_input_masked[:70] + ("..." if len(r.raw_input_masked) > 70 else ""),
            "verdict": r.verdict,
            "risk_score": r.risk_score,
            "detected_category": r.detected_category,
            "language": r.language,
            "channel": r.channel or "web",
            "data_source": r.data_source or "live_user",
            "is_simulated": r.is_simulated,
            "created_at": r.created_at.strftime("%H:%M %d-%b") if r.created_at else ""
        }
        for r in recent_records
    ]

    total_threat_reports = db.query(ThreatReport).count()
    live_total = db.query(AnalysisHistory).filter(AnalysisHistory.data_source == "live_user").count()
    sim_total = db.query(AnalysisHistory).filter(AnalysisHistory.data_source.in_(["demo_seed", "test_traffic"])).count()

    return DashboardStatsResponse(
        total_analyses=total_analyses,
        safe_count=safe_count,
        suspicious_count=suspicious_count,
        high_risk_count=high_risk_count,
        category_distribution=category_distribution,
        top_signals=top_signals,
        language_breakdown=language_breakdown,
        risk_score_distribution=risk_score_dist,
        timeline_trend=timeline_trend,
        recent_analyses=recent_analyses,
        total_threat_reports=total_threat_reports,
        seeded_vs_live={"live": live_total, "simulated": sim_total},
        channel_breakdown=channel_breakdown
    )
