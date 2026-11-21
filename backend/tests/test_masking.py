import pytest
from backend.app.core.masking import mask_sensitive_data

def test_mask_phone_number():
    text = "Call officer at 9876543210 immediately"
    masked = mask_sensitive_data(text)
    assert "9876543210" not in masked
    assert "98******10" in masked

def test_mask_card_number():
    text = "Card number 4123-5678-9012-3456 is blocked"
    masked = mask_sensitive_data(text)
    assert "4123" not in masked
    assert "XXXX-XXXX-3456" in masked

def test_mask_otp():
    text = "Your OTP is 482910 for transaction authorization"
    masked = mask_sensitive_data(text)
    assert "482910" not in masked
    assert "[OTP_REDACTED]" in masked

def test_mask_multiple_credentials():
    text = "Dear user 9876543210, your OTP is 918234 for card 1234567890123456."
    masked = mask_sensitive_data(text)
    assert "9876543210" not in masked
    assert "918234" not in masked
    assert "1234567890123456" not in masked
