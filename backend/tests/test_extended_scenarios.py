import pytest
import io
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.normalizer import text_normalizer
from backend.app.core.vpa_verifier import vpa_verifier
from backend.app.core.masking import mask_sensitive_data
from backend.app.rag.retriever import rag_retriever
from backend.app.detectors.nlp_classifier import nlp_classifier
from backend.app.detectors.rule_engine import rule_engine
from backend.app.detectors.url_scanner import url_scanner
from backend.app.fusion.risk_engine import risk_engine
from backend.app.scripts.retrain_from_feedback import audit_and_export_feedback

client = TestClient(app)

# 1. New Scam Category Tests
def test_category_job_investment_scam():
    text = "Work from home! Earn Rs. 3500 daily by liking YouTube videos. Deposit Rs. 5000 in Telegram VIP crypto task group: https://t.me/crypto_vip_task"
    res = client.post("/api/analyze/text", json={"text": text})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] in ["HIGH RISK", "SUSPICIOUS"]
    assert data["risk_score"] >= 35

def test_category_loan_app_extortion():
    text = "Instant 10,000 loan approved without collateral! Grant Contacts permission or we will leak your gallery photos to contacts."
    res = client.post("/api/analyze/text", json={"text": text})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] in ["HIGH RISK", "SUSPICIOUS"]

def test_category_courier_digital_arrest():
    text = "FedEx Customs Mumbai: Your package contains MDMA narcotics and fake passports. Call CBI Skype officer immediately to avoid arrest."
    res = client.post("/api/analyze/text", json={"text": text})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] in ["HIGH RISK", "SUSPICIOUS"]
    assert data["risk_score"] >= 60

def test_category_marketplace_qr_scam():
    text = "I am an Indian Army soldier interested in your OLX sofa. Scan this UPI QR code to receive Rs. 15,000 advance payment."
    res = client.post("/api/analyze/text", json={"text": text})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] in ["HIGH RISK", "SUSPICIOUS"]

def test_category_accidental_transfer_trap():
    text = "I accidentally transferred Rs. 5,000 to your Google Pay number. Please return it urgently to my other UPI ID 9876543210@ybl."
    res = client.post("/api/analyze/text", json={"text": text})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] in ["HIGH RISK", "SUSPICIOUS"]

def test_category_remote_access_scam():
    text = "Bank technical support: Install AnyDesk or TeamViewer QuickSupport app and read the 9-digit code to unblock your account."
    res = client.post("/api/analyze/text", json={"text": text})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] == "HIGH RISK"
    assert data["risk_score"] >= 70

def test_category_collect_request_pin_fraud():
    text = "Electricity Board: Approve this UPI collect request of Rs. 2,499 and enter your UPI PIN to process your refund."
    res = client.post("/api/analyze/text", json={"text": text})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] in ["HIGH RISK", "SUSPICIOUS"]

# 2. VPA Verifier Specialized Scenarios
def test_vpa_verifier_valid_consumer_handles():
    handles = ["test@okhdfcbank", "user@okaxis", "merchant@paytm", "person@ybl", "biz@oksbi"]
    for h in handles:
        res = vpa_verifier.analyze(h)
        assert res.is_valid_format is True
        assert res.verdict in ["SAFE", "SUSPICIOUS"]

def test_vpa_verifier_impersonation_detection():
    impersonators = [
        ("sbi-kyc-care@okhdfcbank", "SBI Helpline"),
        ("electricity-refund@ybl", "Electricity Board"),
        ("police-cyber-cell@paytm", "Cyber Police Dept")
    ]
    for vpa, name in impersonators:
        res = vpa_verifier.analyze(vpa, payee_name=name)
        assert res.risk_score >= 40
        assert res.verdict in ["SUSPICIOUS", "HIGH RISK"]

def test_vpa_verifier_high_amount_alert():
    res = vpa_verifier.analyze("random@okhdfcbank", amount=50000.0)
    assert any("High-Value Transaction" in r for r in res.reasons)

def test_vpa_verifier_empty_and_null_strings():
    res = vpa_verifier.analyze("   ")
    assert res.is_valid_format is False
    assert res.verdict == "HIGH RISK"

# 3. Normalizer Properties & Edge Cases
def test_normalizer_handles_emojis_and_special_chars():
    dirty = "🚨 URGENT: SBI account ⚠️ suspended!! 📲"
    norm = text_normalizer.normalize(dirty)
    assert "URGENT" in norm
    assert "SBI account" in norm

def test_normalizer_homoglyph_replacement_extended():
    cyrillic_text = "Y\u043eur b\u0430nk ассоunt is blоckеd"
    clean = text_normalizer.normalize(cyrillic_text)
    assert "Your bank" in clean or "account is blocked" in clean

def test_normalizer_spaced_acronym_fusion():
    spaced = "Please share the O T P and U P I  P I N received"
    clean = text_normalizer.normalize(spaced)
    assert "OTP" in clean
    assert "UPI PIN" in clean or "PIN" in clean

def test_normalizer_leetspeak_deobfuscation():
    leet = "cl1ck h3re to upd4te your kyc"
    clean = text_normalizer.normalize(leet)
    assert "click" in clean
    assert "update" in clean

# 4. RAG Knowledge Base Retrieval Coverage
def test_rag_retrieves_rbi_zero_liability():
    citations = rag_retriever.retrieve("What is RBI zero liability policy for unauthorized transactions?", top_k=2)
    assert len(citations) > 0
    assert any("Zero Liability" in c["title"] or "RBI" in c["source"] for c in citations)

