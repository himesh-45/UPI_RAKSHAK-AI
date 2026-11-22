import json
from collections import Counter, defaultdict
import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db
from ..models.db_models import AnalysisHistory, ThreatReport
from ..models.schemas import DashboardStatsResponse

router = APIRouter(prefix="/dashboard", tags=["Admin Intelligence"])

@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    scope: str = Query("all", pattern="^(all|live|simulated)$"),
    db: Session = Depends(get_db)
):
    query = db.query(AnalysisHistory)
    if scope == "live":
        query = query.filter(AnalysisHistory.is_simulated == False)
    elif scope == "simulated":
        query = query.filter(AnalysisHistory.is_simulated == True)

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

    # Channel breakdown (web vs telegram vs whatsapp)
    channel_counter = Counter(r.channel or "web" for r in all_records)
    channel_breakdown = {
        "web": channel_counter.get("web", 0),
        "telegram": channel_counter.get("telegram", 0),
        "whatsapp": channel_counter.get("whatsapp", 0)
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

    # Recent analyses
    recent_query = db.query(AnalysisHistory)
    if scope == "live":
        recent_query = recent_query.filter(AnalysisHistory.is_simulated == False)
    elif scope == "simulated":
        recent_query = recent_query.filter(AnalysisHistory.is_simulated == True)
    
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
            "is_simulated": r.is_simulated,
            "created_at": r.created_at.strftime("%H:%M %d-%b") if r.created_at else ""
        }
        for r in recent_records
    ]

    total_threat_reports = db.query(ThreatReport).count()
    live_total = db.query(AnalysisHistory).filter(AnalysisHistory.is_simulated == False).count()
    sim_total = db.query(AnalysisHistory).filter(AnalysisHistory.is_simulated == True).count()

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
