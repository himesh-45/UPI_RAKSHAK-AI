import re
from typing import List, Dict, Any, Tuple

# Advisory / Negative phrasing (Genuine bank warnings & Delivery notices)
GENUINE_ADVISORY_PATTERNS = [
    re.compile(r'(?i)\b(?:never|do not|don\'t|should not|must not|cannot)\s+(?:share|disclose|give|tell|reveal)\b.*?\b(?:otp|pin|cvv|password|passcode)\b'),
    re.compile(r'(?i)\b(?:bank|staff|employee|official|executive)\s+(?:never|does not|will never|never asks?)\s+(?:for|to ask|call for)\b.*?\b(?:otp|pin|cvv|password)\b'),
    re.compile(r'(?i)\b(?:share|give)\s+(?:the\s+)?(?:otp|pin|delivery pin)\b.*?\b(?:only\s+(?:upon|after|at|when)|physically received|at\s+(?:the\s+)?time\s+of\s+(?:delivery|accepting)|delivery agent|handed over)\b'),
    re.compile(r'(?i)\b(?:delivery|package|order|courier)\b.*?\b(?:share\s+(?:otp|pin|delivery pin)\s+only|valid\s+upon\s+receipt|out for delivery)\b'),
    re.compile(r'(?i)(?:kabhi bhi apna otp|otp kisi se sajha na kare|kisi ko na bataye|kisi ke sath share na kare|kisi se share na kare|evaritho share cheyavoddu|evariki cheppavaddu)'),
    re.compile(r'(?i)(?:ఎవరితోనూ పంచుకోవద్దు|ఎవరికీ చెప్పవద్దు|ఓటీపీ పంచుకోవద్దు|ఎవరితోనూ పంచుకోకండి|ఓటీపీ ఎవరికీ చెప్పకండి)'),
    re.compile(r'(?i)(?:किसी\s*(?:से|के\s+साथ)\s*(?:साझा|शेयर)\s*(?:न|मत)\s*करें|साझा\s+(?:न|मत)\s+करें|शेयर\s+(?:न|मत)\s+करें|किसी को न बताएं|बैंक\s+कभी.*?नहीं\s+मांगता|बैंक कभी ओटीपी नहीं मांगता|बैंक कभी पिन नहीं मांगता)'),
    re.compile(r'(?i)(?:(?:if not done by you|if not authorized|report fraud to|sms block to).*?(?:call 1800|toll free|visit branch|never share)|(?:call 1800|toll free|visit branch).*?(?:if not done by you|if not you|if not authorized|report fraud))'),
    re.compile(r'(?i)(?:रिचार्ज\s+सफल|recharge\s+(?:successful|of)|असीमित\s+कॉल|प्रतिदिन\s+और\s+असीमित|\b(?:gb|mb)\s+प्रतिदिन)'),
    re.compile(r'(?i)(?:account\s+me\s+aa\s+gaya|mil\s+gaya|paise\s+aa\s+gaye|resolve\s+ho\s+gaya|refund\s+aa\s+gaya|credit\s+aipoindi|khate\s+me\s+aa\s+gaya|wapas\s+mil\s+gaya)')
]

# Negation prefixes within 6 words of credential action
NEGATION_PREFIX_REGEX = re.compile(
    r'(?i)\b(?:never|do not|don\'t|must not|should not|cannot|not to|kabhi nahi|kabhi na|kisi ko na|kisi se na|na kare|cheyavoddu|cheyakandi|eppudu cheyavoddu|evariki cheppavaddu|मत|नहीं\s+करें|నద్దు|వద్దు|చెప్పవద్దు|పంచుకోవద్దు)\b'
)

