import re
from typing import Dict, Any, List, Optional, Tuple

# 1. Debit / Credit / Transaction alert indicators
DEBIT_CREDIT_PATTERNS = [
    re.compile(r'(?i)\b(?:debited|credited|withdrawn|charged|deducted|spent|paid|transferred)\b'),
    re.compile(r'(?i)\b(?:transaction\s+of|purchase\s+of|payment\s+of|txn\s+of)\b'),
    re.compile(r'(?i)\b(?:a/c|account)\s*(?:has\s+been|is)?\s*(?:debited|credited)\b'),
    re.compile(r'(?i)(?:₹|rs\.?|inr)?\s*[\d,]+(?:\.\d{2})?\s*(?:debited|deducted|withdrawn|spent|paid|kat\s*gaye|cut\s*gaye|डेबिट|కట్|డెబిట్)'),
    re.compile(r'(?i)(?:debited|deducted|withdrawn|डेबिट|డెబిట్)\s*(?:by|of|for)?\s*(?:₹|rs\.?|inr)?\s*[\d,]+'),
    # Indic Hindi - flexible with intermediate amount or words
    re.compile(r'(?i)(?:खाते|अकाउंट|खाता)\s*(?:से)?.*?(?:डेबिट|कटे|निकाले|कटा)'),
    re.compile(r'(?i)(?:पैसे|रुपये|राशि|₹|rs\.?|inr).*?(?:कट\s*गए|निकल\s*गए|डेबिट\s*हुए|डेबिट\s*हो\s*गए|काटे\s*गए)'),
    re.compile(r'(?i)ट्रांजेक्शन\s*हुआ'),
    # Indic Telugu
    re.compile(r'(?i)(?:ఖాతా|ఎకౌంట్).*?(?:నుండి)?.*?(?:డెబిట్|కట్|విత్‌డ్రా|తీసివేయబడింది)'),
    re.compile(r'(?i)(?:డబ్బులు|రూపాయలు|మొత్తం|₹|rs\.?).*?(?:కట్\s*అయ్యాయి|డెబిట్\s*అయింది|విత్‌డ్రా\s*అయింది|తీసివేయబడ్డాయి)'),
    re.compile(r'(?i)లావాదేవీ\s*జరిగింది'),
    # Hinglish
    re.compile(r'(?i)(?:debit\s*ho\s*gaya|paise\s*(?:cut|kat)\s*gaye|khate\s*se\s*(?:kat|nikal)\s*gaye|kat\s*chuke\s*hai)')
]

# 2. Callback instructions / Dispute reverse actions
CALLBACK_INSTRUCTION_PATTERNS = [
    re.compile(r'(?i)\b(?:if\s+not\s+(?:done\s+)?(?:by\s+)?you|if\s+not\s+you|not\s+you\??|if\s+not\s+authorized|if\s+not\s+recogni[sz]ed)\b.*?\b(?:call|contact|dial|reach|msg|whatsapp|sms)\b'),
    re.compile(r'(?i)\b(?:to\s+(?:cancel|reverse|dispute|stop|block|freeze|claim\s+refund))\b.*?\b(?:call|contact|dial|reach|msg|whatsapp)\b'),
    re.compile(r'(?i)\b(?:call|contact|dial|reach|whatsapp|msg)\b.*?\b(?:immediately|urgently|now|turant|ventane)\b'),
    re.compile(r'(?i)\b(?:customer\s+care|fraud\s+team|support\s+desk|bank\s+helpline)\b.*?\b(?:call|dial|contact|at|on|reach)\b'),
    re.compile(r'(?i)\b(?:call|contact|dial)\s+(?:on\s+)?(?:\+91|0|[6-9]|x{3,}|toll|this\s+number)'),
    re.compile(r'(?i)\b(?:dispute\s+transaction|dispute\s+this|unauthorized\s+transaction)\b.*?\b(?:call|contact|dial)\b'),
    re.compile(r'(?i)\b(?:i\s+am\s+from|from)\s+(?:bank\s+fraud|fraud\s+team|security\s+division)\b.*?\b(?:call|contact|reach|dial)\b'),
    re.compile(r'(?i)\b(?:msg|message|whatsapp|ping)\s+(?:on|to|at)?\s*(?:this\s+number|\+91|0|[6-9]|x{3,})'),
    # Indic Hindi
    re.compile(r'(?i)(?:यदि\s*आपने|अगर\s*आपने|आपने\s*नहीं|अगर\s*यह).*?(?:नहीं\s*किया|नहीं\s*है).*?(?:कॉल|संपर्क|डायल)'),
    re.compile(r'(?i)(?:रद्द\s*करने|रोकने|रिवर्स|शिकायत\s*हेतु|सत्यापन\s*हेतु).*?(?:कॉल|संपर्क|डायल)'),
    re.compile(r'(?i)(?:तुरंत\s*कॉल\s*करें|कस्टमर\s*केयर\s*से\s*संपर्क|इस\s*नंबर\s*पर\s*(?:कॉल|संपर्क))'),
    # Indic Telugu
    re.compile(r'(?i)(?:మీరు\s*చేయకపోతే|మీరు\s*కాకపోతే|ఈ\s*లావాదేవీ\s*మీరు\s*చేయకపోతే).*?(?:కాల్|సంప్రదించండి|డయల్)'),
    re.compile(r'(?i)(?:రద్దు\s*చేయడానికి|ఆపడానికి|ఫిర్యాదు\s*చేయడానికి).*?(?:కాల్|సంప్రదించండి|డయల్)'),
    re.compile(r'(?i)(?:వెంటనే\s*కాల్\s*చేయండి|ఈ\s*నంబర్‌కు\s*కాల్\s*చేయండి|కస్టమర్\s*కేర్‌ను\s*సంప్రదించండి)'),
    # Hinglish
    re.compile(r'(?i)(?:agar\s+aapne\s+nahi\s+kiya|agar\s+ye\s+aapne\s+nahi|if\s+not\s+you).*?(?:call|sampark|contact|kare|karo)'),
    re.compile(r'(?i)(?:cancel|reverse|rokne|wapas)\s+(?:karne\s+ke\s+liye|ke\s+liye).*?(?:call|sampark|contact|kare|karo)')
]

