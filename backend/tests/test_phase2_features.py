import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_vpa_safe_check_legitimate():
    res = client.post("/api/analyze/vpa", json={
        "vpa": "rahul.sharma@okhdfcbank",
        "payee_name": "Rahul Sharma",
        "amount": 500.0,
        "is_collect": False
    })
    assert res.status_code == 200
    data = res.json()
    assert data["is_valid_format"] is True
    assert data["provider"] == "Google Pay (HDFC Bank)"
    assert data["verdict"] == "SAFE"
    assert data["risk_score"] <= 34

def test_vpa_safe_check_collect_request_fraud():
    res = client.post("/api/analyze/vpa", json={
        "vpa": "sbi-support-desk@ybl",
        "payee_name": "SBI Customer Service",
        "amount": 10000.0,
        "is_collect": True
    })
    assert res.status_code == 200
    data = res.json()
    assert data["is_collect_request"] is True
    assert data["verdict"] == "HIGH RISK"
    assert data["risk_score"] >= 70
    assert any("Institutional Brand Impersonation" in r for r in data["reasons"])
    assert any("Collect Request Alert" in r for r in data["reasons"])

def test_vpa_safe_check_malformed():
    res = client.post("/api/analyze/vpa", json={
        "vpa": "not-an-email-or-vpa",
        "is_collect": False
    })
    assert res.status_code == 200
    data = res.json()
    assert data["is_valid_format"] is False
    assert data["verdict"] == "HIGH RISK"

def test_batch_text_analysis():
    payload = {
        "items": [
            {"text": "URGENT: Your SBI account is blocked. Update KYC immediately at http://sbi.co.in.fake-kyc.com", "language": "en"},
            {"text": "Sent Rs. 150 for lunch via UPI", "language": "en"},
            {"text": "మీ విద్యుత్ బిల్లు చెల్లించలేదు. ఈ రాత్రి 9:30 గంటలకు విద్యుత్ సరఫరా నిలిపివేయబడుతుంది. వెంటనే 9876543210 కు కాల్ చేయండి.", "language": "te"}
        ]
    }
    res = client.post("/api/analyze/batch", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_processed"] == 3
    assert len(data["reports"]) == 3
    assert data["reports"][0]["verdict"] in ["HIGH RISK", "SUSPICIOUS"]
    assert data["reports"][1]["verdict"] == "SAFE"
    assert data["reports"][2]["verdict"] in ["HIGH RISK", "SUSPICIOUS"]

def test_user_feedback_submission():
    payload = {
        "analysis_id": 1,
        "input_text": "Sample text for feedback test",
        "reported_verdict": "SUSPICIOUS",
        "is_correct": False,
        "correct_category": "legitimate",
        "feedback_notes": "This was actually a genuine transaction notification from my credit card."
    }
    res = client.post("/api/feedback", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "id" in data

def test_explainability_waterfall_and_highlights():
    scam_msg = "URGENT: SBI account suspended! Send OTP to 9876543210 or click https://sbi.co.in.fake-kyc.com"
    res = client.post("/api/analyze/text", json={"text": scam_msg})
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] == "HIGH RISK"
    
    # 1. Token-level highlight spans
    highlights = data.get("highlight_spans", [])
    assert len(highlights) > 0
    labels = [h["label"] for h in highlights]
    assert any("CREDENTIAL" in l or "LINK" in l or "URGENCY" in l for l in labels)

    # 2. Score Waterfall steps
    waterfall = data.get("waterfall", [])
    assert len(waterfall) > 0
    components = [w["component"] for w in waterfall]
    assert any("Rule Safety Layer" in c or "URL" in c or "Corroboration" in c for c in components)

    # 3. Localized Scam Story Timeline
    story = data.get("scam_story")
    assert story is not None
    assert len(story["steps"]) >= 3
    assert story["steps"][0]["stage"] is not None

    # 4. Pre-filled 1930 summary
    complaint = data.get("prefilled_1930_summary")
    assert complaint is not None
    assert "portal" in complaint
    assert "formal_complaint_narrative" in complaint
    assert "9876543210" in complaint.get("suspect_phones", [])
