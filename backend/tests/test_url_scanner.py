import pytest
from backend.app.detectors.url_scanner import url_scanner

def test_url_extraction():
    text = "Check this link http://example.com/login and also bit.ly/3xFake for cashback."
    urls = url_scanner.extract_urls(text)
    assert len(urls) == 2
    assert "http://example.com/login" in urls
    assert any("bit.ly" in u for u in urls)

def test_ip_address_host():
    res = url_scanner.analyze_url("http://192.168.1.1/verify")
    assert res["url_score"] >= 45.0
    assert any("Direct IP Host" in s["signal"] for s in res["signals"])

def test_url_shortener():
    res = url_scanner.analyze_url("https://bit.ly/3xFake")
    assert any("URL Shortener Cloaking" in s["signal"] for s in res["signals"])
    assert res["is_suspicious"] is True

def test_brand_impersonation_sbi_top():
    res = url_scanner.analyze_url("http://sbi-kyc-update-login.top/auth")
    assert res["url_score"] >= 70.0
    assert any("Brand Typosquatting" in s["signal"] for s in res["signals"])
    assert any("High-Risk Top-Level Domain" in s["signal"] for s in res["signals"])
    assert any("Phishing Keywords" in s["signal"] for s in res["signals"])

def test_levenshtein_typosquatting_hdfc():
    # hdfcbamk vs hdfcbank (dist = 1)
    res = url_scanner.analyze_url("https://hdfcbamk.com/login")
    assert any("Typosquatting" in s["signal"] for s in res["signals"])
    assert res["url_score"] >= 45.0

def test_at_symbol_deception():
    res = url_scanner.analyze_url("http://sbi.co.in@evil-server.com/login")
    assert any("URL Authority Deception" in s["signal"] for s in res["signals"])

def test_punycode_detection():
    res = url_scanner.analyze_url("http://xn--sb-dia.com/verify")
    assert any("Punycode (IDN)" in s["signal"] for s in res["signals"])

def test_excessive_subdomains():
    res = url_scanner.analyze_url("http://portal.login.secure.update.bank.xyz/kyc")
    assert any("Excessive Subdomains" in s["signal"] for s in res["signals"])

def test_official_legitimate_sbi():
    res = url_scanner.analyze_url("https://www.onlinesbi.sbi")
    assert res["is_official"] is True
    assert res["url_score"] == 0.0

def test_official_hdfc():
    res = url_scanner.analyze_url("https://netbanking.hdfcbank.com/netbanking")
    assert res["is_official"] is True
    assert res["url_score"] <= 10.0