# 1. Credential / OTP / PIN Theft Patterns (Active requests, both SVO and SOV Indic order)
OTP_REQUEST_PATTERNS = [
    re.compile(r'(?i)\b(?:share|send|submit|tell|provide|verify|enter|forward|input)\b\s+(?:the\s+|your\s+|this\s+|received\s+)?(?:[a-zA-Z0-9-]+\s+){0,3}\b(?:otp|upi pin|atm pin|pin|cvv|password|passcode|secret code)\b'),
    re.compile(r'(?i)\b(?:enter|put|submit|type|enter cheyandi|dale|dalo|bataye|cheppandi)\b.*?\b(?:otp|upi pin|atm pin|pin|cvv|password)\b.*?\b(?:to (?:authenticate|cancel|stop|freeze|claim|verify|reactivate)|par|lo)\b'),
    re.compile(r'(?i)\b(?:otp|upi pin|pin|cvv|password)\b.*?\b(?:batao|bataye|bheje|share kare|cheppandi|share cheyandi|enter cheyandi|dale|dalo|darj kare|kottu|enter karo)\b'),
    re.compile(r'(?i)\b(?:share\s+otp\s+received|send\s+otp\s+to|otp\s+manager|provide\s+(?:the\s+)?.*?otp)\b'),
    re.compile(r'(?i)(?:ఓటీపీ నమోదు చేయండి|పిన్ నమోదు చేయండి|ఓటీపీ చెప్పండి|పిన నమోదు|ఓటీపీ ఎంటర్|పిన ఎంటర్|పిన కొట్టండి|पिन दर्ज करें|पिन डालें|पिन डालो|ओटीपी बताएं|ओटीपी साझा करें|ओटीपी दर्ज करें)')
]

# 2. Collect Request Trick (Receiving money NEVER requires PIN)
COLLECT_PIN_PATTERNS = [
    re.compile(r'(?i)\b(?:enter|put|type|kottandi|dale|dalo|darj kare)\b.*?\b(?:pin|upi pin)\b.*?\b(?:to (?:receive|claim|collect|get|credit)|paise lene|dabbulu pondadaniki|paise paane)\b'),
    re.compile(r'(?i)\b(?:accept|approve)\b.*?\b(?:collect request|payment request|request|mandate)\b.*?\b(?:to (?:claim|receive|get|credit)|cashback|reward|refund|balance|instantly|pin|upi pin)\b'),
    re.compile(r'(?i)\b(?:receive|get|claim)\b.*?\b(?:cashback|refund|money|reward|advance|token|balance)\b.*?\b(?:enter|approve|accept|scan)\b.*?\b(?:upi pin|pin|qr)\b'),
    re.compile(r'(?i)\b(?:scan|qr\s*code)\b.*?\b(?:receive|get|claim|collect|credit)\b.*?\b(?:balance|money|funds|refund|cashback|bank|account|payment|advance|rs)\b'),
    re.compile(r'(?i)\b(?:olx|quikr|soldier|army)\b.*?\b(?:scan|qr|code)\b.*?\b(?:receive|payment|advance)\b'),
    re.compile(r'(?i)(?:కలెక్ట్ రిక్వెస్ట్|డబ్బులు పొందడానికి|రివార్డ్ పొందడానికి|క్రెడిట్ అవ్వాలంటే|అకౌంట్ లో పడతాయి).*?(?:పిన్|pin|upi pin|ఆమోద|అప్రూవ్)'),
    re.compile(r'(?i)(?:qr\s*(?:code|కోడ్|కోడ్|कोड)|స్కాన్|स्कैन).*?(?:పిన్|pin|upi pin).*?(?:డబ్బులు|పడతాయి|पैसे|credit|receive|account)'),
    re.compile(r'(?i)(?:पैसे|रिफंड|कैशबैक|इनाम)\s*(?:पाने|प्राप्त करने|लेने)\s*के\s*लिए.*?(?:पिन दर्ज करें|पिन डालें|पिन डालो|pin|upi pin|कलेक्ट|स्वीकार)')
]

