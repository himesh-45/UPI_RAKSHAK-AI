import json
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db
from ..models.db_models import AnalysisHistory

router = APIRouter(prefix="/history", tags=["History & Audit"])

@router.get("")
def get_history(
    filter_type: str = Query("all", pattern="^(all|live|simulated)$"),
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(AnalysisHistory)
    if filter_type == "live":
        query = query.filter(AnalysisHistory.is_simulated == False)
    elif filter_type == "simulated":
        query = query.filter(AnalysisHistory.is_simulated == True)

    total = query.count()
    records = query.order_by(desc(AnalysisHistory.created_at)).offset(offset).limit(limit).all()

    items = []
    for r in records:
        items.append({
            "id": r.id,
            "input_type": r.input_type,
            "raw_input_masked": r.raw_input_masked,
            "verdict": r.verdict,
            "risk_score": r.risk_score,
            "detected_category": r.detected_category,
            "language": r.language,
            "is_simulated": r.is_simulated,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "filter": filter_type,
        "items": items
    }
