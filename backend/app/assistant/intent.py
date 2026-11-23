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
    INTENT_HELP,
    INTENT_HOW_TO,
    INTENT_EMERGENCY,
    INTENT_GREETING,
    INTENT_SMALL_TALK,
    INTENT_OUT_OF_SCOPE,
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
            r'\b(yono account|power will be disconnected|electricity power|electricity bill|kbc lucky draw|lottery winner|mdma|customs narcotics|digital arrest warrant|challan of rs|reward points worth|disconnection tonight|25,00,000|speed post delivery|accept collect request|claim cashback|claim on whatsapp|review hotels earn)\b|'
            r'(?:बिजली\s*बिल|योनो|लॉटरी|केबीसी|पार्ट\s*टाइम|अवैध\s*पार्सल|कस्टम|डिजिटल\s*अरेस्ट:|कैशबैक\s*पाने|कलेक्ट\s*रिक्वेस्ट\s*(?:स्वीकार|अप्रूव|आई)|पेमेंट\s*रिक्वेस्ट|बिना\s*सिबिल|सिम\s*कार्ड.*बंद|डाउनलोड\s*करें|पैन\s*अपडेट)|'
            r'(?:విద్యుత్\s*కనెక్షన్|ఖాతా\s*బ్లాక్|లాటరీలో|పార్ట్\s*టైమ్|డ్రగ్స్\s*దొరికాయి|క్యాష్‌బ్యాక్|కలెక్ట్\s*రిక్వెస్ట్.*(?:యాక్సెప్ట్|పిన్)|లోన్\s*యాప్|రిక్వెస్ట్\s*అప్రూవ్|క్షణాల్లో\s*డబ్బు)',
            re.IGNORECASE
        )

        # 2. Small Talk / Greetings / Thanks (checked before how-to so "what is your name" is greeting)
        self.smalltalk_patterns = [
            re.compile(r'^(hi|hello|hey|namaste|namaskar|namaskaram|good morning|good afternoon|good evening|hello there)[!.]*$', re.IGNORECASE),
            re.compile(r'\b(thanks|thank you|thank u|dhanyawad|dhanyavadalu|shukriya|thanks a lot)\b', re.IGNORECASE),
            re.compile(r'\b(who are you|what is your name|who built you|what is upi rakshak|what can you do|what are your capabilities|what are you capable of)\b', re.IGNORECASE),
            re.compile(r'\b(meeru evaru|aap kaun hain|aap kya karte ho|aapka naam kya hai)\b', re.IGNORECASE),
            re.compile(r'^(bye|goodbye|see you|ok bye|untanu)[!.]*$', re.IGNORECASE),
            re.compile(r'(?:नमस्ते|सुप्रभात|हेलो भाई|अलविदा|ధన్యవాదాలు|నమస్కారం|హలో బాగున్నారా|శుభోదయం|సెలవు|ధన్యవాద్|धन्यवाद|आप कौन हैं)', re.IGNORECASE),
        ]

        # 2b. Out-of-Scope Queries (General trivia, recipes, weather, code requests, sports)
        self.out_of_scope_patterns = [
            re.compile(r'\b(recipe|biryani|cook|baking|cake|weather|forecast|temperature|cricket score|cricket match|world cup|capital of|joke|chutkula|essay|poem|write (a )?python|write (a )?code|javascript|linked list|factorial|quicksort|binary search|solve.*equation|movie|cinema ticket|marathon|tomato plant|quantum mechanics|translate this)\b', re.IGNORECASE),
            re.compile(r'\b(kaise banate|mausam kaisa|kisne banwaya|ela cheyali biryani|joke cheppandi|cinema director|vanta ela|ela chesukovali|ela tayaru)\b', re.IGNORECASE),
            re.compile(r'(?:कोड दें|स्कोर क्या है|कविता|राजधानी|తయారీ విధానం|ప్రధానమంత్రి ఎవరు|కవిత చెప్పండి)', re.IGNORECASE),
        ]

        # 3. Emergency Patterns (Immediate financial loss, ongoing theft)
        self.emergency_patterns = [
            re.compile(r'\b(lost|debited|stolen|deducted|withdrew|scammed)\b.*\b(\d+|rupees|rs|inr|money|balance|cash|funds)\b', re.IGNORECASE),
            re.compile(r'\b(\d+|rupees|rs|inr|money|balance|funds)\b.*\b(lost|debited|stolen|deducted|cut|chale gaye|poyayi|gayab|withdraw|scammed|compromised)\b', re.IGNORECASE),
            re.compile(r'\b(paisa|paise|rupaye|dabbu|dabbulu|money)\b.*\b(cut|kat|chale|poyindi|poyayi|deduct|stolen)\b', re.IGNORECASE),
            re.compile(r'\b(unauthorized|fraudulent)\b.*\b(debit|transaction|transfer|withdrawal)\b', re.IGNORECASE),
            re.compile(r'\b(i shared otp|maine otp diya|otp cheppanu|pin shared|shared pin|entered pin)\b', re.IGNORECASE),
            re.compile(r'\b(anydesk|teamviewer|rustdesk|remote access)\b.*\b(debited|cut|money|deducted|fraud|nikal|dabbulu|wiped|loss|download)\b', re.IGNORECASE),
            re.compile(r'\b(transferred|sent|paid)\b.*\b(money|rs|rupees|funds|fee|registration)\b.*\b(fake|scammer|digital arrest|police|lottery)\b', re.IGNORECASE),
            re.compile(r'(?:पैसे|रुपये|रुपए|रुपयों|खाते|खाता|बैलेंस|धनराशी).*(?:कट\s*गए|कट\s*गया|निकल\s*गए|चले\s*गए|गायब|नुकसान|उड़\s*गए|खाली|डिटेक्ट|कटौती)', re.IGNORECASE),
            re.compile(r'(?:ओटीपी\s*(?:बता|दे|शेयर)|पिन\s*(?:डाल|बता|दर्ज)|एनीडेस्क\s*डाउनलोड).*(?:पैसे|कट|निकाल|खाली|गए)', re.IGNORECASE),
            re.compile(r'(?:अनधिकृत|धोखाधड़ी|फ्रॉड).*(?:लेन-देन|कटौती|ट्रांजैक्शन|पैसे|हुई है)', re.IGNORECASE),
            re.compile(r'(?:नकली\s*पुलिस|डिजिटल\s*अरेस्ट|लॉटरी).*(?:पैसे\s*(?:ट्रांसफर|भेज|दे|कट|दिए))|(?:पैसे\s*(?:ट्रांसफर|भेज|दे|कट|दिए)).*(?:नकली\s*पुलिस|डिजिटल\s*अरेस्ट|लॉटरी|तुरंत\s*रोकें)', re.IGNORECASE),
            re.compile(r'(?:कार्ड\s*से|अकाउंट\s*से|ऑटोपे).*(?:पैसे\s*कट|लगातार\s*कट|ब्लॉक\s*करवाएं|बिना\s*इजाजत)', re.IGNORECASE),
            re.compile(r'(?:డబ్బులు|రూపాయలు|ఖాతా|బ్యాలెన్స్).*(?:కట్\s*అయ్యాయి|పోయాయి|డ్రా\s*అయ్యాయి|ఖాళీ|డెబిట్|మోసపోయాను|చెల్లించాను)', re.IGNORECASE),
            re.compile(r'(?:ఓటీపీ\s*చెప్పాను|పిన్\s*ఎంటర్|పిన్\s*నమోదు|యాప్\s*డౌన్‌లోడ్).*(?:డబ్బులు|కట్|పోయాయి|ఖాళీ)', re.IGNORECASE),
            re.compile(r'(?:అనధికారిక|మోసపూరిత).*(?:లావాదేవీ|డెబిట్|డ్రా|జరిగింది)', re.IGNORECASE),
            re.compile(r'(?:నకిలీ\s*పోలీసులకు|మోసగాడికి|లాటరీ\s*కోసం).*(?:డబ్బులు\s*పంపాను|చెల్లించాను|ఫ్రీజ్|మోసపోయాను)', re.IGNORECASE),
            re.compile(r'(?:కార్డు\s*నుండి|ఆటోపే\s*ద్వారా).*(?:డబ్బులు\s*కట్|లావాదేవీలు|జరుగుతున్నాయి)', re.IGNORECASE),
        ]

        # 4. How-To Inquiries & Procedural Questions
        self.howto_patterns = [
            re.compile(r'\b(how to (complain|compliant|report|file)|process of 1930|procedure for 1930|how to 1930)\b', re.IGNORECASE),
            re.compile(r'\b(1930 (pe|lo|par|ki|number|के लिए|కాల్|కోసం))\b', re.IGNORECASE),
            re.compile(r'\b(cybercrime\.gov\.in (pe|lo|par|filing|complaint|report|లో))\b', re.IGNORECASE),
            re.compile(r'\b(what is (digital arrest|golden hour|rbi zero liability|rbi limited liability|collect request|trai dlt|the difference))\b', re.IGNORECASE),
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
            re.compile(r'(?:दस्तावेज जरूरी|जीरो लायबिलिटी|नियम क्या हैं|क्या यह असली है|सत्यापित कैसे करें|చక్షు పోర్టల్|ఎలా తెలుసుకోవాలి|నంబర్ ఎంత|డిజిసాథీ|పరిమిత బాధ్యత|ఎన్ని సిమ్|दस्तावेज|आधार पर कितने)', re.IGNORECASE),
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
                    intent=INTENT_GREETING,
                    confidence=0.98,
                    rule_matched="smalltalk_pattern"
                )

        # 2b. Out-of-Scope Detection (recipes, weather, general trivia)
        for pat in self.out_of_scope_patterns:
            if pat.search(cleaned):
                # Ensure it's not actually a security question
                if not re.search(r'\b(upi|bank|otp|pin|cvv|scam|1930|cyber|fraud|police|loss|lost|money|debit|credit|apk|arrest|freeze)\b|(?:सिम|आधार|साइबर|मोसम|మోసం|బ్యాంక్|సిమ్|ఆధార్)', cleaned, re.IGNORECASE):
                    return IntentResult(
                        intent=INTENT_OUT_OF_SCOPE,
                        confidence=0.96,
                        rule_matched="out_of_scope_pattern"
                    )

        # 3. Emergency Detection
        is_pasted_forward = bool(self.forwarded_pattern.search(cleaned))
        is_url = bool(self.url_pattern.search(cleaned))
        is_vpa = bool(self.vpa_pattern.search(cleaned))
        is_q = bool(re.search(r'\b(how|what|why|is this|check|kaise|kya|kyun|ela|enti|evaru)\b|[?]|(?:क्या|कैसे|क्यों|ఎలా|ఏమిటి|ఎవరు|ఎన్ని|నియమాలు|నియమం)', cleaned, re.IGNORECASE))

        if not is_pasted_forward:
            for pat in self.emergency_patterns:
                if pat.search(cleaned):
                    if not re.search(r'\b(how to|what to do if|process|rules|kya kare agar|tarika)\b', cleaned, re.IGNORECASE):
                        return IntentResult(
                            intent=INTENT_EMERGENCY,
                            confidence=0.96,
                            rule_matched="emergency_pattern"
                        )

        # 4. If query is phrased as a question, prioritize HOW_TO
        if is_q:
            for pat in self.howto_patterns:
                if pat.search(cleaned):
                    return IntentResult(
                        intent=INTENT_HOW_TO,
                        confidence=0.95,
                        rule_matched="howto_pattern"
                    )

        # 5. Threat Artifacts (URLs, VPAs, SMS Headers, Forwarded Threat, Urgency Lures)
        is_sms = bool(self.sms_header_pattern.search(cleaned))
        is_lure = bool(self.urgency_lure_pattern.search(cleaned))

        if (is_url or is_vpa or is_sms or is_pasted_forward or is_lure):
            if not is_q:
                return IntentResult(
                    intent=INTENT_ANALYZE,
                    confidence=0.95,
                    rule_matched="threat_artifact_pattern"
                )

        # 5b. General HOW_TO fallback before ML
        for pat in self.howto_patterns:
            if pat.search(cleaned):
                return IntentResult(
                    intent=INTENT_HOW_TO,
                    confidence=0.95,
                    rule_matched="howto_pattern"
                )

        # 6. ML Model Classification Fallback
        probs = self.pipeline.predict_proba([cleaned])[0]
        max_idx = probs.argmax()
        pred_class = self.pipeline.classes_[max_idx]
        max_prob = float(probs[max_idx])

        # Confidence Threshold: If below 0.25 or single ambiguous word
        if max_prob < 0.25 or (len(cleaned.split()) <= 1 and cleaned.lower() not in ["hi", "hello", "namaste", "namaskaram"]):
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
