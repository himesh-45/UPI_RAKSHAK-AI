import re
from typing import List, Dict, Any, Tuple

# Advisory / Negative phrasing (Genuine bank warnings & Delivery notices)
GENUINE_ADVISORY_PATTERNS = [
    re.compile(r'(?i)\b(?:never|do not|don\'t|should not|must not|cannot)\s+(?:share|disclose|give|tell|reveal)\b.*?\b(?:otp|pin|cvv|password|passcode)\b'),
    re.compile(r'(?i)\b(?:bank|staff|employee|official|executive)\s+(?:never|does not|will never|never asks?)\s+(?:for|to ask|call for)\b.*?\b(?:otp|pin|cvv|password)\b'),
    re.compile(r'(?i)\b(?:share|give)\s+(?:the\s+)?otp\b.*?\b(?:only\s+(?:upon|after|at|when)|physically received|at time of delivery|delivery agent)\b'),
    re.compile(r'(?i)\b(?:delivery|package|order|courier)\b.*?\b(?:share\s+otp\s+only|valid\s+upon\s+receipt)\b'),
    re.compile(r'(?i)(?:kabhi bhi apna otp|otp kisi se sajha na kare|kisi ko na bataye|kisi ke sath share na kare|kisi se share na kare|evaritho share cheyavoddu|evariki cheppavaddu)'),
    re.compile(r'(?i)(?:ఎవరితోనూ పంచుకోవద్దు|ఎవరికీ చెప్పవద్దు|ఓటీపీ పంచుకోవద్దు|ఎవరితోనూ పంచుకోకండి|ఓటీపీ ఎవరికీ చెప్పకండి)'),
    re.compile(r'(?i)(?:किसी\s*(?:से|के\s+साथ)\s*(?:साझा|शेयर)\s*(?:न|मत)\s*करें|साझा\s+(?:न|मत)\s+करें|शेयर\s+(?:न|मत)\s+करें|किसी को न बताएं|बैंक\s+कभी.*?नहीं\s+मांगता|बैंक कभी ओटीपी नहीं मांगता|बैंक कभी पिन नहीं मांगता)'),
    re.compile(r'(?i)\b(?:if not done by you|report fraud to|call helpline|sms block to)\b')
]

# Negation prefixes within 6 words of credential action
NEGATION_PREFIX_REGEX = re.compile(
    r'(?i)\b(?:never|do not|don\'t|not|never ask|never asks|kabhi nahi|kabhi na|na kare|cheyavoddu|cheyakandi|eppudu cheyavoddu|evariki cheppavaddu|मत|नहीं|నద్దు|వద్దు|చెప్పవద్దు|పంచుకోవద్దు)\b'
)

# 1. Credential / OTP / PIN Theft Patterns (Active requests)
OTP_REQUEST_PATTERNS = [
    re.compile(r'(?i)\b(?:share|send|submit|tell|provide|verify|enter|forward|input)\b\s+(?:the\s+|your\s+|this\s+|received\s+)?(?:6-digit\s+|secret\s+)?\b(?:otp|upi pin|atm pin|pin|cvv|password|passcode|secret code)\b'),
    re.compile(r'(?i)\b(?:enter|put|submit|type|enter cheyandi|dale|bataye|cheppandi)\b.*?\b(?:otp|upi pin|atm pin|pin|cvv|password)\b.*?\b(?:to (?:authenticate|cancel|stop|freeze|claim|verify|reactivate)|par|lo)\b'),
    re.compile(r'(?i)\b(?:otp|upi pin|pin|cvv|password)\b.*?\b(?:batao|bataye|bheje|share kare|cheppandi|share cheyandi)\b'),
    re.compile(r'(?i)(?:ఓటీపీ నమోదు చేయండి|పిన్ నమోదు చేయండి|ఓటీపీ చెప్పండి|पिन दर्ज करें|ओटीपी बताएं|ओटीपी साझा करें)')
]

