import os
import re
import math
import hashlib
import datetime
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import Session
import tldextract
from ..config import settings
from ..database import SessionLocal
from ..models.db_models import CommunityReport, CommunityDispute

# Anti-Poisoning Whitelist: Official Bank & Government Domains and VPAs
IMMUNE_DOMAINS = {
    "sbi.co.in", "onlinesbi.sbi", "hdfcbank.com", "icicibank.com", "axisbank.com",
    "pnbindia.in", "bankofbaroda.in", "canarabank.com", "kotak.com", "indusind.com",
    "paytm.com", "phonepe.com", "bhimupi.org.in", "npci.org.in", "cybercrime.gov.in",
    "rbi.org.in", "uidai.gov.in", "incometax.gov.in", "gov.in", "nic.in"
}

IMMUNE_VPAS = {
    "pmcares@sbi", "pmcares@hdfcbank", "swiggy@icici", "zomato@hdfcbank",
    "airtel@sbi", "jio@icici", "irctc@sbi", "tneb@indianbank", "electricity@axis"
}

HALF_LIFE_DAYS = 30.0
MIN_REPORTERS_THRESHOLD = 2
MAX_COMMUNITY_FUSION_POINTS = 15.0

def normalize_entity(entity_type: str, raw_value: str) -> Tuple[str, str]:
    """
    Normalizes the entity and generates a privacy-preserving display mask.
    Returns (normalized_clean_value, masked_display).
    """
    val = raw_value.strip().lower()
    entity_type = entity_type.lower()

    if entity_type == "phone":
        # Extract last 10 digits
        digits = re.sub(r'\D', '', val)
        if len(digits) >= 10:
            norm = digits[-10:]
            masked = norm[:2] + "******" + norm[-2:]
            return norm, masked
        return digits, digits[:2] + "****" if len(digits) >= 4 else "****"

    elif entity_type == "vpa":
        norm = val
        if "@" in norm:
            user, handle = norm.split("@", 1)
            masked_user = user[:2] + "***" if len(user) > 2 else "***"
            masked = f"{masked_user}@{handle}"
        else:
            masked = norm[:3] + "***"
        return norm, masked

    elif entity_type in ["url", "domain"]:
        extracted = tldextract.extract(val)
        if extracted.registered_domain:
            norm = extracted.registered_domain.lower()
        else:
            norm = re.sub(r'^https?://', '', val).split('/')[0].lower()
        parts = norm.split('.')
        masked = parts[0][:3] + "***." + ".".join(parts[1:]) if len(parts) > 1 else norm[:3] + "***"
        return norm, masked

    return val, val[:3] + "***"

def hash_entity(entity_type: str, normalized_val: str) -> str:
    """
    Computes a deterministic SHA-256 hash of (entity_type + normalized_val).
    """
    payload = f"{entity_type.lower()}:{normalized_val}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

def hash_reporter(reporter_id: str) -> str:
    """
    Computes a salted SHA-256 hash of the reporter's IP / account ID.
    """
    salt = settings.SENDER_HASH_SALT.encode("utf-8")
    payload = reporter_id.strip().encode("utf-8")
    return hashlib.sha256(salt + payload).hexdigest()

def is_immune_entity(entity_type: str, normalized_val: str) -> bool:
    """
    Strict anti-poisoning check: protects critical national infrastructure,
    official banks, and public utilities from frivolous or malicious reporting.
    """
    if entity_type in ["url", "domain"]:
        for d in IMMUNE_DOMAINS:
            if normalized_val == d or normalized_val.endswith("." + d):
                return True
    elif entity_type == "vpa":
        if normalized_val in IMMUNE_VPAS:
            return True
        # Check if handle belongs to official government domain
        if normalized_val.endswith("@gov.in") or normalized_val.endswith("@nic.in"):
            return True
    return False

def calculate_decay_weight(created_at: datetime.datetime) -> float:
    """
    Exponential recency decay with a 30-day half-life: w(d) = 2^(-d / 30).
    A report from today has weight 1.0; 30 days ago has weight 0.5; 60 days ago has 0.25.
    """
    age_days = (datetime.datetime.utcnow() - created_at).total_seconds() / 86400.0
    if age_days < 0:
        age_days = 0
    return math.pow(0.5, age_days / HALF_LIFE_DAYS)

