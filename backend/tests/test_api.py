import os
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import settings

client = TestClient(app)

@pytest.fixture
def demo_assets_dir():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "app", "data", "demo_assets")

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_api_analyze_text_scam():
    payload = {
        "text": "Your UPI account will be blocked. Click here to verify immediately and enter your OTP: http://sbi-kyc-verify.top",
        "save_history": True
    }
    res = client.post("/api/analyze/text", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] == "HIGH RISK"
    assert data["risk_score"] >= 80
    assert "OTP" in data["plain_language_explanation"] or "high risk" in data["plain_language_explanation"].lower()
    assert len(data["evidence"]) >= 2
    assert len(data["recommended_actions"]) >= 1

def test_api_analyze_text_safe():
    payload = {
        "text": "HDFC Bank: Rs. 1,450.00 debited from a/c 4821 for Swiggy. NEVER share your OTP or PIN with anyone.",
        "save_history": True
    }
    res = client.post("/api/analyze/text", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] == "SAFE"
    assert data["risk_score"] <= 34

def test_api_analyze_url_phishing():
    payload = {
        "url": "http://sbi-kyc-update-login.top/auth",
        "save_history": True
    }
    res = client.post("/api/analyze/url", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] == "HIGH RISK"
    assert data["risk_score"] >= 70

def test_api_analyze_url_safe():
    payload = {
        "url": "https://www.onlinesbi.sbi",
        "save_history": True
    }
    res = client.post("/api/analyze/url", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["verdict"] == "SAFE"

def test_api_analyze_image_qr(demo_assets_dir):
    qr_path = os.path.join(demo_assets_dir, "qr_fake_cashback.png")
    with open(qr_path, "rb") as f:
        files = {"file": ("qr_fake_cashback.png", f, "image/png")}
        data = {"save_history": "true", "language": "en"}
        res = client.post("/api/analyze/image", files=files, data=data)

    assert res.status_code == 200
    report = res.json()
    assert report["verdict"] == "HIGH RISK"
    assert report["risk_score"] >= 70
    assert any("QR" in e["source_module"] for e in report["evidence"])

def test_api_assistant_chat():
    payload = {
        "message": "I received an SMS saying power cut at 9:30 PM call +91-98765-43210. Is it real?",
        "language": "en"
    }
    res = client.post("/api/assistant/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert "1930" in data["reply"]
    assert data["verdict"] in ["HIGH RISK", "SUSPICIOUS"]

def test_api_threat_report_submission():
    payload = {
        "input_type": "text",
        "suspicious_content": "Fake lottery won 25 Lakhs call 9876543210",
        "scam_category": "lottery_prize",
        "comments": "Received on WhatsApp from unknown number",
        "contact": "9876543210"
    }
    res = client.post("/api/report", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert data["status"] == "PENDING_REVIEW"

def test_api_dashboard_stats():
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["total_analyses"] >= 10
    assert "category_distribution" in data
    assert "seeded_vs_live" in data
    assert data["seeded_vs_live"]["simulated"] >= 50

def test_api_history_pagination():
    res = client.get("/api/history?limit=10&offset=0&filter_type=all")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert len(data["items"]) <= 10

def test_api_auth_login_and_me():
    # 1. Invalid login
    res = client.post("/api/auth/login", json={"email": "wrong@example.com", "password": "bad"})
    assert res.status_code == 401

    # 2. Valid admin login
    res = client.post("/api/auth/login", json={"email": settings.ADMIN_EMAIL, "password": settings.ADMIN_PASSWORD})
    assert res.status_code == 200
    token_data = res.json()
    token = token_data["access_token"]
    assert token

    # 3. Access protected /me
    headers = {"Authorization": f"Bearer {token}"}
    res_me = client.get("/api/auth/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["email"] == settings.ADMIN_EMAIL
