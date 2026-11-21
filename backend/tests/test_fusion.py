import pytest
from backend.app.detectors.nlp_classifier import nlp_classifier
from backend.app.detectors.rule_engine import rule_engine
from backend.app.detectors.url_scanner import url_scanner
from backend.app.detectors.qr_scanner import qr_scanner
from backend.app.fusion.risk_engine import risk_engine

def analyze_sample(text: str, input_type: str = "text", qr_result = None, lang_override = "auto"):
    nlp_res = nlp_classifier.predict(text)
    rule_res = rule_engine.evaluate(text)
    url_res = url_scanner.scan_all_urls(text)
    
    report = risk_engine.fuse(
        input_type=input_type,
        text=text,
        nlp_result=nlp_res,
        rule_result=rule_res,
        url_results=url_res,
        qr_result=qr_result,
        language_override=lang_override
    )
    return report

def test_classic_blocked_otp_high_risk():
    text = "Your UPI account will be blocked. Click here to verify immediately and enter your OTP: http://sbi-kyc-verify.top"
    report = analyze_sample(text)

    assert report.verdict == "HIGH RISK"
    assert report.risk_score >= 80
    assert any("Urgency" in e.signal for e in report.evidence)
    assert any("Credential Theft" in e.signal for e in report.evidence)
    assert any("Do NOT share your OTP" in a for a in report.recommended_actions)

def test_genuine_bank_alert_is_safe():
    text = "HDFC Bank: An amount of Rs. 1,450.00 is debited from account ending 4821 on 21-Nov-2026 for Swiggy. Available balance: Rs. 24,190.00. NEVER share your OTP or PIN with anyone."
    report = analyze_sample(text)

    assert report.verdict == "SAFE"
    assert report.risk_score <= 34
    assert report.detected_category == "legitimate"

def test_telugu_scam_explanation():
    text = "ప్రియమైన వినియోగదారుడా, మీ SBI ఖాతా కేవైసీ పెండింగ్ ఉన్నందున ఈ రాత్రి బ్లాక్ చేయబడుతుంది. వెంటనే నవీకరించండి: http://sbi-kyc-verify.top"
    report = analyze_sample(text)

    assert report.verdict == "HIGH RISK"
    assert report.language == "te"
    assert "ప్రమాద" in report.plain_language_explanation
    assert len(report.recommended_actions) >= 1

def test_hindi_electricity_explanation():
    text = "प्रिय उपभोक्ता, आपके बिजली का बिल अपडेट नहीं होने के कारण आज रात 9:30 बजे बिजली काट दी जाएगी। तुरंत भुगतान करें: http://bijli-bill-pay.online"
    report = analyze_sample(text)

    assert report.verdict == "HIGH RISK"
    assert report.language == "hi"
    assert "जोखिम" in report.plain_language_explanation
    assert len(report.recommended_actions) >= 1

def test_collect_request_pin_fraud():
    text = "Congratulations! You have received a cashback refund of Rs. 3,500 on PhonePe. Enter your UPI PIN to claim money into your account."
    report = analyze_sample(text)

    assert report.verdict == "HIGH RISK"
    assert any("receiving money NEVER requires entering your PIN" in a for a in report.recommended_actions)

def test_disclaimer_present_in_report():
    text = "Test sample message"
    report = analyze_sample(text)
    assert "Heuristic risk indicator" in report.disclaimer
    assert "1930" in report.disclaimer
