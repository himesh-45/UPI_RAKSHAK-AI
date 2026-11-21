import pytest
from backend.app.detectors.nlp_classifier import nlp_classifier
from backend.app.detectors.rule_engine import rule_engine

def test_language_detection():
    assert nlp_classifier.detect_language("Your account is blocked. Verify immediately.") == "en"
    assert nlp_classifier.detect_language("आपका बैंक खाता आज रात निलंबित कर दिया जाएगा।") == "hi"
    assert nlp_classifier.detect_language("మీ ఖాతా కేవైసీ పెండింగ్ ఉన్నందున బ్లాక్ చేయబడుతుంది.") == "te"
    assert nlp_classifier.detect_language("Aapka bank account suspend ho jayega turant verify kare") == "hi"
    assert nlp_classifier.detect_language("Mee bank account freeze aindi ventane check cheyandi") == "te"

def test_classic_blocked_otp_scam_rules():
    text = "Your UPI account will be blocked. Click here to verify immediately and enter your OTP: http://fake-sbi.top/verify"
    result = rule_engine.evaluate(text)
    
    assert result["hard_override_high_risk"] is True
    assert result["signals_detected"]["has_otp_request"] is True
    assert result["signals_detected"]["has_urgency"] is True
    assert result["signals_detected"]["has_link"] is True
    assert any("Credential Theft Attempt" in r["signal"] for r in result["matched_rules"])
    assert any("Artificial Urgency" in r["signal"] for r in result["matched_rules"])

def test_collect_request_pin_trick():
    text = "You won Rs 3,500 cashback! Enter your UPI PIN to claim reward into your bank account."
    result = rule_engine.evaluate(text)
    
    assert result["hard_override_high_risk"] is True
    assert result["signals_detected"]["has_collect_trick"] is True
    assert any("UPI Collect Fraud Rule" in r["signal"] for r in result["matched_rules"])

def test_remote_access_app_rule():
    text = "Please download AnyDesk app and share the 9-digit code with our customer care agent to get your refund."
    result = rule_engine.evaluate(text)
    
    assert result["hard_override_high_risk"] is True
    assert result["signals_detected"]["has_remote_app"] is True

def test_genuine_bank_alert_negative_rule():
    text = "HDFC Bank: Rs. 1,450.00 debited from a/c 4821 on 21-Nov-2026. Bal: Rs. 24,190.00. NEVER share your OTP or PIN with anyone."
    result = rule_engine.evaluate(text)
    
    assert result["is_genuine_alert"] is True
    assert result["hard_override_high_risk"] is False
    assert result["rule_score"] <= 10.0

def test_telugu_scam_detection():
    text = "మీ ఖాతా కేవైసీ పెండింగ్ ఉన్నందున ఈ రాత్రి బ్లాక్ చేయబడుతుంది. వెంటనే నవీకరించండి: http://fake-bank-kyc.top"
    nlp_res = nlp_classifier.predict(text)
    rule_res = rule_engine.evaluate(text)
    
    assert nlp_res["language"] == "te"
    assert nlp_res["category"] == "fake_bank_kyc"
    assert rule_res["signals_detected"]["has_urgency"] is True

def test_hindi_electricity_scam():
    text = "प्रिय उपभोक्ता, आपके बिजली का बिल अपडेट नहीं होने के कारण आज रात 9:30 बजे बिजली काट दी जाएगी।"
    nlp_res = nlp_classifier.predict(text)
    rule_res = rule_engine.evaluate(text)
    
    assert nlp_res["language"] == "hi"
    assert nlp_res["category"] == "electricity_disconnection"
    assert rule_res["signals_detected"]["has_urgency"] is True

def test_legitimate_otp_message():
    text = "SBI Security Alert: OTP for login is 482910. Valid for 10 minutes. Do NOT share OTP with anyone including bank staff."
    nlp_res = nlp_classifier.predict(text)
    rule_res = rule_engine.evaluate(text)
    
    assert nlp_res["category"] == "legitimate"
    assert rule_res["is_genuine_alert"] is True
    assert rule_res["hard_override_high_risk"] is False
