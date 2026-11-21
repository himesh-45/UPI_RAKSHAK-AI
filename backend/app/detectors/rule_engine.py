import re
from typing import List, Dict, Any

# Pattern definitions for Rule-Based Safety Layer

# Advisory / Negative phrasing (Genuine bank warnings)
GENUINE_ADVISORY_PATTERNS = [
    re.compile(r'(?i)\b(?:never|do not|don\'t|kabhi bhi nahi|eppudu)\s*(?:share|tell|disclose|give|batao|share cheyavaddu)\b.*?\b(?:otp|pin|cvv|password)\b'),
    re.compile(r'(?i)\b(?:bank|staff|employee)\s*(?:never|does not)\s*(?:ask|call)\b.*?\b(?:otp|pin|cvv|password)\b'),
    re.compile(r'(?i)(?:kabhi bhi apna otp|otp kisi se sajha na kare|evaritho share cheyavoddu|ఎవరితోనూ పంచుకోవద్దు|ఎవరికీ చెప్పవద్దు|किसी से साझा न करें|ఓటీపీ పంచుకోవద్దు)'),
    re.compile(r'(?i)\b(?:if not done by you|report fraud to|call helpline)\b')
]

# 1. OTP / PIN / CVV Request Patterns (Theft attempt)
OTP_REQUEST_PATTERNS = [
    re.compile(r'(?i)\b(?:enter|share|send|submit|tell|provide|verify|batao|dale|cheppandi|enter cheyandi)\b.*?\b(?:otp|upi pin|pin|cvv|password|passcode|secret code)\b'),
    re.compile(r'(?i)\b(?:otp|upi pin|pin|cvv|password)\b.*?\b(?:share kare|batao|cheppandi|bheje|submit kare)\b'),
    re.compile(r'(?i)\b(?:to (?:authenticate|stop|cancel|freeze|claim|verify))\b.*?\b(?:enter|share)\b.*?\b(?:otp|pin|cvv)\b')
]

# 2. Collect Request Trick (Receiving money NEVER requires PIN)
COLLECT_PIN_PATTERNS = [
    re.compile(r'(?i)\b(?:enter|put|type|kottandi|dale)\b.*?\b(?:pin|upi pin)\b.*?\b(?:to (?:receive|claim|collect|get)|paise lene|dabbulu pondadaniki)\b'),
    re.compile(r'(?i)\b(?:accept|approve)\b.*?\b(?:collect request|request)\b.*?\b(?:enter|put)?\b.*?\b(?:pin|upi pin)\b'),
    re.compile(r'(?i)\b(?:receive|get|claim)\b.*?\b(?:cashback|refund|money|reward)\b.*?\b(?:enter|approve)\b.*?\b(?:upi pin|pin)\b'),
    re.compile(r'(?i)\b(?:కలెక్ట్ రిక్వెస్ట్|డబ్బులు పొందడానికి).*?(?:పిన్|pin)\b')
]

# 3. Urgency & Account-Block Threat Patterns
URGENCY_BLOCK_PATTERNS = [
    re.compile(r'(?i)\b(?:will be|is|account)\s*(?:blocked|suspended|deactivated|closed|frozen|hold|disconnected|cut off)\b.*?\b(?:tonight|today|immediately|within \d+ hours|in \d+ hours|turant|ventane)\b'),
    re.compile(r'(?i)\b(?:electricity|power|power line|current)\b.*?\b(?:disconnected|cut|band)\b.*?\b(?:tonight|today|9:30|immediate|turant)\b'),
    re.compile(r'(?i)\b(?:turant|ventane|urgent|immediately)\b.*?\b(?:update|verify|call|contact|unblock)\b'),
    re.compile(r'(?i)(?:आज रात|24 घंटे|నిలిపివేయబడుతుంది|బ్లాక్ చేయబడుతుంది|ఈ రాత్రి|రద్దు|వెంటనే|నిలిపివేయబడింది|తక్షణమే)')
]