# 3. Callback Number Types: Personal Mobile, Obfuscated/Placeholder, Words
PERSONAL_MOBILE_REGEX = re.compile(r'(?<!\d)(?:\+91[-\s]?)?[6-9]\d{9}(?!\d)')
PERSONAL_MOBILE_0_REGEX = re.compile(r'(?<!\d)0[6-9]\d{9}(?!\d)')
SPACED_MOBILE_REGEX = re.compile(r'(?<!\d)[6-9](?:\s+\d){9}(?!\d)')

PLACEHOLDER_NUMBER_REGEX = re.compile(r'(?i)(?:\+91[-\s]?)?(?:[xX*]{6,12}|[6-9]\d{1,4}[xX*]{5,9}|[xX*]{3,5}[-\s][xX*]{3,5})')

DIGITS_IN_WORDS_REGEX = re.compile(
    r'(?i)\b(?:zero|one|two|three|four|five|six|seven|eight|nine)(?:\s+(?:zero|one|two|three|four|five|six|seven|eight|nine)){5,}\b'
)
DIGITS_IN_HINDI_REGEX = re.compile(
    r'(?:शून्य|एक|दो|तीन|चार|पांच|छह|सात|आठ|नौ)(?:\s+(?:शून्य|एक|दो|तीन|चार|पांच|छह|सात|आठ|नौ)){5,}'
)
DIGITS_IN_TELUGU_REGEX = re.compile(
    r'(?:సున్నా|ఒకటి|రెండు|మూడు|నాలుగు|ఐదు|ఆరు|ఏడు|ఎనిమిది|తొమ్మిది)(?:\s+(?:సున్నా|ఒకటి|రెండు|మూడు|నాలుగు|ఐదు|ఆరు|ఏడు|ఎనిమిది|తొమ్మిది)){5,}'
)

# Official toll-free prefixes (Genuine banking callbacks)
TOLL_FREE_REGEX = re.compile(r'(?<!\d)(?:1800|1860)[-\s]?\d{3,4}[-\s]?\d{3,4}(?!\d)')
SHORTCODE_REGEX = re.compile(r'(?<!\d)(?:567676|56161|567678|1930|155260)(?!\d)')

