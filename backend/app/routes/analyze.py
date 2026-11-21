import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.db_models import AnalysisHistory, Feedback
from ..models.schemas import (
    TextAnalysisRequest, UrlAnalysisRequest, SafetyReport,
    VpaAnalysisRequest, VpaAnalysisResponse,
    BatchAnalysisRequest, BatchAnalysisResponse,
    UserFeedbackRequest, UserFeedbackResponse
)
from ..detectors.nlp_classifier import nlp_classifier
from ..detectors.rule_engine import rule_engine
from ..detectors.url_scanner import url_scanner
from ..detectors.ocr_pipeline import ocr_pipeline
from ..core.vpa_verifier import vpa_verifier
from ..fusion.risk_engine import risk_engine
from ..core.masking import mask_sensitive_data
from ..core.security import sanitize_text, rate_limiter, ALLOWED_IMAGE_TYPES, MAX_FILE_SIZE_BYTES

router = APIRouter(prefix="/analyze", tags=["Threat Analysis"])

@router.post("/text", response_model=SafetyReport, dependencies=[Depends(rate_limiter)])
def analyze_text(req: TextAnalysisRequest, db: Session = Depends(get_db)):
    raw_text = req.text.strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Text payload cannot be empty")

    # 1. Multi-Layer Detectors
    nlp_res = nlp_classifier.predict(raw_text)
    rule_res = rule_engine.evaluate(raw_text)
    url_res = url_scanner.scan_all_urls(raw_text)

    # 2. Risk Fusion Engine
    report = risk_engine.fuse(
        input_type="text",
        text=raw_text,
        nlp_result=nlp_res,
        rule_result=rule_res,
        url_results=url_res,
        language_override=req.language
    )

    # 3. Privacy Masking
    masked = mask_sensitive_data(raw_text)
    report.masked_input = masked

    # 4. Persistence (if user consented to history logging)
    if req.save_history:
        record = AnalysisHistory(
            input_type="text",
            raw_input_masked=masked,
            verdict=report.verdict,
            risk_score=report.risk_score,
            detected_category=report.detected_category,
            language=report.language,
            evidence_json=json.dumps([e.model_dump() for e in report.evidence]),
            actions_json=json.dumps(report.recommended_actions),
            is_simulated=False
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        report.id = record.id

    return report

@router.post("/url", response_model=SafetyReport, dependencies=[Depends(rate_limiter)])
def analyze_url(req: UrlAnalysisRequest, db: Session = Depends(get_db)):
    url = req.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    # Static analysis
    url_res = [url_scanner.analyze_url(url)]
    rule_res = rule_engine.evaluate(url)
    nlp_res = nlp_classifier.predict(url)

    report = risk_engine.fuse(
        input_type="url",
        text=url,
        nlp_result=nlp_res,
        rule_result=rule_res,
        url_results=url_res
    )

    masked = mask_sensitive_data(url)
    report.masked_input = masked

    if req.save_history:
        record = AnalysisHistory(
            input_type="url",
            raw_input_masked=masked,
            verdict=report.verdict,
            risk_score=report.risk_score,
            detected_category=report.detected_category,
            language=report.language,
            evidence_json=json.dumps([e.model_dump() for e in report.evidence]),
            actions_json=json.dumps(report.recommended_actions),
            is_simulated=False
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        report.id = record.id

    return report

@router.post("/image", response_model=SafetyReport, dependencies=[Depends(rate_limiter)])
async def analyze_image(
    file: UploadFile = File(...),
    save_history: bool = Form(True),
    language: str = Form("auto"),
    db: Session = Depends(get_db)
):
    # Validate MIME type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: {file.content_type}. Allowed: PNG, JPEG, JPG, WEBP"
        )

    image_bytes = await file.read()
    if len(image_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File size exceeds maximum 5MB limit")

    # OCR & QR Pipeline
    ocr_res = ocr_pipeline.process_image(image_bytes)
    if not ocr_res["success"]:
        raise HTTPException(status_code=400, detail=ocr_res.get("error", "Image processing failed"))

    combined_text = ocr_res["combined_text"]
    qr_analysis = ocr_res.get("qr_analysis")

    # Feed extracted content into NLP and URL detectors
    nlp_res = nlp_classifier.predict(combined_text) if combined_text else {"category": "legitimate", "confidence": 0.5, "language": "en"}
    rule_res = rule_engine.evaluate(combined_text) if combined_text else {"matched_rules": [], "rule_score": 0.0, "hard_override_high_risk": False}
    url_res = url_scanner.scan_all_urls(combined_text)

    report = risk_engine.fuse(
        input_type="image",
        text=combined_text,
        nlp_result=nlp_res,
        rule_result=rule_res,
        url_results=url_res,
        qr_result=qr_analysis,
        ocr_result=ocr_res,
        language_override=language
    )

    masked_summary = f"[Image: {file.filename}] " + mask_sensitive_data(combined_text[:300])
    report.masked_input = masked_summary

    if save_history:
        record = AnalysisHistory(
            input_type="image",
            raw_input_masked=masked_summary,
            verdict=report.verdict,
            risk_score=report.risk_score,
            detected_category=report.detected_category,
            language=report.language,
            evidence_json=json.dumps([e.model_dump() for e in report.evidence]),
            actions_json=json.dumps(report.recommended_actions),
            is_simulated=False
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        report.id = record.id

    return report

@router.post("/vpa", response_model=VpaAnalysisResponse, dependencies=[Depends(rate_limiter)])
def analyze_vpa(req: VpaAnalysisRequest):
    """
    Analyzes a UPI VPA (UPI ID), checking handle provider validity,
    brand impersonation, collect request trick indicators, and high amount risks.
    """
    return vpa_verifier.analyze(
        vpa=req.vpa,
        payee_name=req.payee_name,
        amount=req.amount,
        is_collect=req.is_collect
    )

@router.post("/batch", response_model=BatchAnalysisResponse, dependencies=[Depends(rate_limiter)])
def analyze_batch(req: BatchAnalysisRequest, db: Session = Depends(get_db)):
    """
    Batch processes up to 50 text items concurrently, returning individual safety reports.
    """
    reports = []
    for item in req.items:
        raw_text = item.text.strip()
        if not raw_text:
            continue
        nlp_res = nlp_classifier.predict(raw_text)
        rule_res = rule_engine.evaluate(raw_text)
        url_res = url_scanner.scan_all_urls(raw_text)
        rep = risk_engine.fuse(
            input_type="text",
            text=raw_text,
            nlp_result=nlp_res,
            rule_result=rule_res,
            url_results=url_res,
            language_override=item.language
        )
        rep.masked_input = mask_sensitive_data(raw_text)
        reports.append(rep)

    return BatchAnalysisResponse(
        total_processed=len(reports),
        reports=reports
    )

@router.post("/feedback", response_model=UserFeedbackResponse, dependencies=[Depends(rate_limiter)])
def submit_feedback(req: UserFeedbackRequest, db: Session = Depends(get_db)):
    """
    Submits user correction/validation feedback for continuous improvement and retrain audits.
    """
    masked_text = mask_sensitive_data(req.input_text) if req.input_text else None
    feedback_record = Feedback(
        analysis_id=req.analysis_id,
        input_text_masked=masked_text,
        reported_verdict=req.reported_verdict,
        is_correct=req.is_correct,
        correct_category=req.correct_category,
        feedback_notes=req.feedback_notes
    )
    db.add(feedback_record)
    db.commit()
    db.refresh(feedback_record)

    return UserFeedbackResponse(
        id=feedback_record.id,
        status="success",
        message="Feedback logged successfully. Thank you for making UPI Rakshak AI stronger."
    )
