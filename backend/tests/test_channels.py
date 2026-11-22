import os
import json
import asyncio
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import settings
from backend.app.database import SessionLocal
from backend.app.models.db_models import AnalysisHistory
from backend.app.channels.core import (
    hash_sender_id,
    check_channel_rate_limit,
    is_duplicate_message,
    delete_user_channel_data,
    process_channel_submission,
    _RATE_LIMIT_BUCKET,
    _SEEN_UPDATES
)

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_channel_state():
    """Reset rate limiter and deduplication buckets between tests."""
    _RATE_LIMIT_BUCKET.clear()
    _SEEN_UPDATES.clear()
    yield
    _RATE_LIMIT_BUCKET.clear()
    _SEEN_UPDATES.clear()

def test_sender_hash_privacy():
    raw_id = "+919876543210"
    h1 = hash_sender_id(raw_id)
    h2 = hash_sender_id(raw_id)
    assert h1 == h2
    assert len(h1) == 64
    assert raw_id not in h1
    assert "9876543210" not in h1

def test_rate_limiter_20_per_hour():
    sender_hash = hash_sender_id("test_rate_user")
    
    # First 20 should pass
    for i in range(20):
        allowed, remaining = check_channel_rate_limit(sender_hash)
        assert allowed is True
        assert remaining == 20 - (i + 1)

    # 21st must be blocked
    allowed, remaining = check_channel_rate_limit(sender_hash)
    assert allowed is False
    assert remaining == 0

def test_deduplication():
    assert is_duplicate_message("telegram", "update_1001") is False
    assert is_duplicate_message("telegram", "update_1001") is True
    assert is_duplicate_message("telegram", "update_1002") is False
    assert is_duplicate_message("whatsapp", "update_1001") is False  # Separate channel

def test_channel_process_text_and_privacy_db():
    raw_phone = "+919123456789"
    sender_hash = hash_sender_id(raw_phone)
    delete_user_channel_data(sender_hash)

    msg = "Urgent: Electricity power disconnect tonight at 9:30 PM. Call officer at 9876543210 immediately."
    res = asyncio.run(process_channel_submission(
        channel="telegram",
        sender_id=raw_phone,
        content_type="text",
        content=msg
    ))

    assert res["verdict"] in ["HIGH RISK", "SUSPICIOUS"]
    assert res["risk_score"] >= 50
    assert "1930" in res["text"] or "Dial 1930" in str(res["buttons"])

    # Verify Database row
    db = SessionLocal()
    try:
        row = db.query(AnalysisHistory).filter(AnalysisHistory.sender_hash == sender_hash).first()
        assert row is not None
        assert row.channel == "telegram"
        assert row.sender_hash == sender_hash
        # Raw phone number must be masked in raw_input_masked
        assert raw_phone not in row.raw_input_masked
        assert "[PHONE_REDACTED]" in row.raw_input_masked or "******" in row.raw_input_masked
    finally:
        db.close()

    # Test /delete_data command
    del_res = asyncio.run(process_channel_submission(
        channel="telegram",
        sender_id=raw_phone,
        content_type="text",
        content="/delete_data"
    ))
    assert "deleted 1" in del_res["text"].lower()

    db = SessionLocal()
    try:
        remaining_rows = db.query(AnalysisHistory).filter(AnalysisHistory.sender_hash == sender_hash).count()
        assert remaining_rows == 0
    finally:
        db.close()

def test_group_chat_privacy_no_db_persistence():
    group_sender = "user_in_group_555"
    sender_hash = hash_sender_id(group_sender)
    delete_user_channel_data(sender_hash)

    res = asyncio.run(process_channel_submission(
        channel="telegram",
        sender_id=group_sender,
        content_type="text",
        content="Free Rs. 5000 cashback! Scan QR now: http://fake-cashback.top",
        is_group=True
    ))
    assert res["verdict"] == "HIGH RISK"

    # Strictly assert NO record is created in database for group messages
    db = SessionLocal()
    try:
        count = db.query(AnalysisHistory).filter(AnalysisHistory.sender_hash == sender_hash).count()
        assert count == 0, "Group chat messages must NEVER be stored in DB"
    finally:
        db.close()

def test_telegram_webhook_secret_verification(monkeypatch):
    monkeypatch.setattr(settings, "TELEGRAM_WEBHOOK_SECRET", "super_secret_webhook_token_123")

    payload = {
        "update_id": 999111,
        "message": {
            "chat": {"id": 12345, "type": "private"},
            "from": {"id": 12345},
            "text": "Hello bot"
        }
    }

    # Without header -> 403
    res_bad = client.post("/api/channels/telegram/webhook", json=payload)
    assert res_bad.status_code == 403

    # With invalid header -> 403
    res_invalid = client.post(
        "/api/channels/telegram/webhook",
        json=payload,
        headers={"X-Telegram-Bot-Api-Secret-Token": "wrong_token"}
    )
    assert res_invalid.status_code == 403

    # With correct header -> 200
    res_ok = client.post(
        "/api/channels/telegram/webhook",
        json=payload,
        headers={"X-Telegram-Bot-Api-Secret-Token": "super_secret_webhook_token_123"}
    )
    assert res_ok.status_code == 200

def test_meta_webhook_challenge():
    # Valid challenge handshake
    res = client.get("/api/channels/whatsapp/meta?hub.mode=subscribe&hub.challenge=115599&hub.verify_token=demo_token")
    assert res.status_code == 200
    assert res.text == "115599"

def test_twilio_webhook_endpoint():
    form_payload = {
        "MessageSid": "SM1234567890abcdef",
        "From": "whatsapp:+919876543210",
        "Body": "Your electricity connection will be disconnected today. Pay now.",
        "NumMedia": "0"
    }

    res = client.post("/api/channels/whatsapp/twilio", data=form_payload)
    assert res.status_code == 200
    assert "xml" in res.headers["content-type"]
    assert "<Response><Message>" in res.text