def test_rag_retrieves_golden_hour_guidance():
    citations = rag_retriever.retrieve("How to freeze funds in golden hour using 1930 helpline?", top_k=2)
    assert len(citations) > 0
    assert any("1930" in c["title"] or "Golden Hour" in c["title"] for c in citations)

def test_rag_retrieves_bank_sbi_hotline():
    citations = rag_retriever.retrieve("State Bank of India SBI emergency debit card blocking number", top_k=2)
    assert len(citations) > 0
    assert any("SBI" in c["title"] or "State Bank" in c["title"] for c in citations)

def test_rag_retrieves_digital_arrest_notice():
    citations = rag_retriever.retrieve("Is digital arrest legal in India police video call?", top_k=2)
    assert len(citations) > 0
    assert any("Digital Arrest" in c["title"] or "Extortion" in c["title"] for c in citations)

def test_rag_retrieves_sim_swap_defense():
    citations = rag_retriever.retrieve("What to do if phone loses network suddenly SIM swap?", top_k=2)
    assert len(citations) > 0
    assert any("SIM Swap" in c["title"] or "Sanchar Saathi" in c["title"] for c in citations)

# 5. Security & Boundary Validations
def test_upload_file_size_limit_rejection():
    oversized_data = b"0" * (6 * 1024 * 1024)
    file_payload = {"file": ("big_image.png", io.BytesIO(oversized_data), "image/png")}
    res = client.post("/api/analyze/image", files=file_payload)
    assert res.status_code == 400
    assert "exceeds maximum" in res.json()["detail"].lower()

def test_upload_invalid_mime_type_rejection():
    bad_file = {"file": ("malware.exe", io.BytesIO(b"MZ..."), "application/x-msdownload")}
    res = client.post("/api/analyze/image", files=bad_file)
    assert res.status_code == 400
    assert "unsupported file format" in res.json()["detail"].lower()

def test_url_analysis_empty_rejected():
    res = client.post("/api/analyze/url", json={"url": "   "})
    assert res.status_code == 400

def test_text_analysis_empty_rejected():
    res = client.post("/api/analyze/text", json={"text": "   "})
    assert res.status_code == 400

# 6. Masking Verification
def test_masking_indian_phone_variations():
    masked = mask_sensitive_data("+91 9876543210")
    assert "9876543210" not in masked
    assert "******" in masked

def test_masking_card_numbers():
    masked = mask_sensitive_data("4111 2222 3333 4444")
    assert "4111 2222" not in masked
    assert "XXXX" in masked

def test_masking_otp_codes():
    masked = mask_sensitive_data("Your OTP is 492810")
    assert "492810" not in masked
    assert "[OTP_REDACTED]" in masked

# 7. Feedback Retrain Audit
def test_audit_and_export_feedback_executes_without_error():
    result = audit_and_export_feedback()
    assert isinstance(result, bool)

# 8. Static URL Scanner Adversarial Variants
def test_url_scanner_punycode_spoof():
    res = url_scanner.analyze_url("https://xn--sbi-e1a.co.in/login")
    assert res["url_score"] >= 35.0
    assert any("Punycode" in s["signal"] for s in res["signals"])

def test_url_scanner_ip_address_host():
    res = url_scanner.analyze_url("http://192.168.1.55/pay.html")
    assert res["url_score"] >= 50.0
    assert any("Direct IP Host" in s["signal"] for s in res["signals"])

def test_url_scanner_official_bank_domain_clean():
    res = url_scanner.analyze_url("https://retail.onlinesbi.sbi/retail/login.htm")
    assert res["is_official"] is True
    assert res["url_score"] == 0.0

# 9. Language & Health Deep Checks
def test_language_detection_hinglish_detection():
    from backend.app.core.language_detector import language_detector
    meta = language_detector.detect_language("Aapka SBI account suspend ho gaya hai turant kyc update kare")
    assert meta["language"] == "hi" or meta.get("sub_type") == "hinglish"

def test_language_detection_roman_telugu_detection():
    from backend.app.core.language_detector import language_detector
    meta = language_detector.detect_language("Mee current bill kattaledu ee roju current cut chestharu")
    assert meta["language"] == "te" or meta.get("sub_type") == "roman_te"

def test_vpa_verifier_format_special_characters():
    res = vpa_verifier.analyze("invalid$$handle@@bank")
    assert res.is_valid_format is False
    assert res.verdict == "HIGH RISK"

def test_waterfall_step_subtotal_consistency():
    text = "URGENT: SBI account blocked! Send OTP to 9876543210 immediately."
    res = client.post("/api/analyze/text", json={"text": text})
    data = res.json()
    waterfall = data.get("waterfall", [])
    assert len(waterfall) >= 2
    # Ensure all step point fields are valid floats
    for step in waterfall:
        assert isinstance(step["points"], (int, float))
        assert isinstance(step["running_total"], (int, float))

def test_prefilled_1930_handles_multiple_suspect_artifacts():
    text = "SBI support 9876543210 or 8765432109, click http://sbi-fake.xyz, send fee to scammer@ybl"
    res = client.post("/api/analyze/text", json={"text": text})
    data = res.json()
    complaint = data.get("prefilled_1930_summary")
    assert complaint is not None
    assert len(complaint.get("suspect_phones", [])) >= 1
    assert "1930" in complaint.get("helpline")

def test_health_check_engines_deep_structure():
    res = client.get("/api/health")
    assert res.status_code == 200
    engines = res.json().get("engines", {})
    assert "nlp_loaded" in engines
    assert "ocr_available" in engines
    assert "url_brands_indexed" in engines
    assert "rag_knowledge_entries" in engines
    assert engines["rag_knowledge_entries"] >= 60

