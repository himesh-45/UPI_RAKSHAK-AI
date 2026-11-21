import re
import urllib.parse
import tldextract
from typing import List, Dict, Any, Optional, Set
from rapidfuzz import distance

# 88 Verified Official Indian Banking, UPI, Government, Utility, and E-Commerce Domains
OFFICIAL_ENTITIES = [
    # 1. Major Public Sector Banks
    {"name": "State Bank of India (SBI)", "brand": "sbi", "domains": ["sbi.co.in", "onlinesbi.sbi", "bank.sbi", "onlinesbi.com"]},
    {"name": "Punjab National Bank", "brand": "pnb", "domains": ["pnbindia.in", "pnb.bank"]},
    {"name": "Bank of Baroda", "brand": "bankofbaroda", "domains": ["bankofbaroda.in", "bankofbaroda.com", "bob.bank"]},
    {"name": "Canara Bank", "brand": "canarabank", "domains": ["canarabank.com", "canarabank.in"]},
    {"name": "Union Bank of India", "brand": "unionbank", "domains": ["unionbankofindia.co.in", "unionbank.bank"]},
    {"name": "Bank of India", "brand": "bankofindia", "domains": ["bankofindia.co.in", "bankofindia.com"]},
    {"name": "Indian Bank", "brand": "indianbank", "domains": ["indianbank.in", "indianbank.co.in"]},
    {"name": "Central Bank of India", "brand": "centralbank", "domains": ["centralbankofindia.co.in"]},
    {"name": "Indian Overseas Bank", "brand": "iob", "domains": ["iob.in", "iobnet.co.in"]},
    {"name": "UCO Bank", "brand": "ucobank", "domains": ["ucobank.com"]},
    {"name": "Bank of Maharashtra", "brand": "bankofmaharashtra", "domains": ["bankofmaharashtra.in"]},
    {"name": "Punjab & Sind Bank", "brand": "punjabandsind", "domains": ["punjabandsindbank.co.in"]},

    # 2. Major Private Sector Banks
    {"name": "HDFC Bank", "brand": "hdfc", "domains": ["hdfcbank.com", "hdfc.com", "hdfcbank.co.in"]},
    {"name": "ICICI Bank", "brand": "icici", "domains": ["icicibank.com", "icicibank.co.in"]},
    {"name": "Axis Bank", "brand": "axis", "domains": ["axisbank.com", "axisbank.co.in"]},
    {"name": "Kotak Mahindra Bank", "brand": "kotak", "domains": ["kotak.com", "kotakbank.com"]},
    {"name": "IndusInd Bank", "brand": "indusind", "domains": ["indusind.com"]},
    {"name": "Yes Bank", "brand": "yesbank", "domains": ["yesbank.in"]},
    {"name": "IDFC FIRST Bank", "brand": "idfcfirst", "domains": ["idfcfirstbank.com"]},
    {"name": "Federal Bank", "brand": "federalbank", "domains": ["federalbank.co.in"]},
    {"name": "South Indian Bank", "brand": "southindianbank", "domains": ["southindianbank.com"]},
    {"name": "Bandhan Bank", "brand": "bandhanbank", "domains": ["bandhanbank.com"]},
    {"name": "RBL Bank", "brand": "rblbank", "domains": ["rblbank.com"]},
    {"name": "City Union Bank", "brand": "cityunionbank", "domains": ["cityunionbank.com"]},
    {"name": "Karur Vysya Bank", "brand": "kvb", "domains": ["kvb.co.in"]},
    {"name": "Karnataka Bank", "brand": "karnatakabank", "domains": ["karnatakabank.com"]},
    {"name": "Jammu & Kashmir Bank", "brand": "jkbank", "domains": ["jkbank.com"]},
    {"name": "AU Small Finance Bank", "brand": "aubank", "domains": ["aubank.in"]},
    {"name": "Equitas Small Finance Bank", "brand": "equitasbank", "domains": ["equitasbank.com"]},

    # 3. UPI Apps, Fintech & Payments Banks
    {"name": "Paytm / Paytm Payments Bank", "brand": "paytm", "domains": ["paytm.com", "paytmbank.com"]},
    {"name": "PhonePe", "brand": "phonepe", "domains": ["phonepe.com"]},
    {"name": "Google Pay", "brand": "gpay", "domains": ["pay.google.com", "google.com"]},
    {"name": "BHIM / NPCI", "brand": "bhim", "domains": ["bhimupi.org.in", "npci.org.in"]},
    {"name": "NPCI", "brand": "npci", "domains": ["npci.org.in"]},
    {"name": "Amazon Pay", "brand": "amazonpay", "domains": ["amazon.in", "amazonpay.in"]},
    {"name": "CRED", "brand": "cred", "domains": ["cred.club"]},
    {"name": "MobiKwik", "brand": "mobikwik", "domains": ["mobikwik.com"]},
    {"name": "Freecharge", "brand": "freecharge", "domains": ["freecharge.in"]},
    {"name": "Airtel Payments Bank", "brand": "airtelbank", "domains": ["airtelbank.com", "airtel.in"]},
    {"name": "Jio Payments Bank", "brand": "jiopay", "domains": ["jiopaymentsbank.com", "jio.com"]},
    {"name": "India Post Payments Bank (IPPB)", "brand": "ippb", "domains": ["ippbonline.com"]},
    {"name": "Fino Payments Bank", "brand": "finobank", "domains": ["finobank.com"]},

    # 4. Indian Government & Welfare Portals
    {"name": "National Cybercrime Reporting Portal (1930)", "brand": "cybercrime", "domains": ["cybercrime.gov.in"]},
    {"name": "UIDAI (Aadhaar)", "brand": "uidai", "domains": ["uidai.gov.in"]},
    {"name": "Income Tax Department", "brand": "incometax", "domains": ["incometax.gov.in"]},
    {"name": "Ministry of Finance", "brand": "finmin", "domains": ["finmin.nic.in"]},
    {"name": "Reserve Bank of India (RBI)", "brand": "rbi", "domains": ["rbi.org.in"]},
    {"name": "National Portal of India", "brand": "india_gov", "domains": ["india.gov.in"]},
    {"name": "EPFO (Employees' Provident Fund)", "brand": "epfindia", "domains": ["epfindia.gov.in"]},
    {"name": "Parivahan Sewa", "brand": "parivahan", "domains": ["parivahan.gov.in"]},
    {"name": "Passport Seva", "brand": "passportindia", "domains": ["passportindia.gov.in"]},
    {"name": "DigiLocker", "brand": "digilocker", "domains": ["digilocker.gov.in"]},
    {"name": "UMANG", "brand": "umang", "domains": ["umang.gov.in", "web.umang.gov.in"]},
    {"name": "IRCTC (Indian Railways)", "brand": "irctc", "domains": ["irctc.co.in"]},
    {"name": "PM Kisan Samman Nidhi", "brand": "pmkisan", "domains": ["pmkisan.gov.in"]},
    {"name": "PM Awas Yojana", "brand": "pmay", "domains": ["pmaymis.gov.in"]},
    {"name": "Ayushman Bharat / NHA", "brand": "pmjay", "domains": ["pmjay.gov.in", "nha.gov.in"]},
    {"name": "CoWIN Portal", "brand": "cowin", "domains": ["cowin.gov.in"]},
    {"name": "National Crime Records Bureau", "brand": "ncrb", "domains": ["ncrb.gov.in"]},
    {"name": "Central Board of Direct Taxes", "brand": "cbdt", "domains": ["incometaxindia.gov.in"]},

    # 5. State Electricity Boards (DISCOMs)
    {"name": "BESCOM (Bangalore Electricity)", "brand": "bescom", "domains": ["bescom.karnataka.gov.in", "bescom.org"]},
    {"name": "TSSPDCL (Telangana Southern Power)", "brand": "tsspdcl", "domains": ["tssouthernpower.com"]},
    {"name": "TSNPDCL (Telangana Northern Power)", "brand": "tsnpdcl", "domains": ["tsnpdcl.in"]},
    {"name": "APCPDCL (Andhra Central Power)", "brand": "apcpdcl", "domains": ["apcpdcl.in"]},
    {"name": "APSPDCL (Andhra Southern Power)", "brand": "apspdcl", "domains": ["apspdcl.in"]},
    {"name": "UPPCL (Uttar Pradesh Power)", "brand": "uppcl", "domains": ["upenergy.in"]},
    {"name": "TNEB / TANGEDCO (Tamil Nadu Power)", "brand": "tneb", "domains": ["tangedco.gov.in"]},
    {"name": "MSEDCL (Maharashtra Mahavitaran)", "brand": "msedcl", "domains": ["mahadiscom.in"]},
    {"name": "Tata Power", "brand": "tatapower", "domains": ["tatapower.com"]},
    {"name": "Adani Electricity Mumbai", "brand": "adanielectricity", "domains": ["adanielectricity.com"]},
    {"name": "BSES Delhi (Yamuna & Rajdhani)", "brand": "bses", "domains": ["bsesdelhi.com"]},
    {"name": "PSPCL (Punjab State Power)", "brand": "pspcl", "domains": ["pspcl.in"]},
    {"name": "WBSEDCL (West Bengal Power)", "brand": "wbsedcl", "domains": ["wbsedcl.in"]},
    {"name": "DHBVN (Dakshin Haryana Bijli)", "brand": "dhbvn", "domains": ["dhbvn.org.in"]},
    {"name": "UHBVN (Uttar Haryana Bijli)", "brand": "uhbvn", "domains": ["uhbvn.org.in"]},
    {"name": "KSEB (Kerala State Electricity)", "brand": "kseb", "domains": ["kseb.in"]},
    {"name": "CESC (Calcutta Electricity)", "brand": "cesc", "domains": ["cesc.co.in"]},

    # 6. E-Commerce & Logistics / Couriers
    {"name": "Amazon India", "brand": "amazon", "domains": ["amazon.in"]},
    {"name": "Flipkart", "brand": "flipkart", "domains": ["flipkart.com"]},
    {"name": "Meesho", "brand": "meesho", "domains": ["meesho.com"]},
    {"name": "OLX India", "brand": "olx", "domains": ["olx.in"]},
    {"name": "Quikr", "brand": "quikr", "domains": ["quikr.com"]},
    {"name": "FedEx India", "brand": "fedex", "domains": ["fedex.com"]},
    {"name": "Blue Dart Express", "brand": "bluedart", "domains": ["bluedart.com"]},
    {"name": "India Post", "brand": "indiapost", "domains": ["indiapost.gov.in"]},
    {"name": "DHL Express", "brand": "dhl", "domains": ["dhl.com"]},
    {"name": "Delhivery", "brand": "delhivery", "domains": ["delhivery.com"]},
    {"name": "DTDC Express", "brand": "dtdc", "domains": ["dtdc.in"]}
]