# 4. Remote-Access Application Requests
REMOTE_APP_PATTERNS = [
    re.compile(r'(?i)\b(?:install|download|open|chalu kare|install cheyandi)\b.*?\b(?:anydesk|teamviewer|quicksupport|rustdesk|ultraviewer|airdroid)\b'),
    re.compile(r'(?i)\b(?:anydesk|teamviewer|quicksupport|rustdesk|ultraviewer)\b.*?\b(?:code|access|connect|screen share|share)\b')
]

# 5. Link + Credential / Verification Requests
LINK_PATTERN = re.compile(r'(?i)\b(?:https?://|hxxps?://|bit\.ly/|tinyurl\.com/|is\.gd/|cutt\.ly/|[a-zA-Z0-9-]+\.(?:top|xyz|click|site|online|club|biz)/)\S*')
VERIFY_CREDENTIAL_WORDS = [
    re.compile(r'(?i)\b(?:kyc|verify|update|authenticate|reactivate|aadhaar|pan card|credentials|unfreeze)\b'),
    re.compile(r'(?i)\b(?:केवाईसी|अपडेट|वेबसाइट|లింక్|నవీకరించండి|సమర్పించండి)\b')
]

# 7. Disconnection / Block threat with personal phone contact or link
PHONE_CONTACT_PATTERN = re.compile(r'(?i)(?:call|contact|संपर्क|कॉल|సంప్రదించండి|ఫోన్).*?(?:\+91[-\s]?)?[6-9]\d{2,5}[-\s]?\d{3,5}')

LOTTERY_FEE_PATTERNS = [
    re.compile(r'(?i)\b(?:won|winner|lottery|lucky draw|prize|kbc|giveaway)\b.*?\b(?:lakh|crore|car|iphone)\b'),
    re.compile(r'(?i)\b(?:registration fee|processing fee|tax|shipping fee|refundable)\b.*?\b(?:pay|deposit|upi|transfer)\b')
]

