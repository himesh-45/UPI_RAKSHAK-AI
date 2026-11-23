import pytest
from backend.app.detectors.callback_detector import callback_scam_detector
from backend.app.detectors.nlp_classifier import nlp_classifier
from backend.app.detectors.rule_engine import rule_engine
from backend.app.detectors.url_scanner import url_scanner
from backend.app.fusion.risk_engine import risk_engine


def analyze_sample(text: str, lang_override: str = "auto"):
    nlp_res = nlp_classifier.predict(text)
    rule_res = rule_engine.evaluate(text)
    url_res = url_scanner.scan_all_urls(text)
    report = risk_engine.fuse(
        input_type="text",
        text=text,
        nlp_result=nlp_res,
        rule_result=rule_res,
        url_results=url_res,
        language_override=lang_override,
    )
    return report


# ==============================================================================
# 1. FAILING REGRESSION EXAMPLE & DIRECT VARIANTS
# ==============================================================================

def test_exact_failing_example_regression():
    """
    Exact failing example from user specification:
    'Alert: ₹49,999 debited from your account. If not done by you, call +91-XXXXXXXXXX immediately.'
    Must get at least SUSPICIOUS, and HIGH RISK when combined with urgency.
    """
    text = "Alert: ₹49,999 debited from your account. If not done by you, call +91-XXXXXXXXXX immediately."
    report = analyze_sample(text)

    assert report.verdict in ("HIGH RISK", "SUSPICIOUS")
    assert report.risk_score >= 70
    assert report.detected_category == "fake_debit_alert_callback"

    # Verify explainability signals
    signals = [e.signal for e in report.evidence]
    assert any("callback" in s.lower() or "phone" in s.lower() or "mobile" in s.lower() for s in signals)
    assert any("reference" in s.lower() or "account" in s.lower() or "missing" in s.lower() or "marker" in s.lower() for s in signals)


def test_callback_with_indian_mobile_number():
    """Realistic Indian mobile callback number format (+91-9876543210)."""
    text = "Alert: Rs 38,500 debited from your bank account. If this transaction was not done by you, call +91-9876543210 immediately to dispute."
    report = analyze_sample(text)

    assert report.verdict == "HIGH RISK"
    assert report.risk_score >= 75
    assert report.detected_category == "fake_debit_alert_callback"


def test_callback_with_spaced_digits_obfuscation():
    """Phone number obfuscated with spaces to evade simple regexes."""
    text = "Dear Customer, INR 45,000 debited from your account. If not authorized, call 9 8 7 6 5 4 3 2 1 0 right now to block."
    report = analyze_sample(text)

    assert report.verdict in ("HIGH RISK", "SUSPICIOUS")
    assert report.risk_score >= 70
    assert report.detected_category == "fake_debit_alert_callback"


def test_callback_with_number_in_words():
    """Phone number written partially or entirely in words."""
    text = "Bank Alert: ₹29,000 debited from account. If not you, call nine eight seven six five four three two one zero immediately to reverse."
    report = analyze_sample(text)

    assert report.verdict in ("HIGH RISK", "SUSPICIOUS")
    assert report.risk_score >= 65


def test_callback_whatsapp_directive():
    """Directing victim to WhatsApp or message on personal number."""
    text = "Alert: Rs 49,000 debited from your account. To cancel or dispute this transaction, msg on WhatsApp +91-9876543210 immediately."
    report = analyze_sample(text)

    assert report.verdict in ("HIGH RISK", "SUSPICIOUS")
    assert report.risk_score >= 70
    assert report.detected_category == "fake_debit_alert_callback"


def test_bank_fraud_team_impersonation_follow_up():
    """Attackers impersonating bank fraud prevention team."""
    text = "Hello, I am from bank fraud team. Your card has an unauthorized debit of Rs 48,000. Please call 9876543210 immediately to cancel the charge."
    report = analyze_sample(text)

    assert report.verdict in ("HIGH RISK", "SUSPICIOUS")
    assert report.risk_score >= 70


# ==============================================================================
# 2. MULTILINGUAL CALLBACK SCAM TESTS (HINDI, TELUGU, HINGLISH)
# ==============================================================================

def test_hindi_callback_scam():
    text = "अलर्ट: आपके खाते से ₹49,999 डेबिट हो गए हैं। यदि आपने यह नहीं किया है, तो तुरंत 9876543210 पर कॉल करें।"
    report = analyze_sample(text, lang_override="hi")

    assert report.verdict in ("HIGH RISK", "SUSPICIOUS")
    assert report.risk_score >= 70
    assert report.language == "hi"


def test_telugu_callback_scam():
    text = "హెచ్చరిక: మీ బ్యాంక్ ఖాతా నుండి ₹49,999 డెబిట్ చేయబడింది. మీరు చేయకపోతే వెంటనే 9876543210 కి కాల్ చేయండి."
    report = analyze_sample(text, lang_override="te")

    assert report.verdict in ("HIGH RISK", "SUSPICIOUS")
    assert report.risk_score >= 70
    assert report.language == "te"