# 3. Urgency & Account-Block Threat Patterns
URGENCY_BLOCK_PATTERNS = [
    re.compile(r'(?i)\b(?:will be|is|will|account)\s*(?:blocked|suspended|deactivated|closed|frozen|hold|disconnected?|cut off)\b.*?\b(?:tonight|today|immediately|within \d+ hours|in \d+ hours|turant|ventane|now)\b'),
    re.compile(r'(?i)\b(?:electricity|power|power line|current|power supply)\b.*?\b(?:disconnect(?:ed)?|cut|band|katt)\b.*?\b(?:tonight|today|9:30|immediate|turant|ratridi|now)\b'),
    re.compile(r'(?i)\b(?:turant|ventane|urgent|immediately|now)\b.*?\b(?:update|verify|call|contact|unblock|clear bill|disconnect)\b'),
    re.compile(r'(?i)(?:आज रात|24 घंटे|10 बजे|(?:आज रात|रात|today|tonight).*?9:30|9:30\s*(?:pm|बजे|గంటలకు)|निलिपिవేయబడుతుంది|బ్లాక్ చేయబడుతుంది|ఈ రాత్రి|రద్దు|వెంటనే|నిలిపివేయబడింది|తక్షణమే|काट दी जाएगी)')
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

# 6. Disconnection / Block threat with personal phone contact or link (English & Indic syntax)
PHONE_CONTACT_PATTERN = re.compile(
    r'(?i)(?:(?:call|contact|संपर्क|कॉल|సంప్రదించండి|ఫోన్|supervisor|officer|अधिकारी|అధికారి).*?(?:\+91[-\s]?)?(?<!1800)(?<!1860)(?<!1930)[6-9]\d{9}|(?:\+91[-\s]?)?(?<!1800)(?<!1860)(?<!1930)[6-9]\d{9}.*?(?:par call|ku call|ki call|call chey|call kare|par sampark|me sampark|कॉल|సంప్రదించండి))'
)

# 7. Advance-fee lottery patterns
LOTTERY_FEE_PATTERNS = [
    re.compile(r'(?i)\b(?:won|winner|lottery|lucky draw|prize|kbc|giveaway|crorepati|amitabh)\b.*?\b(?:lakh|crore|car|iphone|ticket)\b'),
    re.compile(r'(?i)\b(?:registration fee|processing fee|tax|shipping fee|refundable|file charge|फ़ाइल चार्ज)\b.*?\b(?:pay|deposit|upi|transfer|करें|करे)\b'),
    re.compile(r'(?i)(?:(?:केबीसी|लकी ड्रॉ|लॉटरी|इनाम|బహుమతి|లక్కీ డ్రా|లాటరీ|crorepati).*?(?:लाख|करोड़|lakh|crore|\d+\s*(?:लाख|crore|లక్షలు)|ticket|whatsapp)|(?:लाख|करोड़|lakh|crore|\d+\s*(?:लाख|crore|లక్షలు)).*?(?:केबीसी|लकी ड्रॉ|लॉटरी|इनाम|బహుమతి|లక్కీ డ్రా|లాటరీ|crorepati))'),
    re.compile(r'(?i)(?:lottery|lucky draw|लॉटरी|लकी ड्रॉ|లాటరీ|లక్కీ డ్రా).*?(?:call|कॉल|సంప్రదించండి|संपर्क|contact|manager|మేనేజర్)')
]

# 8. Digital Arrest / Customs / Police threat
DIGITAL_ARREST_PATTERNS = [
    re.compile(r'(?i)\b(?:narcotics|customs|cbi|police|dcp|crime branch|digital arrest|contraband|mdma|drugs|enforcement directorate|money laundering|income tax)\b.*?\b(?:parcel|consignment|arrest warrant|video call|fir registered|skype|clearance fee)\b'),
    re.compile(r'(?i)(?:डिजिटल अरेस्ट|नारकोटिक्स|कस्टम्स|वारंट|డ్రగ్స్|కస్టమ్స్|ఎఫ్‌ఐఆర్|అరెస్ట్|money laundering)')
]

# 9. Loan Extortion / Contact Book Harassment
LOAN_EXTORTION_PATTERNS = [
    re.compile(r'(?i)\b(?:contacts|relatives|family|gallery|photo|photos|contact list)\b.*?\b(?:social media|share|send|defame|leak|post|morphed|viral)\b'),
    re.compile(r'(?i)\b(?:recovery team|recovery boys|police complaint|defame|harass|ghar par|varna|lekapothe|pre-litigation|recovery magistrate)\b.*?\b(?:loan|repay|bhugtan|recovery|upi|attachment of salary)\b'),
    re.compile(r'(?i)(?:मॉर्फ की गई|तस्वीरें|रिश्तेदारों|badnaam|contacts andariki|photo contacts|recovery team|recovery boys|viral karenge|contact list)')
]

# 10. Part-Time / Task / Crypto Investment Scam Patterns
JOB_INVESTMENT_PATTERNS = [
    re.compile(r'(?i)\b(?:part[- ]?time|work from home|daily salary|daily earning|per day|prati roju)\b.*?\b(?:telegram|whatsapp|hotel rating|google rating|youtube (?:like|task)|video like|task job|salary|t\.me/)\b'),
    re.compile(r'(?i)\b(?:task|tasks)\b.*?\b(?:vip task|recharge|trading wallet|withdraw|deposit|earned|withdrawal)\b'),
    re.compile(r'(?i)\b(?:crypto|guaranteed return|मुनाफा|गुना|कमाएं|సంపాదించే|పెట్టుబడి|రేటింగ్స్|intraday|stock market tips|sure[- ]shot)\b.*?\b(?:telegram|whatsapp|return|profit|100%|group|vip group)\b'),
    re.compile(r'(?i)(?:पार्ट टाइम|वर्क फ्रॉम होम|घर बैठे|रोजाना|प्रतिदिन|రేటింగ్స్|టాస్క్|పార్ట్-టైమ్|వర్క్ ఫ్రమ్ హోమ్|సువర్ణావకాశం|రివ్యూలు).*?(?:कॉल|व्हाट्सएप|टेलीग्राम|whatsapp|telegram|సంపాదించండి|t\.me)')
]

# 11. Accidental Transfer Scams
ACCIDENTAL_TRANSFER_PATTERNS = [
    re.compile(r'(?i)\b(?:mistake|accidentally|by mistake|galti se|porapatuna)\b.*?\b(?:transferred|sent|credited|refund|return|bhej\w*|pamp\w*|wapas)\b'),
    re.compile(r'(?i)\b(?:refund|return|send back|wapas|return kijiye|wapas kijiye|wapas kar)\b.*?\b(?:different upi|another number|other vpa|alag number|warna|varna|police|fir|qr|qr code)\b'),
    re.compile(r'(?i)\b(?:credited to your account).*?\b(?:refund|return|different upi)\b')
]

# 12. Fake Customer Support Impersonation
FAKE_SUPPORT_PATTERNS = [
    re.compile(r'(?i)(?:customer care|helpline|support|helpdesk|సహాయ కేంద్రం|కస్టమర్ కేర్|कस्टमर केयर|हेल्पलाइन|complaint cell).*?(?:officer|executive|manager|specialist|call|कॉल|సంప్రదించండి|అధికారి|dial).*?(?:\+91[-\s]?)?[6-9]\d{9}')
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

        # Contextual check for legitimate delivery OTP, telecom recharge, or official bank debit
        is_delivery_otp = bool(re.search(
            r'(?i)\b(?:delivery\s+(?:associate|agent|boy|executive|person)|out\s+for\s+delivery|upon\s+(?:delivery|physical)|at\s+(?:the\s+)?time\s+of\s+(?:delivery|accepting)|handed\s+over|handover|accepting\s+(?:the\s+)?parcel|receiving\s+(?:the\s+)?package|delivery\s+PIN)\b',
            text
        ))
        is_telecom_recharge = bool(re.search(
            r'(?i)(?:रिचार्ज\s+सफल|recharge\s+(?:successful|of)|असीमित\s+कॉल|प्रतिदिन\s+और\s+असीमित|\b(?:gb|mb)\s+प्रतिदिन)',
            text
        ))
        is_bank_debit_alert = bool(re.search(
            r'(?i)\b(?:withdrawn\s+from\s+atm|debited\s+from\s+a/c|credited\s+to\s+a/c|available\s+bal(?:ance)?|avail\s+bal)\b',
            text
        ))

        # 1. OTP / PIN theft check (with strict negation and delivery filtering)
        for p in OTP_REQUEST_PATTERNS:
            m = p.search(text)
            if m:
                if not self.check_negation(text, m.span()) and not is_delivery_otp:
                    has_otp_request = True
                    matched_rules.append({
                        "signal": "Credential Theft Attempt: Explicit instruction to share or input OTP / UPI PIN / CVV / Password.",
                        "source_module": "RULE_SAFETY_LAYER",
                        "weight": 50.0,
                        "severity": "CRITICAL"
                    })
                    break

        # Advisory check: ONLY genuine if NO active OTP theft request is present
        advisory_matches = [p for p in GENUINE_ADVISORY_PATTERNS if p.search(text)]
        if (advisory_matches or is_delivery_otp or is_telecom_recharge or is_bank_debit_alert) and not has_otp_request:
            is_genuine_alert = True
            matched_rules.append({
                "signal": "Legitimate Safety Advisory: Message explicitly warns NEVER to share OTP/PIN, or is verified delivery/bank/telecom notice.",
                "source_module": "RULE_SAFETY_LAYER",
                "weight": -40.0,
                "severity": "INFO"
            })

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

        # 10. Job & Task Investment Scams
        has_job_scam = False
        if not is_telecom_recharge:
            for p in JOB_INVESTMENT_PATTERNS:
                if p.search(text):
                    has_job_scam = True
                    matched_rules.append({
                        "signal": "Part-Time Task & Investment Fraud: Promises unreal daily returns, rating tasks, or Telegram VIP group deposits.",
                        "source_module": "RULE_SAFETY_LAYER",
                        "weight": 40.0,
                        "severity": "HIGH"
                    })
                    break

        # 11. Accidental Transfer Scams
        has_accidental_transfer = False
        for p in ACCIDENTAL_TRANSFER_PATTERNS:
            if p.search(text):
                has_accidental_transfer = True
                matched_rules.append({
                    "signal": "Accidental Transfer Reversal Scam: Claims money was sent by mistake and requests return to a different UPI ID.",
                    "source_module": "RULE_SAFETY_LAYER",
                    "weight": 40.0,
                    "severity": "HIGH"
                })
                break

        # 12. Fake Customer Support
        has_fake_support = False
        for p in FAKE_SUPPORT_PATTERNS:
            if p.search(text):
                has_fake_support = True
                matched_rules.append({
                    "signal": "Fake Customer Support Helpline: Unauthorized mobile contact posing as official help desk executive.",
                    "source_module": "RULE_SAFETY_LAYER",
                    "weight": 35.0,
                    "severity": "HIGH"
                })
                break

        # Hard Override evaluation
        hard_override_high_risk = False
        override_reason = None

        is_utility_threat = has_urgency and (has_phone_threat or has_link) and any(
            kw in text.lower() for kw in ["बिजली", "electricity", "power", "విద్యుత్", "bill", "disconnect", "कट", "బిల్లు"]
        )

        if has_otp_request:
            hard_override_high_risk = True
            override_reason = "Hard Override Triggered: Coercive instruction requesting credential (OTP/PIN/password)."
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
        elif has_lottery and (has_phone_threat or has_link or any(w in text.lower() for w in ["call", "manager", "संपर्क", "कॉल"])):
            hard_override_high_risk = True
            override_reason = "Hard Override Triggered: Advance-fee lottery prize claim with contact prompt."

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