# 4. Genuine Bank Alert Markers (Protection for Real Notifications)
GENUINE_ACCOUNT_LAST4 = re.compile(
    r'(?i)\b(?:a/c|acct|acc|account|card)\s*(?:no\.?)?\s*(?:ending\s+(?:with\s+|in\s+)?|\*+|x+|xx)?\s*[*xX\d]{0,4}\d{4}\b'
)
GENUINE_REF_PATTERNS = [
    re.compile(r'(?i)\b(?:ref(?:\s*no)?|txn(?:\s*id)?|rrn|utr|upi\s*ref|imps\s*ref|cms)\s*[:#\-\s]\s*[a-zA-Z0-9]{6,}\b'),
    re.compile(r'(?i)\b(?:vpa|to|at|info)\s+([a-zA-Z0-9.\-_]{2,}@[a-zA-Z0-9.\-_]{2,}|\b(?:swiggy|zomato|amazon|flipkart|uber|ola|netflix|irctc)\b)')
]
GENUINE_BALANCE_LINE = re.compile(
    r'(?i)\b(?:avl\s*bal|available\s*bal(?:ance)?|total\s*bal(?:ance)?|bal(?:\s*inr|\s*rs)?)\s*[:.]?\s*(?:₹|rs\.?|inr)?\s*[\d,]+'
)

# 5. Generic Account phrasing (Indicator of mass-target phishing alert)
GENERIC_ACCOUNT_REGEX = re.compile(
    r'(?i)\b(?:your\s+account|your\s+bank\s+account|apke\s+khate|mee\s+account|aapka\s+khata)\b'
)

# 6. Urgency indicators
URGENCY_REGEX = re.compile(
    r'(?i)(?:\b(?:immediately|urgently|within\s+24\s+hours|within\s+1\s+hour|within\s+\d+\s+min(?:utes)?|turant|ventane|urgent|now|at\s+once)\b|आज\s*ही|तुरंत|వెంటనే|తక్షణమే)'
)

# 7. Large round amounts commonly used in shock scams
LARGE_ROUND_AMOUNT_REGEX = re.compile(
    r'(?i)(?:₹|rs\.?|inr)\s*(?:49,?999|50,?000|25,?000|99,?999|1,?00,?000|75,?000|30,?000|20,?000|40,?000|80,?000|15,?000|10,?000)'
)

