import datetime
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models.db_models import CommunityReport, CommunityDispute
from backend.app.core.community_reputation import (
    normalize_entity,
    is_immune_entity,
    submit_community_report,
    lookup_community_reputation,
    submit_dispute,
    moderate_report,
    calculate_decay_weight
)
from backend.app.fusion.risk_engine import risk_engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_community_db():
    db = SessionLocal()
    try:
        db.query(CommunityReport).delete()
        db.query(CommunityDispute).delete()
        db.commit()
    finally:
        db.close()
    yield
    db = SessionLocal()
    try:
        db.query(CommunityReport).delete()
        db.query(CommunityDispute).delete()
        db.commit()
    finally:
        db.close()

def test_normalization_and_masking():
    norm_phone, mask_phone = normalize_entity("phone", "+91 98765-43210")
    assert norm_phone == "9876543210"
    assert mask_phone == "98******10"

    norm_vpa, mask_vpa = normalize_entity("vpa", "scammer.fraud@paytm")
    assert norm_vpa == "scammer.fraud@paytm"
    assert mask_vpa == "sc***@paytm"

    norm_url, mask_url = normalize_entity("url", "https://sbi.co.in.fake-kyc.top/verify.php")
    assert norm_url == "fake-kyc.top"
    assert "fake-kyc.top" in mask_url or "fak***.top" in mask_url

def test_anti_poisoning_whitelist():
    # Official bank domains and handles must be immune
    assert is_immune_entity("url", "sbi.co.in") is True
    assert is_immune_entity("domain", "onlinesbi.sbi") is True
    assert is_immune_entity("domain", "hdfcbank.com") is True
    assert is_immune_entity("domain", "cybercrime.gov.in") is True
    assert is_immune_entity("vpa", "pmcares@sbi") is True
    assert is_immune_entity("vpa", "officer@gov.in") is True

    # Malicious domains must NOT be immune
    assert is_immune_entity("url", "sbi-kyc-update.top") is False
    assert is_immune_entity("vpa", "refund-sbi@ybl") is False

    # Attempting to report an immune domain must fail
    res = submit_community_report(
        entity_type="url",
        entity_value="https://www.onlinesbi.sbi",
        scam_category="fake_bank_kyc",
        reporter_id="analyst_1"
    )
    assert res["success"] is False
    assert "immune" in res["error"]

def test_reporter_rate_limiting():
    # First submission succeeds
    r1 = submit_community_report(
        entity_type="vpa",
        entity_value="evil-phisher@paytm",
        scam_category="collect_request_fraud",
        reporter_id="user_ip_111"
    )
    assert r1["success"] is True

    # Immediate second submission by same reporter on same entity must be blocked
    r2 = submit_community_report(
        entity_type="vpa",
        entity_value="evil-phisher@paytm",
        scam_category="collect_request_fraud",
        reporter_id="user_ip_111"
    )
    assert r2["success"] is False
    assert "24 hours" in r2["error"]

def test_consensus_gating_minimum_two_reporters():
    test_vpa = "fraudster-urgent@ybl"

    # Step 1: Exactly 1 reporter flags it
    submit_community_report(
        entity_type="vpa",
        entity_value=test_vpa,
        scam_category="collect_request_fraud",
        reporter_id="reporter_alpha"
    )

    lookup_1 = lookup_community_reputation("vpa", test_vpa)
    assert lookup_1["consensus_reached"] is False
    assert lookup_1["reputation_status"] == "PENDING_CONSENSUS"
    assert lookup_1["fusion_points"] == 0.0

    # Step 2: Second independent reporter flags it
    submit_community_report(
        entity_type="vpa",
        entity_value=test_vpa,
        scam_category="collect_request_fraud",
        reporter_id="reporter_beta"
    )

    lookup_2 = lookup_community_reputation("vpa", test_vpa)
    assert lookup_2["consensus_reached"] is True
    assert lookup_2["distinct_reporters"] == 2
    assert lookup_2["fusion_points"] > 0.0
    assert lookup_2["fusion_points"] <= 15.0

def test_recency_decay_calculation():
    now = datetime.datetime.utcnow()
    # Today's report -> weight ~ 1.0
    w_today = calculate_decay_weight(now)
    assert 0.99 <= w_today <= 1.0

    # 30-day-old report -> weight ~ 0.5
    w_30d = calculate_decay_weight(now - datetime.timedelta(days=30))
    assert 0.49 <= w_30d <= 0.51

    # 60-day-old report -> weight ~ 0.25
    w_60d = calculate_decay_weight(now - datetime.timedelta(days=60))
    assert 0.24 <= w_60d <= 0.26

def test_capped_fusion_impact_cannot_trigger_high_risk():
    test_phone = "9876500000"

    # Seed 5 distinct community reports for this phone
    for i in range(5):
        submit_community_report(
            entity_type="phone",
            entity_value=test_phone,
            scam_category="fake_customer_support",
            reporter_id=f"reporter_num_{i}"
        )

    # Completely benign, non-scam message that merely mentions the phone number
    benign_text = f"Hi Mom, I bought groceries. My delivery driver called from {test_phone}."

    report = risk_engine.fuse(
        input_type="text",
        text=benign_text,
        nlp_result={"category": "legitimate", "confidence": 0.95, "language": "en"},
        rule_result={"matched_rules": [], "rule_score": 0.0, "hard_override_high_risk": False, "is_genuine_alert": False},
        url_results=[]
    )

    # Assert community evidence was extracted
    community_ev = [e for e in report.evidence if e.source_module == "COMMUNITY_REPUTATION"]
    assert len(community_ev) >= 1
    assert community_ev[0].weight <= 15.0

    # Critical Security Guarantee: Community reputation alone CANNOT trigger HIGH RISK
    # It can only raise the verdict from SAFE to at most SUSPICIOUS (<= 49)
    assert report.verdict != "HIGH RISK"
    assert report.risk_score <= 49

def test_dispute_and_admin_moderation():
    test_vpa = "innocent-store@okhdfcbank"

    # Seed 2 reports so it reaches consensus
    submit_community_report("vpa", test_vpa, "marketplace_qr_scam", "user_1")
    submit_community_report("vpa", test_vpa, "marketplace_qr_scam", "user_2")

    before_dispute = lookup_community_reputation("vpa", test_vpa)
    assert before_dispute["consensus_reached"] is True

    # Public dispute submission
    disp = submit_dispute(
        entity_type="vpa",
        entity_value=test_vpa,
        claimant_email="merchant@innocentstore.com",
        dispute_reason="We are a verified merchant. Our competitors submitted fraudulent flags.",
        proof_url="https://innocentstore.com/gst-certificate.pdf"
    )
    assert disp["success"] is True

    # Admin moderates and dismisses the false reports
    db = SessionLocal()
    try:
        report_row = db.query(CommunityReport).filter(CommunityReport.entity_type == "vpa").first()
        assert report_row is not None
        mod_success = moderate_report(report_row.id, "DISMISS")
        assert mod_success is True
    finally:
        db.close()

    # After dismissal, active consensus drops below threshold
    after_dismissal = lookup_community_reputation("vpa", test_vpa)
    assert after_dismissal["consensus_reached"] is False