def test_hinglish_callback_scam():
    text = "Alert: Aapke account se Rs 49,999 debit ho gaya hai. Agar aapne nahi kiya to turant call karein 9876543210 par transaction cancel karne ke liye."
    report = analyze_sample(text)

    assert report.verdict in ("HIGH RISK", "SUSPICIOUS")
    assert report.risk_score >= 70


# ==============================================================================
# 3. GENUINE BANK ALERT PROTECTION (HARD NEGATIVES)
# ==============================================================================

def test_genuine_bank_alert_with_last4_and_utr():
    """Genuine bank alert with account last 4, UTR, balance, and standard safety notice."""
    text = "HDFC Bank: Rs 2,500.00 debited from a/c **4821 on 22-Nov-26 to SWIGGY. UTR: 432789123456. Avl Bal: Rs 18,450.00. Never share OTP or PIN."
    report = analyze_sample(text)

    assert report.verdict == "SAFE"
    assert report.risk_score <= 20
    assert report.detected_category == "legitimate"


def test_genuine_bank_alert_with_official_1800_tollfree():
    """Genuine bank alert providing official 1800 toll-free customer care number."""
    text = "SBI: INR 1,200.00 debited from A/c ending XX5432 on 21-Nov-26 at RELIANCE RETAIL. Ref 412345678901. If not done by you, call 1800112211 or 18004253800."
    report = analyze_sample(text)

    assert report.verdict == "SAFE"
    assert report.risk_score <= 25


def test_genuine_hindi_bank_alert():
    """Genuine Hindi debit alert with account last 4 and 1800 helpline."""
    text = "एसबीआई: आपके खाता संख्या **4321 से ₹1,500 का डेबिट हुआ। शेष राशि: ₹12,400। यदि यह आपने नहीं किया तो 1800112211 पर संपर्क करें। ओटीपी साझा न करें।"
    report = analyze_sample(text, lang_override="hi")

    assert report.verdict == "SAFE"
    assert report.risk_score <= 25


def test_genuine_telugu_bank_alert():
    """Genuine Telugu debit alert with account last 4 and official helpline."""
    text = "ఆంధ్రా బ్యాంక్: మీ ఖాతా **9876 నుండి ₹850 డెబిట్ చేయబడింది. బ్యాలెన్స్: ₹9,400. సహాయం కోసం 18004251515 సంప్రదించండి. ఎవరికీ ఓటీపీ చెప్పవద్దు."
    report = analyze_sample(text, lang_override="te")

    assert report.verdict == "SAFE"
    assert report.risk_score <= 25


# ==============================================================================
# 4. DIRECT UNIT TESTS ON CALLBACK DETECTOR MODULE
# ==============================================================================

def test_callback_detector_unit_signals():
    text = "Alert: ₹49,999 debited from your account. If not done by you, call +91-XXXXXXXXXX immediately."
    res = callback_scam_detector.detect(text)

    assert res["is_callback_scam"] is True
    assert res["details"]["has_debit_credit"] is True
    assert res["details"]["has_callback_instruction"] is True
    assert (res["details"]["has_personal_mobile"] or res["details"]["has_placeholder"]) is True
    assert res["details"]["missing_genuine_markers"] is True
    assert res["score"] >= 70.0


def test_callback_detector_negative_on_official_alert():
    text = "ICICI Bank: Debited INR 3,200 from a/c **8765 on 20-Nov-2026. Ref: 498712345678. Call 18001080 for dispute."
    res = callback_scam_detector.detect(text)

    assert res["is_callback_scam"] is False
    assert res["score"] <= 10.0


# ==============================================================================
# 5. PROPERTY / INVARIANCE TESTS
# ==============================================================================

def test_property_adding_callback_directive_never_lowers_score():
    """
    Property: Given a vague debit alert, appending an urgent callback directive
    to a suspicious personal number should NEVER decrease the risk score.
    """
    base_text = "Alert: ₹49,999 debited from your account."
    with_callback = base_text + " If not done by you, call 9876543210 immediately to dispute."

    base_report = analyze_sample(base_text)
    cb_report = analyze_sample(with_callback)

    assert cb_report.risk_score >= base_report.risk_score


def test_property_adding_genuine_markers_never_raises_score():
    """
    Property: Given an alert, adding genuine banking markers (masked account last-4,
    UTR reference number, and official 1800 toll-free number) should NEVER raise the risk score.
    """
    alert_text = "Alert: ₹1,500 debited from account."
    genuine_text = alert_text + " Ending in **4321. Ref: UTR987654321012. Call toll-free 1800112211. Never share OTP."

    alert_report = analyze_sample(alert_text)
    genuine_report = analyze_sample(genuine_text)

    assert genuine_report.risk_score <= alert_report.risk_score
