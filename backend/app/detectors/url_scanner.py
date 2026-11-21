import re
import urllib.parse
import tldextract
from typing import List, Dict, Any, Optional
from rapidfuzz import distance, fuzz

# Official Indian Banking, UPI, and Government Domains
OFFICIAL_ENTITIES = [
    {"name": "State Bank of India (SBI)", "brand": "sbi", "domains": ["sbi.co.in", "onlinesbi.sbi", "bank.sbi"]},
    {"name": "HDFC Bank", "brand": "hdfc", "domains": ["hdfcbank.com", "hdfc.com"]},
    {"name": "ICICI Bank", "brand": "icici", "domains": ["icicibank.com"]},
    {"name": "Axis Bank", "brand": "axis", "domains": ["axisbank.com"]},
    {"name": "Punjab National Bank", "brand": "pnb", "domains": ["pnbindia.in"]},
    {"name": "Kotak Mahindra Bank", "brand": "kotak", "domains": ["kotak.com", "kotakbank.com"]},
    {"name": "Bank of Baroda", "brand": "bankofbaroda", "domains": ["bankofbaroda.in", "bob.bank"]},
    {"name": "Canara Bank", "brand": "canarabank", "domains": ["canarabank.com"]},
    {"name": "Paytm / Paytm Payments Bank", "brand": "paytm", "domains": ["paytm.com", "paytmbank.com"]},
    {"name": "PhonePe", "brand": "phonepe", "domains": ["phonepe.com"]},
    {"name": "Google Pay", "brand": "gpay", "domains": ["pay.google.com", "google.com"]},
    {"name": "BHIM / NPCI", "brand": "bhim", "domains": ["bhimupi.org.in", "npci.org.in"]},
    {"name": "NPCI", "brand": "npci", "domains": ["npci.org.in"]},
    {"name": "IRCTC", "brand": "irctc", "domains": ["irctc.co.in"]},
    {"name": "Cybercrime Helpline", "brand": "cybercrime", "domains": ["cybercrime.gov.in"]},
    {"name": "UIDAI (Aadhaar)", "brand": "uidai", "domains": ["uidai.gov.in"]},
    {"name": "Income Tax Department", "brand": "incometax", "domains": ["incometax.gov.in"]},
    {"name": "BESCOM (Bangalore Electricity)", "brand": "bescom", "domains": ["bescom.karnataka.gov.in", "bescom.org"]},
    {"name": "TSSPDCL (Telangana Electricity)", "brand": "tsspdcl", "domains": ["tssouthernpower.com"]},
    {"name": "UPPCL (UP Electricity)", "brand": "uppcl", "domains": ["upenergy.in"]},
    {"name": "TNEB / TANGEDCO", "brand": "tneb", "domains": ["tangedco.gov.in"]}
]

SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "is.gd", "cutt.ly", "t.co", "rb.gy",
    "ow.ly", "tiny.cc", "rebrand.ly", "shorturl.at", "bl.ink"
}

SUSPICIOUS_TLDS = {
    "top", "xyz", "click", "site", "online", "club", "biz",
    "live", "loan", "work", "vip", "gq", "cf", "tk", "ml", "cc",
    "buzz", "rest", "support", "link", "info"
}

HIGH_RISK_URL_KEYWORDS = {
    "kyc", "verify", "verification", "update", "refund", "cashback",
    "claim", "login", "authenticate", "pan", "aadhaar", "bonus",
    "reward", "unblock", "secure", "helpline", "disconnection", "bill"
}

# Regex to safely find URLs without executing them
URL_EXTRACT_REGEX = re.compile(
    r'(?i)\b(?:hxxps?|https?|ftp)://[^\s<>"\'{}|\\^`]+|'
    r'\b(?:www\d{0,3}\.)[^\s<>"\'{}|\\^`]+|'
    r'\b[a-zA-Z0-9.-]+\.(?:com|in|co\.in|org|net|top|xyz|click|site|online|club|biz|gov\.in|edu\.in)/[^\s<>"\'{}|\\^`]*|'
    r'\b(?:bit\.ly|tinyurl\.com|is\.gd|cutt\.ly|t\.co|rb\.gy)/[a-zA-Z0-9_\-]+'
)