class CallbackScamDetector:
    """
    Detects fake debit/credit alert callback phishing scams (Telephone-Oriented Attack Delivery).
    Scammers send shock alerts ('₹49,999 debited') directing victims to dial an unverified mobile number
    or unreadable placeholder to reverse the transaction.
    """

    def analyze(self, text: str) -> Dict[str, Any]:
        if not text:
            return {
                "is_callback_scam": False,
                "score": 0.0,
                "signals": [],
                "details": {}
            }

        # Step 1: Detect Debit/Credit alert wording
        has_debit_credit = any(p.search(text) for p in DEBIT_CREDIT_PATTERNS)

        # Step 2: Detect Callback instruction
        has_callback_instruction = any(p.search(text) for p in CALLBACK_INSTRUCTION_PATTERNS)

        # Step 3: Detect & classify Callback numbers
        personal_mobiles = PERSONAL_MOBILE_REGEX.findall(text)
        personal_0_mobiles = PERSONAL_MOBILE_0_REGEX.findall(text)
        spaced_mobiles = SPACED_MOBILE_REGEX.findall(text)
        placeholders = PLACEHOLDER_NUMBER_REGEX.findall(text)
        words_en = DIGITS_IN_WORDS_REGEX.findall(text)
        words_hi = DIGITS_IN_HINDI_REGEX.findall(text)
        words_te = DIGITS_IN_TELUGU_REGEX.findall(text)

        toll_free_numbers = TOLL_FREE_REGEX.findall(text)
        shortcodes = SHORTCODE_REGEX.findall(text)

        has_personal_mobile = bool(personal_mobiles or personal_0_mobiles or spaced_mobiles)
        has_placeholder = bool(placeholders)
        has_words_number = bool(words_en or words_hi or words_te)
        has_toll_free = bool(toll_free_numbers or shortcodes)

        # Treat personal mobile, placeholder (e.g. XXXXXXXXXX), or spelled out digits as callback target
        has_suspicious_callback_number = (has_personal_mobile or has_placeholder or has_words_number)

        # Step 4: Evaluate genuine banking markers
        has_last4 = bool(GENUINE_ACCOUNT_LAST4.search(text))
        has_ref = any(p.search(text) for p in GENUINE_REF_PATTERNS)
        has_bal = bool(GENUINE_BALANCE_LINE.search(text))
        is_generic_acct = bool(GENERIC_ACCOUNT_REGEX.search(text)) and not has_last4

        # Genuine score factor: if legitimate bank markers are heavily present with toll-free, it's genuine
        genuine_markers_count = sum([has_last4, has_ref, has_bal])
        missing_genuine_markers = (genuine_markers_count == 0) or (is_generic_acct and not has_ref)

        # Step 5: Urgency & shock amount
        has_urgency = bool(URGENCY_REGEX.search(text))
        has_large_round_amt = bool(LARGE_ROUND_AMOUNT_REGEX.search(text))

        # Decision Logic:
        # Scam criteria: Debit/Credit alert + Callback instruction + (Suspicious callback number OR generic instruction without official toll-free) + missing genuine markers
        signals = []
        is_scam = False
        score = 0.0

        if has_debit_credit and has_callback_instruction and (has_suspicious_callback_number or not has_toll_free) and missing_genuine_markers:
            is_scam = True
            score = 55.0  # Base score in SUSPICIOUS territory (35-69)

            # Signal 1: Callback instruction on debit alert
            signals.append({
                "signal": "Callback Phishing Trap: Message alerts of an alleged debit/credit and instructs you to call or message a number to dispute or cancel it.",
                "source_module": "CALLBACK_PHISHING_DETECTOR",
                "weight": 35.0,
                "severity": "HIGH"
            })

            # Signal 2: Callback number nature
            if has_placeholder:
                extracted_ph = placeholders[0]
                score += 15.0
                signals.append({
                    "signal": f"Obfuscated / Placeholder Callback Number: Target phone number '{extracted_ph}' uses masked placeholder digits (e.g., XXXXXXXXXX), a hallmark of templated mass-phishing lures.",
                    "source_module": "CALLBACK_PHISHING_DETECTOR",
                    "weight": 20.0,
                    "severity": "HIGH"
                })
            elif has_personal_mobile:
                extracted_ph = (personal_mobiles or personal_0_mobiles or spaced_mobiles)[0]
                score += 15.0
                signals.append({
                    "signal": f"Personal Mobile Callback: Instructions ask you to dial a personal 10-digit mobile number ('{extracted_ph}') rather than an authorized banking toll-free or official short-code.",
                    "source_module": "CALLBACK_PHISHING_DETECTOR",
                    "weight": 20.0,
                    "severity": "HIGH"
                })
            elif has_words_number:
                score += 15.0
                signals.append({
                    "signal": "Spelled-Out Callback Number: Phone number is obfuscated in written words to evade automated telecom filter scanners.",
                    "source_module": "CALLBACK_PHISHING_DETECTOR",
                    "weight": 20.0,
                    "severity": "HIGH"
                })

            # Signal 3: Missing genuine markers
            signals.append({
                "signal": "Missing Genuine Banking Markers: Notice lacks verified account last-4 digits (XX1234), official transaction reference ID (UTR/RRN), and account balance information.",
                "source_module": "CALLBACK_PHISHING_DETECTOR",
                "weight": 15.0,
                "severity": "MEDIUM"
            })

            # Signal 4: Urgency or large round amount
            if has_urgency:
                score += 15.0
                signals.append({
                    "signal": "Artificial Urgency: Coercive instruction to call 'immediately' or within an urgent deadline to prevent loss.",
                    "source_module": "CALLBACK_PHISHING_DETECTOR",
                    "weight": 15.0,
                    "severity": "HIGH"
                })

            if has_large_round_amt:
                score += 10.0
                signals.append({
                    "signal": "Shock Round Amount: Alert uses a large round figure commonly deployed in psychological fraud bait.",
                    "source_module": "CALLBACK_PHISHING_DETECTOR",
                    "weight": 10.0,
                    "severity": "MEDIUM"
                })

            # Cap max score to 85.0 (High Risk)
            score = min(88.0, score)

        return {
            "is_callback_scam": is_scam,
            "score": score,
            "signals": signals,
            "category": "fake_debit_alert_callback" if is_scam else None,
            "details": {
                "has_debit_credit": has_debit_credit,
                "has_callback_instruction": has_callback_instruction,
                "has_personal_mobile": has_personal_mobile,
                "has_placeholder": has_placeholder,
                "has_words_number": has_words_number,
                "has_toll_free": has_toll_free,
                "missing_genuine_markers": missing_genuine_markers,
                "has_urgency": has_urgency,
                "has_large_round_amt": has_large_round_amt
            }
        }

    detect = analyze

callback_scam_detector = CallbackScamDetector()