# 2. Collect Request Trick (Receiving money NEVER requires PIN)
COLLECT_PIN_PATTERNS = [
    re.compile(r'(?i)\b(?:enter|put|type|kottandi|dale|darj kare)\b.*?\b(?:pin|upi pin)\b.*?\b(?:to (?:receive|claim|collect|get|credit)|paise lene|dabbulu pondadaniki|paise paane)\b'),
    re.compile(r'(?i)\b(?:accept|approve)\b.*?\b(?:collect request|request|mandate)\b.*?\b(?:enter|put|type)?\b.*?\b(?:pin|upi pin)\b'),
    re.compile(r'(?i)\b(?:receive|get|claim)\b.*?\b(?:cashback|refund|money|reward|advance|token)\b.*?\b(?:enter|approve|accept)\b.*?\b(?:upi pin|pin)\b'),
    re.compile(r'(?i)(?:కలెక్ట్ రిక్వెస్ట్|డబ్బులు పొందడానికి|రివార్డ్ పొందడానికి).*?(?:పిన్|pin|upi pin)'),
    re.compile(r'(?i)(?:पैसे पाने के लिए|रिफंड पाने के लिए|कैशबैक पाने के लिए).*?(?:पिन दर्ज करें|पिन डालें|pin)')
]

# 3. Urgency & Account-Block Threat Patterns
URGENCY_BLOCK_PATTERNS = [
    re.compile(r'(?i)\b(?:will be|is|account)\s*(?:blocked|suspended|deactivated|closed|frozen|hold|disconnected|cut off)\b.*?\b(?:tonight|today|immediately|within \d+ hours|in \d+ hours|turant|ventane)\b'),
    re.compile(r'(?i)\b(?:electricity|power|power line|current|power supply)\b.*?\b(?:disconnected|cut|band|katt)\b.*?\b(?:tonight|today|9:30|immediate|turant|ratridi)\b'),
    re.compile(r'(?i)\b(?:turant|ventane|urgent|immediately)\b.*?\b(?:update|verify|call|contact|unblock|clear bill)\b'),
    re.compile(r'(?i)(?:आज रात|24 घंटे|10 बजे|9:30|निलिपिవేయబడుతుంది|బ్లాక్ చేయబడుతుంది|ఈ రాత్రి|రద్దు|వెంటనే|నిలిపివేయబడింది|తక్షణమే|काट दी जाएगी)')
]

# 4. Remote-Access Application Requests
REMOTE_APP_PATTERNS = [
    re.compile(r'(?i)\b(?:install|download|open|chalu kare|install cheyandi)\b.*?\b(?:anydesk|teamviewer|quicksupport|rustdesk|ultraviewer|airdroid)\b'),
    re.compile(r'(?i)\b(?:anydesk|teamviewer|quicksupport|rustdesk|ultraviewer)\b.*?\b(?:code|access|connect|screen share|share|partner id|9-digit)\b')
]

# 5. Link + Credential / Verification Requests
LINK_PATTERN = re.compile(r'(?i)\b(?:https?://|hxxps?://|bit\.ly/|tinyurl\.com/|is\.gd/|cutt\.ly/|[a-zA-Z0-9-]+\.(?:top|xyz|click|site|online|club|biz)/)\S*')
VERIFY_CREDENTIAL_WORDS = [
    re.compile(r'(?i)\b(?:kyc|verify|update|authenticate|reactivate|aadhaar|pan card|credentials|unfreeze)\b'),
    re.compile(r'(?i)\b(?:केवाईसी|अपडेट|वेबसाइट|लिंक|నవీకరించండి|సమర్పించండి|ధృవీకరించండి)\b')
]

# 6. Disconnection / Block threat with personal phone contact or link
PHONE_CONTACT_PATTERN = re.compile(r'(?i)(?:call|contact|संपर्क|कॉल|సంప్రదించండి|ఫోన్).*?(?:\+91[-\s]?)?[6-9]\d{2,5}[-\s]?\d{3,5}')

# 7. Advance-fee lottery patterns
LOTTERY_FEE_PATTERNS = [
    re.compile(r'(?i)\b(?:won|winner|lottery|lucky draw|prize|kbc|giveaway)\b.*?\b(?:lakh|crore|car|iphone)\b'),
    re.compile(r'(?i)\b(?:registration fee|processing fee|tax|shipping fee|refundable|file charge)\b.*?\b(?:pay|deposit|upi|transfer)\b')
]