# Set of all registered official domains for O(1) membership check
ALL_OFFICIAL_DOMAINS: Set[str] = {
    dom.lower()
    for entity in OFFICIAL_ENTITIES
    for dom in entity["domains"]
}

SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "is.gd", "cutt.ly", "t.co", "rb.gy",
    "ow.ly", "tiny.cc", "rebrand.ly", "shorturl.at", "bl.ink"
}

SUSPICIOUS_TLDS = {
    "top", "xyz", "click", "site", "online", "club", "biz",
    "live", "loan", "work", "vip", "gq", "cf", "tk", "ml", "cc",
    "buzz", "rest", "support", "link", "info", "monster", "cfd"
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
    Features strict registered-domain matching and 88 Indian brand definitions.
    """

    @property
    def all_legitimate_domains(self) -> set:
        return ALL_OFFICIAL_DOMAINS

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

        host_no_port = netloc.split(":")[0]

        # Check if URL is an authorized official domain
        is_official = (
            host_no_port in ALL_OFFICIAL_DOMAINS or
            registered_domain in ALL_OFFICIAL_DOMAINS or
            any(host_no_port == off or host_no_port.endswith("." + off) for off in ALL_OFFICIAL_DOMAINS)
        )
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

        # 5. Strict Registered-Domain Brand Impersonation & Typosquatting
        if not is_official:
            for entity in OFFICIAL_ENTITIES:
                brand = entity["brand"].lower()
                official_domains = entity["domains"]

                # Subdomain trick: e.g., "sbi.co.in.verify-login.xyz"
                brand_in_sub = brand in subdomain or any(off in subdomain for off in official_domains)
                brand_in_dom = brand in domain

                if brand_in_sub or brand_in_dom:
                    score += 50.0
                    signals.append({
                        "signal": f"Brand Typosquatting / Impersonation: URL mimics '{entity['name']}' brand, but destination '{registered_domain}' is NOT an authorized domain ({', '.join(official_domains[:2])}).",
                        "source_module": "URL_SCANNER",
                        "weight": 50.0,
                        "severity": "CRITICAL"
                    })
                    break
                elif len(domain) >= 3 and len(brand) >= 3:
                    # Check Levenshtein distance on domain stem
                    for off in official_domains:
                        off_stem = off.split(".")[0]
                        dist = distance.Levenshtein.distance(domain, off_stem)
                        if 0 < dist <= 2 and len(domain) > 2 and len(off_stem) > 2:
                            score += 45.0
                            signals.append({
                                "signal": f"Typosquatting Detected: Domain '{domain}' is {dist} character edit distance from official '{off_stem}' ({entity['name']}).",
                                "source_module": "URL_SCANNER",
                                "weight": 45.0,
                                "severity": "CRITICAL"
                            })
                            break
                    if signals and signals[-1]["severity"] == "CRITICAL":
                        break

        # 6. Suspicious TLD check
        if suffix in SUSPICIOUS_TLDS and not is_official:
            score += 25.0
            signals.append({
                "signal": f"High-Risk Top-Level Domain: Domain uses '.{suffix}', a TLD heavily associated with disposable phishing campaigns.",
                "source_module": "URL_SCANNER",
                "weight": 25.0,
                "severity": "HIGH"
            })

        # 7. Excessive Subdomains
        sub_parts = [p for p in subdomain.split(".") if p]
        if len(sub_parts) >= 2 and not is_official:
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
        if (hyphen_count >= 2 or (hyphen_count >= 1 and digit_count >= 2)) and not is_official:
            score += 20.0
            signals.append({
                "signal": f"Hyphen/Digit Stuffing: Domain '{domain}' contains {hyphen_count} hyphens and {digit_count} digits.",
                "source_module": "URL_SCANNER",
                "weight": 20.0,
                "severity": "MEDIUM"
            })

        # 9. Non-HTTPS scheme
        if parsed.scheme.lower() == "http" and not is_official:
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
        if found_keywords and not is_official:
            weight = min(25.0, len(found_keywords) * 8.0)
            score += weight
            signals.append({
                "signal": f"Phishing Keywords in URL: Found suspicious keywords ({', '.join(found_keywords[:4])}) in URL structure.",
                "source_module": "URL_SCANNER",
                "weight": weight,
                "severity": "MEDIUM"
            })

        # 11. Excessively long URL
        if len(raw_url) > 75 and not is_official:
            score += 10.0
            signals.append({
                "signal": f"Excessive URL Length: URL is {len(raw_url)} characters long, which may hide suspicious query parameters.",
                "source_module": "URL_SCANNER",
                "weight": 10.0,
                "severity": "LOW"
            })

        # Verified Official Domain recognition
        if is_official and score == 0.0:
            signals.append({
                "signal": f"Verified Official Domain: '{registered_domain}' belongs to authorized official entity registry.",
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
