import json
import os
import random
import io
import csv
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.db_models import StudyResponse, User
from ..models.schemas import StudyItemOut, StudyBatchSubmit
from ..detectors.nlp_classifier import nlp_classifier
from ..detectors.rule_engine import rule_engine
from ..detectors.url_scanner import url_scanner
from ..fusion.risk_engine import risk_engine
from ..core.auth import get_current_admin

router = APIRouter(prefix="/study", tags=["User Study"])

POOL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "study_items_pool.json")

def load_pool() -> List[Dict[str, Any]]:
    if os.path.exists(POOL_PATH):
        with open(POOL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.get("/items", response_model=List[StudyItemOut])
def get_study_items():
    """
    Returns 10 randomized items for an anonymous study session.
    Strips ground truth category and labels.
    """
    pool = load_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Study items pool is empty")
    
    # Stratify: 5 scam, 5 legitimate if available
    scams = [item for item in pool if item.get("is_scam", True)]
    legits = [item for item in pool if not item.get("is_scam", False)]
    
    selected_scams = random.sample(scams, min(5, len(scams)))
    selected_legits = random.sample(legits, min(5, len(legits)))
    selected = selected_scams + selected_legits
    random.shuffle(selected)

    return [
        StudyItemOut(
            item_id=item["item_id"],
            text=item["text"],
            language=item.get("language", "en")
        )
        for item in selected
    ]

@router.post("/evaluate-item")
def evaluate_study_item(payload: Dict[str, str]):
    """
    Runs the live tool analysis on a study item and returns the verdict and top evidence.
    """
    text = payload.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text required")

    nlp_res = nlp_classifier.predict(text)
    rule_res = rule_engine.evaluate(text)
    urls = url_scanner.scan_all_urls(text)
    report = risk_engine.fuse("text", text, nlp_res, rule_res, urls)

    top_evidence = [
        {"signal": e.signal, "severity": e.severity, "weight": e.weight}
        for e in report.evidence[:3]
    ]

    return {
        "verdict": report.verdict,
        "risk_score": report.risk_score,
        "detected_category": report.detected_category,
        "confidence": report.confidence,
        "top_evidence": top_evidence,
        "plain_explanation": report.plain_language_explanation,
        "recommended_action": report.recommended_actions[0] if report.recommended_actions else "Verify sender through official channels."
    }

@router.post("/submit")
def submit_study_responses(batch: StudyBatchSubmit, db: Session = Depends(get_db)):
    """
    Submits user responses for an anonymous study session.
    """
    pool = {item["item_id"]: item for item in load_pool()}
    records_added = 0

    for resp in batch.responses:
        item = pool.get(resp.item_id)
        if not item:
            continue

        gt_is_scam = item.get("is_scam", False)
        user_is_scam = (resp.user_guess.lower() == "scam")
        user_init_correct = (user_is_scam == gt_is_scam)

        # Run tool evaluation
        text = item["text"]
        nlp_res = nlp_classifier.predict(text)
        rule_res = rule_engine.evaluate(text)
        urls = url_scanner.scan_all_urls(text)
        rep = risk_engine.fuse("text", text, nlp_res, rule_res, urls)

        tool_is_scam = (rep.verdict in ["SUSPICIOUS", "HIGH RISK"])
        tool_correct = (tool_is_scam == gt_is_scam)

        db_entry = StudyResponse(
            session_id=batch.session_id,
            item_id=resp.item_id,
            message_text=text,
            ground_truth_category=item.get("category", "unknown"),
            ground_truth_is_scam=gt_is_scam,
            language=item.get("language", "en"),
            user_guess=resp.user_guess.lower(),
            user_confidence=resp.user_confidence,
            user_initial_correct=user_init_correct,
            tool_verdict=rep.verdict,
            tool_risk_score=rep.risk_score,
            tool_is_scam=tool_is_scam,
            tool_correct=tool_correct,
            would_change_decision=resp.would_change.lower(),
            user_revised_guess=resp.revised_guess.lower() if resp.revised_guess else resp.user_guess.lower(),
            explanation_clarity=resp.clarity_rating or 5,
            feedback_notes=resp.feedback or ""
        )
        db.add(db_entry)
        records_added += 1

    db.commit()
    return {"status": "SUCCESS", "saved_responses": records_added}

@router.get("/export")
def export_study_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Admin-only CSV export of study responses for academic verification.
    """
    rows = db.query(StudyResponse).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "session_id", "item_id", "language", "ground_truth_category",
        "ground_truth_is_scam", "user_guess", "user_confidence", "user_initial_correct",
        "tool_verdict", "tool_risk_score", "tool_is_scam", "tool_correct",
        "would_change_decision", "user_revised_guess", "explanation_clarity", "created_at"
    ])

    for r in rows:
        writer.writerow([
            r.id, r.session_id, r.item_id, r.language, r.ground_truth_category,
            r.ground_truth_is_scam, r.user_guess, r.user_confidence, r.user_initial_correct,
            r.tool_verdict, r.tool_risk_score, r.tool_is_scam, r.tool_correct,
            r.would_change_decision, r.user_revised_guess, r.explanation_clarity, r.created_at
        ])

    csv_data = output.getvalue()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=user_study_responses.csv"}
    )