IP_HOST_REGEX = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

class StaticURLScanner:
    """
    Pure static analysis URL scanner.
    NEVER performs network requests, DNS lookups, or resolves links.
    """

    def extract_urls(self, text: str) -> List[str]:
        if not text:
            return []
        matches = URL_EXTRACT_REGEX.findall(text)
        return list(dict.fromkeys(matches))  # deduplicate preserving order

    def analyze_url(self, raw_url: str) -> Dict[str, Any]:
        normalized = raw_url.strip()
        if normalized.lower().startswith("hxxp"):
            normalized = "http" + normalized[4:]
        if not re.match(r'^[a-zA-Z]+://', normalized):
            normalized = "http://" + normalized

        parsed = urllib.parse.urlparse(normalized)
        netloc = parsed.netloc.lower()
        path = parsed.path.lower()
        query = parsed.query.lower()

        ext = tldextract.extract(normalized)
        domain = ext.domain.lower()
        suffix = ext.suffix.lower()
        subdomain = ext.subdomain.lower()
        registered_domain = f"{domain}.{suffix}" if suffix else domain

        signals = []
        score = 0.0

        # 1. IP-address host
        host_no_port = netloc.split(":")[0]
        if IP_HOST_REGEX.match(host_no_port):
            score += 45.0
            signals.append({
                "signal": f"Direct IP Host Address: Host '{host_no_port}' uses numeric IP instead of a registered domain name.",
                "source_module": "URL_SCANNER",
                "weight": 45.0,
                "severity": "CRITICAL"
            })

        # 2. URL shortener
        if registered_domain in SHORTENER_DOMAINS:
            score += 25.0
            signals.append({
                "signal": f"URL Shortener Cloaking: '{registered_domain}' conceals the true destination host.",
                "source_module": "URL_SCANNER",
                "weight": 25.0,
                "severity": "HIGH"
            })

        # 3. '@' symbol in authority (credential deception / redirect trick)
        if "@" in netloc or "@" in parsed.netloc:
            score += 40.0
            signals.append({
                "signal": "URL Authority Deception: Uses '@' in URL to mislead users about the actual destination server.",
                "source_module": "URL_SCANNER",
                "weight": 40.0,
                "severity": "CRITICAL"
            })

        # 4. Punycode / Homoglyph / Internationalized Domain Name
        if "xn--" in netloc:
            score += 35.0
            signals.append({
                "signal": "Punycode (IDN) Detected: Domain uses Internationalized 'xn--' prefix, frequently used in homoglyph spoofing.",
                "source_module": "URL_SCANNER",
                "weight": 35.0,
                "severity": "HIGH"
            })
        
        # Check non-ASCII homoglyphs
        if any(ord(c) > 127 for c in netloc):
            score += 35.0
            signals.append({
                "signal": "Unicode Homoglyph Characters: Domain contains non-ASCII characters visually imitating standard Latin letters.",
                "source_module": "URL_SCANNER",
                "weight": 35.0,
                "severity": "HIGH"
            })

        # 5. Brand Impersonation & Typosquatting (SBI, HDFC, Paytm, ICICI, etc.)
        for entity in OFFICIAL_ENTITIES:
            brand = entity["brand"]
            official_domains = entity["domains"]

            # Exact brand match or close edit distance in domain/subdomain
            brand_in_domain = brand in domain or brand in subdomain
            is_legit = any(registered_domain == off or registered_domain.endswith("." + off) for off in official_domains)

            if brand_in_domain and not is_legit:
                score += 50.0
                signals.append({
                    "signal": f"Brand Typosquatting / Impersonation: URL mimics '{entity['name']}' brand, but domain '{registered_domain}' is NOT an authorized official domain ({', '.join(official_domains)}).",
                    "source_module": "URL_SCANNER",
                    "weight": 50.0,
                    "severity": "CRITICAL"
                })
                break
            elif not is_legit and len(domain) >= 3:
                # Check Levenshtein distance against official domain stems
                for off in official_domains:
                    off_stem = off.split(".")[0]
                    dist = distance.Levenshtein.distance(domain, off_stem)
                    if 0 < dist <= 2 and len(domain) > 2 and len(off_stem) > 2:
                        score += 45.0
                        signals.append({
                            "signal": f"Typosquatting Detected: Domain stem '{domain}' is {dist} character edit distance from official '{off_stem}' ({entity['name']}).",
                            "source_module": "URL_SCANNER",
                            "weight": 45.0,
                            "severity": "CRITICAL"
                        })
                        break

        # 6. Suspicious TLD check
        if suffix in SUSPICIOUS_TLDS:
            score += 25.0
            signals.append({
                "signal": f"High-Risk Top-Level Domain: Domain uses '.{suffix}', a TLD heavily associated with disposable phishing campaigns.",
                "source_module": "URL_SCANNER",
                "weight": 25.0,
                "severity": "HIGH"
            })

        # 7. Excessive Subdomains
        sub_parts = [p for p in subdomain.split(".") if p]
        if len(sub_parts) >= 2:
            score += 20.0
            signals.append({
                "signal": f"Excessive Subdomains: Host contains {len(sub_parts)} nested subdomains ({subdomain}), a common evasion technique.",
                "source_module": "URL_SCANNER",
                "weight": 20.0,
                "severity": "MEDIUM"
            })

        # 8. Hyphen & Digit Abuse
        hyphen_count = domain.count("-")
        digit_count = len(re.findall(r'\d', domain))
        if hyphen_count >= 2 or (hyphen_count >= 1 and digit_count >= 2):
            score += 20.0
            signals.append({
                "signal": f"Hyphen/Digit Stuffing: Domain '{domain}' contains {hyphen_count} hyphens and {digit_count} digits.",
                "source_module": "URL_SCANNER",
                "weight": 20.0,
                "severity": "MEDIUM"
            })

        # 9. Non-HTTPS scheme
        if parsed.scheme.lower() == "http":
            score += 15.0
            signals.append({
                "signal": "Insecure Protocol: URL uses unencrypted HTTP instead of HTTPS.",
                "source_module": "URL_SCANNER",
                "weight": 15.0,
                "severity": "LOW"
            })

        # 10. High-risk keywords in path or query
        url_text = f"{path} {query} {domain}"
        found_keywords = [kw for kw in HIGH_RISK_URL_KEYWORDS if kw in url_text]
        if found_keywords:
            weight = min(25.0, len(found_keywords) * 8.0)
            score += weight
            signals.append({
                "signal": f"Phishing Keywords in URL: Found suspicious keywords ({', '.join(found_keywords[:4])}) in URL structure.",
                "source_module": "URL_SCANNER",
                "weight": weight,
                "severity": "MEDIUM"
            })

        # 11. Excessively long URL
        if len(raw_url) > 75:
            score += 10.0
            signals.append({
                "signal": f"Excessive URL Length: URL is {len(raw_url)} characters long, which may hide suspicious query parameters.",
                "source_module": "URL_SCANNER",
                "weight": 10.0,
                "severity": "LOW"
            })

        # Legitimate domain check
        is_official = any(
            registered_domain == off or registered_domain.endswith("." + off)
            for entity in OFFICIAL_ENTITIES
            for off in entity["domains"]
        )
        if is_official and not signals:
            score = 0.0
            signals.append({
                "signal": f"Verified Official Domain: '{registered_domain}' belongs to verified entity registry.",
                "source_module": "URL_SCANNER",
                "weight": -50.0,
                "severity": "INFO"
            })

        capped_score = max(0.0, min(100.0, score))

        return {
            "url": raw_url,
            "normalized_url": normalized,
            "domain": registered_domain,
            "signals": signals,
            "url_score": capped_score,
            "is_suspicious": capped_score >= 35.0,
            "is_official": is_official
        }

    def scan_all_urls(self, text: str) -> List[Dict[str, Any]]:
        extracted = self.extract_urls(text)
        return [self.analyze_url(u) for u in extracted]

url_scanner = StaticURLScanner()