# 8. Digital Arrest / Customs / Police threat
DIGITAL_ARREST_PATTERNS = [
    re.compile(r'(?i)\b(?:narcotics|customs|cbi|police|dcp|crime branch|digital arrest|contraband|mdma|drugs)\b.*?\b(?:parcel|arrest warrant|video call|fir registered|skype)\b'),
    re.compile(r'(?i)(?:डिजिटल अरेस्ट|नारकोटिक्स|कस्टम्स|वारंट|డ్రగ్స్|కస్టమ్స్|ఎఫ్‌ఐఆర్|అరెస్ట్)')
]

# 9. Loan Extortion / Contact Book Harassment
LOAN_EXTORTION_PATTERNS = [
    re.compile(r'(?i)\b(?:contacts|relatives|family|gallery|photo|photos)\b.*?\b(?:social media|share|send|defame|leak|post|morphed)\b'),
    re.compile(r'(?i)(?:मॉर्फ की गई|तस्वीरें|रिश्तेदारों|badnaam|contacts andariki|photo contacts)')
]

class RuleSafetyEngine:
    def check_negation(self, text: str, match_span: Tuple[int, int]) -> bool:
        """
        Inspects preceding 80 characters for negation words ("never", "do not", "bank never asks").
        """
        start, _ = match_span
        context_start = max(0, start - 80)
        prefix = text[context_start:start].lower()
        if NEGATION_PREFIX_REGEX.search(prefix):
            return True
        return False

    def evaluate(self, text: str) -> Dict[str, Any]:
        """
        Evaluates input text against deterministic safety rules with context-aware negation.
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
        has_digital_arrest = False
        has_loan_extortion = False

        # First: check if text has genuine advisory warning
        advisory_matches = [p for p in GENUINE_ADVISORY_PATTERNS if p.search(text)]
        if advisory_matches:
            is_genuine_alert = True
            matched_rules.append({
                "signal": "Legitimate Safety Advisory: Message explicitly warns NEVER to share OTP/PIN.",
                "source_module": "RULE_SAFETY_LAYER",
                "weight": -40.0,
                "severity": "INFO"
            })

        # 1. OTP / PIN theft check (with strict negation filtering)
        for p in OTP_REQUEST_PATTERNS:
            m = p.search(text)
            if m:
                # Check if this match is negated by context
                if not self.check_negation(text, m.span()) and not is_genuine_alert:
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
            m = p.search(text)
            if m and not self.check_negation(text, m.span()):
                has_collect_trick = True
                matched_rules.append({
                    "signal": "UPI Collect Fraud Rule: Request claims you must enter a PIN or accept a collect request to receive money. Receiving money NEVER requires entering a PIN.",
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

        # 7. Digital Arrest / Customs Coercion
        for p in DIGITAL_ARREST_PATTERNS:
            if p.search(text):
                has_digital_arrest = True
                matched_rules.append({
                    "signal": "Digital Arrest / Law Enforcement Impersonation: Coercive extortion claiming illegal parcel seized by customs/police.",
                    "source_module": "RULE_SAFETY_LAYER",
                    "weight": 50.0,
                    "severity": "CRITICAL"
                })
                break

        # 8. Loan Extortion & Harassment
        for p in LOAN_EXTORTION_PATTERNS:
            if p.search(text):
                has_loan_extortion = True
                matched_rules.append({
                    "signal": "Predatory Loan Extortion: Blackmail threatening to circulate morphed photos or defame contacts.",
                    "source_module": "RULE_SAFETY_LAYER",
                    "weight": 50.0,
                    "severity": "CRITICAL"
                })
                break

        # 9. Disconnection / Block threat with personal phone contact
        has_phone_threat = False
        if has_urgency and PHONE_CONTACT_PATTERN.search(text):
            has_phone_threat = True
            matched_rules.append({
                "signal": "Coercive Threat with Personal Phone Contact: Urgency ultimatum directing victim to call a personal mobile number.",
                "source_module": "RULE_SAFETY_LAYER",
                "weight": 35.0,
                "severity": "HIGH"
            })

        # Hard Override evaluation
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
        elif has_digital_arrest:
            hard_override_high_risk = True
            override_reason = "Hard Override Triggered: Digital arrest extortion threat."
        elif has_loan_extortion:
            hard_override_high_risk = True
            override_reason = "Hard Override Triggered: Predatory loan extortion threat."

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
                "has_lottery": has_lottery,
                "has_digital_arrest": has_digital_arrest,
                "has_loan_extortion": has_loan_extortion
            }
        }

rule_engine = RuleSafetyEngine()