def submit_community_report(
    entity_type: str,
    entity_value: str,
    scam_category: str,
    reporter_id: str,
    evidence_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    Submits a user or analyst community report with anti-poisoning validation
    and 24-hour reporter rate limiting.
    """
    norm_val, masked_display = normalize_entity(entity_type, entity_value)
    
    # Anti-Poisoning Check
    if is_immune_entity(entity_type, norm_val):
        return {
            "success": False,
            "error": "This entity is an authorized bank or government asset and is immune from community flags."
        }

    ent_hash = hash_entity(entity_type, norm_val)
    rep_hash = hash_reporter(reporter_id)

    db = SessionLocal()
    try:
        # Rate limit: 1 report per entity per reporter per 24 hours
        one_day_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
        recent_report = db.query(CommunityReport).filter(
            CommunityReport.entity_hash == ent_hash,
            CommunityReport.reporter_hash == rep_hash,
            CommunityReport.created_at >= one_day_ago
        ).first()

        if recent_report:
            return {
                "success": False,
                "error": "You have already submitted a report for this entity within the last 24 hours."
            }

        report = CommunityReport(
            entity_type=entity_type.lower(),
            entity_hash=ent_hash,
            masked_display=masked_display,
            reporter_hash=rep_hash,
            scam_category=scam_category,
            evidence_text=evidence_text,
            status="ACTIVE"
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        return {
            "success": True,
            "report_id": report.id,
            "masked_display": masked_display,
            "message": "Report recorded. Consensus updates automatically as independent reports arrive."
        }
    finally:
        db.close()

def lookup_community_reputation(entity_type: str, entity_value: str) -> Dict[str, Any]:
    """
    Evaluates community reputation for a given entity with recency decay
    and multi-reporter consensus gating.
    """
    norm_val, masked_display = normalize_entity(entity_type, entity_value)
    if is_immune_entity(entity_type, norm_val):
        return {
            "entity_type": entity_type,
            "masked_display": masked_display,
            "reputation_status": "WHITELISTED",
            "reputation_score": 0.0,
            "fusion_points": 0.0,
            "report_count": 0,
            "distinct_reporters": 0,
            "consensus_reached": False
        }

    ent_hash = hash_entity(entity_type, norm_val)

    db = SessionLocal()
    try:
        reports = db.query(CommunityReport).filter(
            CommunityReport.entity_hash == ent_hash,
            CommunityReport.status == "ACTIVE"
        ).all()

        if not reports:
            return {
                "entity_type": entity_type,
                "masked_display": masked_display,
                "reputation_status": "CLEAN",
                "reputation_score": 0.0,
                "fusion_points": 0.0,
                "report_count": 0,
                "distinct_reporters": 0,
                "consensus_reached": False
            }

        distinct_reporters = len(set(r.reporter_hash for r in reports))
        total_reports = len(reports)

        # Gate: minimum 2 distinct reporters required
        if distinct_reporters < MIN_REPORTERS_THRESHOLD:
            return {
                "entity_type": entity_type,
                "masked_display": masked_display,
                "reputation_status": "PENDING_CONSENSUS",
                "reputation_score": 0.0,
                "fusion_points": 0.0,
                "report_count": total_reports,
                "distinct_reporters": distinct_reporters,
                "consensus_reached": False,
                "note": f"Flagged by 1 reporter; requires at least {MIN_REPORTERS_THRESHOLD} distinct reporters before affecting risk scores."
            }

        # Calculate time-decayed consensus score
        decayed_sum = sum(calculate_decay_weight(r.created_at) for r in reports)
        # Scaled reputation score (0 to 100)
        reputation_score = min(100.0, round(decayed_sum * 25.0, 1))

        # Strictly capped fusion points: max +15.0
        fusion_points = min(MAX_COMMUNITY_FUSION_POINTS, round(reputation_score * 0.15, 1))

        categories = [r.scam_category for r in reports]
        most_common_category = max(set(categories), key=categories.count) if categories else "suspicious_entity"

        return {
            "entity_type": entity_type,
            "masked_display": masked_display,
            "reputation_status": "KNOWN_SCAM" if reputation_score >= 60 else "SUSPICIOUS",
            "reputation_score": reputation_score,
            "fusion_points": fusion_points,
            "report_count": total_reports,
            "distinct_reporters": distinct_reporters,
            "consensus_reached": True,
            "primary_category": most_common_category
        }
    finally:
        db.close()

def submit_dispute(
    entity_type: str,
    entity_value: str,
    claimant_email: str,
    dispute_reason: str,
    proof_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Submits a public dispute for an entity flagged in the reputation database.
    """
    norm_val, masked_display = normalize_entity(entity_type, entity_value)
    ent_hash = hash_entity(entity_type, norm_val)
    claimant_hash = hash_reporter(claimant_email)
    masked_email = claimant_email[:2] + "****@" + claimant_email.split("@")[-1] if "@" in claimant_email else "****"

    db = SessionLocal()
    try:
        dispute = CommunityDispute(
            entity_hash=ent_hash,
            claimant_email_masked=masked_email,
            claimant_hash=claimant_hash,
            dispute_reason=dispute_reason,
            proof_url=proof_url,
            status="PENDING"
        )
        db.add(dispute)
        db.commit()
        db.refresh(dispute)
        return {
            "success": True,
            "dispute_id": dispute.id,
            "message": "Dispute filed successfully and queued for administrative review."
        }
    finally:
        db.close()

def moderate_report(
    report_id: int,
    action: str  # "DISMISS" or "CONFIRM"
) -> bool:
    """
    Administrative moderation action to resolve disputed or false flags.
    """
    db = SessionLocal()
    try:
        report = db.query(CommunityReport).filter(CommunityReport.id == report_id).first()
        if not report:
            return False
        if action == "DISMISS":
            report.status = "DISMISSED"
        elif action == "CONFIRM":
            report.status = "CONFIRMED"
        db.commit()
        return True
    finally:
        db.close()