class RuleSafetyEngine:
    def evaluate(self, text: str) -> Dict[str, Any]:
        """
        Evaluates input text against deterministic safety rules.
        Returns matched signals, rule score boost, and override triggers.
        """
        matched_rules = []
        is_genuine_alert = False
        has_otp_request = False
        has_urgency = False
        has_link = False
        has_collect_trick = False
        has_remote_app = False
        has_lottery = False

        # First: check if text has genuine advisory warning
        advisory_matches = [p.pattern for p in GENUINE_ADVISORY_PATTERNS if p.search(text)]
        if advisory_matches:
            is_genuine_alert = True
            matched_rules.append({
                "signal": "Legitimate Safety Advisory: Message explicitly warns NEVER to share OTP/PIN.",
                "source_module": "RULE_SAFETY_LAYER",
                "weight": -30.0,
                "severity": "INFO"
            })

        # 1. OTP / PIN theft check
        # Only treat as theft if not purely a genuine advisory
        if not is_genuine_alert or any("share" in text.lower() and "never" not in text.lower() for _ in [1]):
            for p in OTP_REQUEST_PATTERNS:
                if p.search(text):
                    has_otp_request = True
                    matched_rules.append({
                        "signal": "Credential Theft Attempt: Explicit instruction to share or input OTP / UPI PIN / CVV / Password.",
                        "source_module": "RULE_SAFETY_LAYER",
                        "weight": 40.0,
                        "severity": "CRITICAL"
                    })
                    break

        # 2. Collect Request Trick
        for p in COLLECT_PIN_PATTERNS:
            if p.search(text):
                has_collect_trick = True
                matched_rules.append({
                    "signal": "UPI Collect Fraud Rule: Request claims you must enter a PIN or accept a collect request to receive money or cashback. In UPI architecture, receiving money NEVER requires entering a PIN.",
                    "source_module": "RULE_SAFETY_LAYER",
                    "weight": 45.0,
                    "severity": "CRITICAL"
                })
                break

        # 3. Urgency / Disconnection / Block threat
        for p in URGENCY_BLOCK_PATTERNS:
            if p.search(text):
                has_urgency = True
                matched_rules.append({
                    "signal": "Artificial Urgency & Threat: Coercive ultimatum threatening immediate account block or utility power cut.",
                    "source_module": "RULE_SAFETY_LAYER",
                    "weight": 25.0,
                    "severity": "HIGH"
                })
                break

        # 4. Remote Access App
        for p in REMOTE_APP_PATTERNS:
            if p.search(text):
                has_remote_app = True
                matched_rules.append({
                    "signal": "Remote Device Takeover: Instructions to download remote desktop apps (AnyDesk/TeamViewer/QuickSupport) to access device.",
                    "source_module": "RULE_SAFETY_LAYER",
                    "weight": 45.0,
                    "severity": "CRITICAL"
                })
                break

        # 5. Link + Verification / KYC credentials
        links_found = LINK_PATTERN.findall(text)
        if links_found:
            has_link = True
            has_verify = any(p.search(text) for p in VERIFY_CREDENTIAL_WORDS)
            if has_verify or has_otp_request or has_urgency:
                matched_rules.append({
                    "signal": f"Deceptive Link with Verification Prompt: Contains suspicious link ({links_found[0][:30]}...) requesting credential/KYC verification.",
                    "source_module": "RULE_SAFETY_LAYER",
                    "weight": 35.0,
                    "severity": "HIGH"
                })

        # 6. Lottery / Prize fee
        for p in LOTTERY_FEE_PATTERNS:
            if p.search(text):
                has_lottery = True
                matched_rules.append({
                    "signal": "Advance-Fee Lottery Lure: Claims large monetary prize or car lottery with requirement to pay processing fees.",
                    "source_module": "RULE_SAFETY_LAYER",
                    "weight": 35.0,
                    "severity": "HIGH"
                })
                break

        # 7. Disconnection / Block threat with personal phone contact
        has_phone_threat = False
        if has_urgency and PHONE_CONTACT_PATTERN.search(text):
            has_phone_threat = True
            matched_rules.append({
                "signal": "Coercive Threat with Personal Phone Contact: Urgency ultimatum directing victim to call a personal mobile number.",
                "source_module": "RULE_SAFETY_LAYER",
                "weight": 35.0,
                "severity": "HIGH"
            })

        # Hard Override evaluation:
        # OTP request + Urgency => Immediate HIGH RISK override
        # Collect request PIN trick => Immediate HIGH RISK override
        # Remote app + urgency/refund => Immediate HIGH RISK override
        # Utility power disconnection threat + phone/link => Immediate HIGH RISK override
        hard_override_high_risk = False
        override_reason = None

        is_utility_threat = has_urgency and (has_phone_threat or has_link) and any(
            kw in text.lower() for kw in ["बिजली", "electricity", "power", "విద్యుత్", "bill", "disconnect", "कट", "బిల్లు"]
        )

        if has_otp_request and (has_urgency or has_link):
            hard_override_high_risk = True
            override_reason = "Hard Override Triggered: Coercive urgency/link combined with credential (OTP/PIN) request."
        elif has_collect_trick:
            hard_override_high_risk = True
            override_reason = "Hard Override Triggered: UPI collect request trick to steal funds (Receiving money never requires a PIN)."
        elif has_remote_app:
            hard_override_high_risk = True
            override_reason = "Hard Override Triggered: Remote access application installation request."
        elif is_utility_threat:
            hard_override_high_risk = True
            override_reason = "Hard Override Triggered: Utility disconnection threat directing contact to unauthorized mobile/link."

        # Compute rule sub-score
        base_rule_score = sum(r["weight"] for r in matched_rules)
        if is_genuine_alert and not hard_override_high_risk:
            base_rule_score = max(0.0, base_rule_score)

        return {
            "matched_rules": matched_rules,
            "rule_score": max(0.0, min(100.0, base_rule_score)),
            "hard_override_high_risk": hard_override_high_risk,
            "override_reason": override_reason,
            "is_genuine_alert": is_genuine_alert,
            "signals_detected": {
                "has_otp_request": has_otp_request,
                "has_collect_trick": has_collect_trick,
                "has_urgency": has_urgency,
                "has_link": has_link,
                "has_remote_app": has_remote_app,
                "has_lottery": has_lottery
            }
        }

rule_engine = RuleSafetyEngine()
