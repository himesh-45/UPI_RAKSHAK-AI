import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from .intent_dataset import (
    TRAIN_INTENT_DATA,
    ALL_INTENTS,
    INTENT_ANALYZE,
    INTENT_HOW_TO,
    INTENT_EMERGENCY,
    INTENT_SMALL_TALK,
    INTENT_UNCLEAR,
)

@dataclass
class IntentResult:
    intent: str
    confidence: float
    rule_matched: Optional[str] = None
    needs_clarification: bool = False
    clarifying_question: Optional[Dict[str, str]] = None
    clarifying_options: Optional[List[Dict[str, str]]] = None


class IntentClassifier:
    """
    Hybrid Intent Classifier for Conversational Safety Assistant.
    Combines fast regex/heuristic rule matching with subword character n-gram
    logistic regression for high accuracy and typo-tolerance across
    English, Hindi, Telugu, and Hinglish.
    """

    def __init__(self):
        self.model = None
        self._build_and_train_model()
        self._compile_rules()

    def _compile_rules(self):
        # 1. URL / Domain Pattern (including shortlinks like t.me, bit.ly, wa.me)
        self.url_pattern = re.compile(
            r'https?://[^\s]+|t\.me/[^\s]+|bit\.ly/[^\s]+|wa\.me/[^\s]+|\b[a-zA-Z0-9.-]+\.(?:top|xyz|cc|online|site|club|app|info|vip|live|work|link|shop|click|tk|ml|ga|cf|gq)\b',
            re.IGNORECASE
        )
        self.vpa_pattern = re.compile(
            r'\b[a-zA-Z0-9.\-_]{2,256}@(okhdfcbank|okaxis|oksbi|okicici|paytm|ybl|ibl|axl|upi|sbi|hdfcbank|icici|barodampay|kotak)\b',
            re.IGNORECASE
        )
        self.sms_header_pattern = re.compile(
            r'\b(?:[A-Z]{2}-[A-Z0-9]{6}|[A-Z]{2}-[A-Z0-9]{3,8}|VK-[A-Z0-9]+|AD-[A-Z0-9]+|VM-[A-Z0-9]+)\b'
        )
        self.forwarded_pattern = re.compile(r'\b(fwd:|forwarded message|forwarded:|sms says|message says|got this message|naaku ee message|ye message aaya)\b', re.IGNORECASE)
        self.urgency_lure_pattern = re.compile(
            r'\b(yono account|power will be disconnected|electricity power|electricity bill|kbc lucky draw|lottery winner|mdma|customs narcotics|digital arrest warrant|challan of rs|reward points worth|disconnection tonight|25,00,000|speed post delivery)\b',
            re.IGNORECASE
        )

        # 2. Small Talk / Greetings / Thanks (checked before how-to so "what is your name" is greeting)
        self.smalltalk_patterns = [
            re.compile(r'^(hi|hello|hey|namaste|namaskar|namaskaram|good morning|good afternoon|good evening|hello there)[!.]*$', re.IGNORECASE),
            re.compile(r'\b(thanks|thank you|thank u|dhanyawad|dhanyavadalu|shukriya|thanks a lot)\b', re.IGNORECASE),
            re.compile(r'\b(who are you|what is your name|who built you|what is upi rakshak|what can you do|what are your capabilities|what are you capable of)\b', re.IGNORECASE),
            re.compile(r'\b(meeru evaru|aap kaun hain|aap kya karte ho|aapka naam kya hai)\b', re.IGNORECASE),
            re.compile(r'^(bye|goodbye|see you|ok bye|untanu)[!.]*$', re.IGNORECASE),
        ]

        # 3. Emergency Patterns (Immediate financial loss, ongoing theft)
        self.emergency_patterns = [
            re.compile(r'\b(lost|debited|stolen|deducted|withdrew|scammed)\b.*\b(\d+|rupees|rs|inr|money|balance|cash)\b', re.IGNORECASE),
            re.compile(r'\b(\d+|rupees|rs|inr)\b.*\b(lost|debited|stolen|deducted|cut|chale gaye|poyayi|gayab|withdraw)\b', re.IGNORECASE),
            re.compile(r'\b(paisa|paise|rupaye|dabbu|dabbulu|money)\b.*\b(cut|kat|chale|poyindi|poyayi|deduct|stolen)\b', re.IGNORECASE),
            re.compile(r'\b(unauthorized|fraudulent)\b.*\b(debit|transaction|transfer|withdrawal)\b', re.IGNORECASE),
            re.compile(r'\b(i shared otp|maine otp diya|otp cheppanu|pin shared|shared pin)\b.*\b(debited|cut|money|loss|khali|poyindi)\b', re.IGNORECASE),
            re.compile(r'\b(anydesk|teamviewer)\b.*\b(debited|cut|money|deducted|fraud|nikal|dabbulu)\b', re.IGNORECASE),
            re.compile(r'\b(account nundi|na bank nundi|mere account se)\b.*\b(cut|debited|nikal|deduct|poyayi)\b', re.IGNORECASE),
        ]

        # 4. How-To Inquiries & Procedural Questions
        self.howto_patterns = [
            re.compile(r'\b(how to (complain|compliant|report|file)|process of 1930|procedure for 1930|how to 1930)\b', re.IGNORECASE),
            re.compile(r'\b(1930 (pe|lo|par|ki|number))\b', re.IGNORECASE),
            re.compile(r'\b(cybercrime\.gov\.in (pe|lo|par|filing|complaint|report))\b', re.IGNORECASE),
            re.compile(r'\b(what is (digital arrest|golden hour|rbi zero liability|collect request|trai dlt))\b', re.IGNORECASE),
            re.compile(r'\b(what should i prepare|what to prepare)\b', re.IGNORECASE),
            re.compile(r'\b(how to (block|bloack|disable|delete) (my )?upi)\b', re.IGNORECASE),
            re.compile(r'\b(how to verify (if )?bank (sms|message))\b', re.IGNORECASE),
            re.compile(r'\b(how do collect requests work|do collect requests debit)\b', re.IGNORECASE),
            re.compile(r'\b(is (entering )?upi pin required|do i need to enter pin)\b', re.IGNORECASE),
            re.compile(r'\b(kya paise lene ke liye|paise lene ke liye pin)\b', re.IGNORECASE),
            re.compile(r'\b(dabbu teesukovadaniki|dabbu pondadaniki upi pin)\b', re.IGNORECASE),
            re.compile(r'\b(digital arrest (kya|ante|real|sach))\b', re.IGNORECASE),
            re.compile(r'\b(can cbi|can police arrest|police arrest over video)\b', re.IGNORECASE),
            re.compile(r'\b(anydesk (app )?(delete|uninstall)|anydesk app delete cheste)\b', re.IGNORECASE),
            re.compile(r'\b(dabbu recovery cheyadam ela|money recovery kaise)\b', re.IGNORECASE),
            re.compile(r'\b(how to (protect|recover|freeze|report|spot|check))\b', re.IGNORECASE),
            re.compile(r'\b(kaise kare|kaise karein|kaise karte hain|kaise hota hai|tarika kya hai)\b', re.IGNORECASE),
            re.compile(r'\b(ela cheyyali|ela cheyali|ela ivvali|ela cheyatam|ela block|ante enti|ento cheppandi|ela gurtinchali)\b', re.IGNORECASE),
        ]

    def _build_and_train_model(self):
        X = [text for text, _ in TRAIN_INTENT_DATA]
        y = [label for _, label in TRAIN_INTENT_DATA]

        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                analyzer='char_wb',
                ngram_range=(2, 5),
                min_df=1,
                sublinear_tf=True
            )),
            ('clf', LogisticRegression(
                C=3.0,
                class_weight='balanced',
                max_iter=1000,
                random_state=42
            ))
        ])
        self.pipeline.fit(X, y)

    def classify(self, text: str, has_image: bool = False, history: Optional[List[Dict[str, str]]] = None) -> IntentResult:
        if has_image:
            return IntentResult(
                intent=INTENT_ANALYZE,
                confidence=1.0,
                rule_matched="has_image"
            )

        cleaned = (text or "").strip()
        if not cleaned:
            return self._build_unclear_result(0.0, "empty_input")

        # 1. Conversational Follow-Up check (context grounding)
        if history and len(history) > 0 and len(cleaned.split()) <= 6:
            follow_up_stems = [
                "how do i do that", "how to do that", "what should i prepare",
                "what next", "where do i click", "how to do step", "tell me more",
                "ela cheyyali", "kahan click kare", "aur batao", "tarvata em cheyali"
            ]
            if any(stem in cleaned.lower() for stem in follow_up_stems):
                return IntentResult(
                    intent=INTENT_HOW_TO,
                    confidence=0.95,
                    rule_matched="conversational_follow_up"
                )

        # 2. Small Talk / Greetings / Thanks (checked before how-to)
        for pat in self.smalltalk_patterns:
            if pat.search(cleaned):
                return IntentResult(
                    intent=INTENT_SMALL_TALK,
                    confidence=0.98,
                    rule_matched="smalltalk_pattern"
                )

        # 3. Emergency vs Pasted SMS Check
        is_pasted_forward = bool(self.forwarded_pattern.search(cleaned))
        is_url = bool(self.url_pattern.search(cleaned))
        is_vpa = bool(self.vpa_pattern.search(cleaned))

        # If user explicitly states they lost money (and not forwarding an SMS like "SMS says: account debited")
        if not is_pasted_forward:
            for pat in self.emergency_patterns:
                if pat.search(cleaned):
                    # Exclude procedural question formulations
                    if not re.search(r'\b(how to|what to do if|process|rules|kya kare agar|ela cheyali|tarika)\b', cleaned, re.IGNORECASE):
                        return IntentResult(
                            intent=INTENT_EMERGENCY,
                            confidence=0.96,
                            rule_matched="emergency_pattern"
                        )

        # 4. Explicit How-To Procedural Inquiries
        for pat in self.howto_patterns:
            if pat.search(cleaned):
                # Ensure it's not a pasted scam message containing a URL
                if not (is_url and len(cleaned) > 130 and not re.search(r'\b(how|what|is this|check|kaise|ela)\b', cleaned, re.IGNORECASE)):
                    return IntentResult(
                        intent=INTENT_HOW_TO,
                        confidence=0.95,
                        rule_matched="howto_pattern"
                    )

        # 5. Threat Artifacts (URLs, VPAs, SMS Headers, Forwarded Threat)
        is_sms = bool(self.sms_header_pattern.search(cleaned))
        is_lure = bool(self.urgency_lure_pattern.search(cleaned))

        if (is_url or is_vpa or is_sms or is_pasted_forward or is_lure) and not re.search(r'\b(how to (complain|report|block)|what is digital arrest)\b', cleaned, re.IGNORECASE):
            return IntentResult(
                intent=INTENT_ANALYZE,
                confidence=0.95,
                rule_matched="threat_artifact_pattern"
            )

        # 6. ML Model Classification Fallback
        probs = self.pipeline.predict_proba([cleaned])[0]
        max_idx = probs.argmax()
        pred_class = self.pipeline.classes_[max_idx]
        max_prob = float(probs[max_idx])

        # Confidence Threshold: If below 0.38 or single ambiguous word
        if max_prob < 0.38 or (len(cleaned.split()) <= 1 and cleaned.lower() not in ["hi", "hello", "namaste", "namaskaram"]):
            return self._build_unclear_result(max_prob, "low_confidence_classifier")

        return IntentResult(
            intent=pred_class,
            confidence=round(max_prob, 3),
            rule_matched="ml_classifier"
        )

    def _build_unclear_result(self, confidence: float, rule_matched: str) -> IntentResult:
        return IntentResult(
            intent=INTENT_UNCLEAR,
            confidence=confidence,
            rule_matched=rule_matched,
            needs_clarification=True,
            clarifying_question={
                "en": "I didn't quite catch that. Would you like me to check a suspicious message for scams, or do you need help with cybercrime reporting and safety guidelines?",
                "hi": "मैं ठीक से समझ नहीं पाया। क्या आप किसी संदिग्ध संदेश या लिंक की जांच करना चाहते हैं, या साइबर अपराध से जुड़ी कोई मदद चाहिए?",
                "te": "నాకు సరిగ్గా అర్థం కాలేదు. మీరు ఏదైనా అనుమానాస్పద సందేశాన్ని తనిఖీ చేయాలనుకుంటున్నారా, లేదా సైబర్ మోసం గురించి సహాయం కావాలా?"
            },
            clarifying_options=[
                {"id": "opt_check_msg", "label": "🔍 Check a Suspicious Message", "action": "prompt_analyze"},
                {"id": "opt_get_help", "label": "💡 Get Help & Reporting Guide", "action": "prompt_help"}
            ]
        )


# Global singleton instance
intent_classifier = IntentClassifier()
