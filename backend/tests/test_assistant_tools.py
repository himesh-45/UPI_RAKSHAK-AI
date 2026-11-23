import pytest
from backend.app.assistant.tools import (
    analyze_text,
    analyze_url,
    check_upi_id,
    check_call_script,
    lookup_community_reports,
    retrieve_kb
)

def test_tool_analyze_text_scam():
    text = "URGENT: Your SBI YONO account is locked. Update KYC at http://sbi-kyc-verify.top immediately or debit will be stopped."
    res = analyze_text(text, language="en")
    assert res["verdict"] in ["HIGH RISK", "SUSPICIOUS"]
    assert res["risk_score"] >= 70
    assert len(res["evidence"]) >= 1
    assert len(res["recommended_actions"]) >= 1

def test_tool_analyze_text_safe():
    text = "HDFC Bank: Rs. 450 debited at Swiggy on 12-Nov. Available balance: Rs. 14,200. Never share OTP with anyone."
    res = analyze_text(text, language="en")
    assert res["verdict"] == "SAFE"
    assert res["risk_score"] <= 34

def test_tool_analyze_url_phishing():
    url = "http://sbi-kyc-pan-update.xyz/login"
    res = analyze_url(url)
    assert res["is_suspicious"] is True
    assert res["url_score"] >= 50
    assert any("Brand Typosquatting" in s["signal"] or ".xyz" in s["signal"] for s in res["signals"])

def test_tool_analyze_url_legitimate():
    url = "https://retail.onlinesbi.sbi"
    res = analyze_url(url)
    assert res["is_suspicious"] is False
    assert res["is_official"] is True
    assert res["url_score"] <= 10

def test_tool_check_upi_id_impersonation():
    vpa = "sbi-support@ybl"
    res = check_upi_id(vpa)
    assert res["is_valid_format"] is True
    assert res["risk_score"] > 30
    assert any("impersonat" in r.lower() or "sbi" in r.lower() for r in res["reasons"])

def test_tool_check_upi_id_valid_safe():
    vpa = "user9876@okhdfcbank"
    res = check_upi_id(vpa)
    assert res["is_valid_format"] is True
    assert "Google Pay" in res["provider"]
    assert res["risk_score"] <= 30

def test_tool_check_call_script_digital_arrest():
    script = (
        "This is CBI Officer Sharma calling from Mumbai Headquarters. A parcel containing MDMA and fake passports "
        "was intercepted with your Aadhaar. You are under digital arrest. Do not disconnect this Skype video call, "
        "and transfer your funds to the RBI security verification account immediately."
    )
    res = check_call_script(script, language="en")
    assert res["verdict"] == "HIGH RISK"
    assert res["risk_score"] >= 80
    assert any("Digital Arrest" in t for t in res["flagged_tactics"])
    assert "1930" in res["immediate_advice"]

def test_tool_lookup_community_reports():
    res = lookup_community_reports(entity_type="phone", entity_value="9876543210")
    assert isinstance(res, dict)
    assert "reputation_status" in res or "community_score" in res or "reports_count" in res

def test_tool_retrieve_kb():
    chunks = retrieve_kb("how to complain to 1930 helpline", language="en", top_k=2)
    assert len(chunks) >= 1
    assert any("1930" in c.get("title", "") or "1930" in c.get("content", "") for c in chunks)
