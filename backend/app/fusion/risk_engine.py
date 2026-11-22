import re
from typing import Dict, Any, List, Optional
from ..config import settings
from ..models.schemas import EvidenceItem, RAGCitation, SafetyReport, HighlightSpan, WaterfallStep
from ..rag.retriever import rag_retriever
from ..core.scam_story import scam_story_engine
from ..core.normalizer import text_normalizer
from ..core.community_reputation import lookup_community_reputation
from ..detectors.url_scanner import URL_EXTRACT_REGEX

PHONE_REGEX = re.compile(r'(?<!\d)(?:\+91[-\s]?)?[6-9]\d{9}(?!\d)')
UPI_VPA_REGEX = re.compile(r'\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z0-9.\-_]{2,}\b')
CREDENTIAL_REGEX = re.compile(r'(?i)\b(?:otp|upi pin|pin|cvv|password|passcode|secret code|पिन|ओटीपी|పిన్|ఓటీపీ)\b')
URGENCY_REGEX = re.compile(r'(?i)\b(?:blocked|suspended|disconnected|cut off|immediately|tonight|24 hours|urgent|turant|ventane|आज रात|బ్లాక్|వెంటనే)\b')
COLLECT_REGEX = re.compile(r'(?i)\b(?:collect|approve|scratch card|reward|cashback|refund|कलेक्ट|కలెక్ట్)\b')
REMOTE_REGEX = re.compile(r'(?i)\b(?:anydesk|teamviewer|quicksupport|rustdesk|ultraviewer)\b')

CATEGORY_NAMES_I18N = {
    "fake_bank_kyc": {
        "en": "Fake Bank KYC Phishing",
        "hi": "फर्जी बैंक केवाईसी धोखाधड़ी",
        "te": "నకిలీ బ్యాంక్ కేవైసీ మోసం"
    },
    "electricity_disconnection": {
        "en": "Electricity Disconnection Scam",
        "hi": "बिजली बिल डिस्कनेक्शन धोखा",
        "te": "విద్యుత్ సరఫరా రద్దు బెదిరింపు మోసం"
    },
    "fake_upi_refund_cashback": {
        "en": "Fake UPI Refund & Cashback Scam",
        "hi": "फर्जी यूपीआई रिफंड/कैशबैक धोखा",
        "te": "నకిలీ UPI క్యాష్‌బ్యాక్/రీఫండ్ మోసం"
    },
    "collect_request_fraud": {
        "en": "UPI Collect Request Fraud",
        "hi": "यूपीआई कलेक्ट रिक्वेस्ट धोखा",
        "te": "యూపీఐ కలెక్ట్ రిక్వెస్ట్ మోసం"
    },
    "lottery_prize": {
        "en": "Lottery & Advance-Fee Prize Scam",
        "hi": "केबीसी/लकी ड्रॉ लॉटरी धोखाधड़ी",
        "te": "లక్కీ డ్రా మరియు లాటరీ మోసం"
    },
    "fake_customer_support": {
        "en": "Fake Customer Support Helpline",
        "hi": "फर्जी कस्टमर केयर धोखा",
        "te": "నకిలీ కస్టమర్ కేర్ హెల్ప్‌లైన్ మోసం"
    },
    "remote_access_scam": {
        "en": "Remote Device Takeover Scam",
        "hi": "रिमोट एक्सेस ऐप धोखा (AnyDesk)",
        "te": "రిమోట్ యాక్సెస్ యాప్ మోసం"
    },
    "otp_pin_theft": {
        "en": "Credential & OTP/PIN Theft",
        "hi": "ओटीपी और यूपीआई पिन चोरी",
        "te": "ఓటీపీ మరియు యూపీఐ పిన్ దొంగతనం"
    },
    "fake_govt_scheme": {
        "en": "Fake Government Subsidy Scheme",
        "hi": "फर्जी सरकारी योजना व सब्सिडी धोखा",
        "te": "నకిలీ ప్రభుత్వ పథకం సాయం మోసం"
    },
    "job_investment_scam": {
        "en": "Part-Time Task & Crypto Investment Scam",
        "hi": "पार्ट-टाइम टास्क व निवेश धोखा",
        "te": "పార్ట్-టైమ్ జాబ్ & పెట్టుబడి మోసం"
    },
    "loan_app_extortion": {
        "en": "Predatory Loan App Extortion",
        "hi": "फर्जी लोन ऐप ब्लैकमेल व उत्पीड़न",
        "te": "నకిలీ లోన్ యాప్ వేధింపు మోసం"
    },
    "courier_customs_scam": {
        "en": "Courier Narcotics & Digital Arrest Scam",
        "hi": "कूरियर पार्सल व डिजिटल अरेस्ट धोखा",
        "te": "కొరియర్ డ్రగ్స్ & డిజిటల్ అరెస్ట్ మోసం"
    },
    "marketplace_qr_scam": {
        "en": "OLX / Marketplace QR Scam",
        "hi": "ओएलएक्स क्यूआर कोड धोखा",
        "te": "ఓఎల్ఎక్స్ క్యూఆర్ కోడ్ మోసం"
    },
    "accidental_transfer_scam": {
        "en": "Accidental Transfer Reversal Scam",
        "hi": "गलत खाते में पैसे भेजने का झांसा",
        "te": "పొరపాటున డబ్బు పంపినట్లు మోసం"
    },
    "legitimate": {
        "en": "Legitimate Notification / Genuine Message",
        "hi": "प्रामाणिक बैंक/सेवा संदेश",
        "te": "నిజమైన సర్వీస్/బ్యాంక్ సందేశం"
    }
}

class RiskFusionEngine:
    """
    Evidence-based multi-signal Risk Fusion Engine.
    Combines NLP, deterministic rules, static URL analysis, QR/UPI anomalies, and OCR signals.
    Generates token highlight spans, score waterfall breakdowns, and 1930 reports.
    """

    def extract_highlight_spans(self, text: str) -> List[HighlightSpan]:
        spans = []
        if not text:
            return spans

        # 1. URLs
        for m in URL_EXTRACT_REGEX.finditer(text):
            spans.append(HighlightSpan(
                start=m.start(),
                end=m.end(),
                text=m.group(),
                label="SUSPICIOUS_LINK",
                severity="HIGH"
            ))

        # 2. Phone numbers
        for m in PHONE_REGEX.finditer(text):
            spans.append(HighlightSpan(
                start=m.start(),
                end=m.end(),
                text=m.group(),
                label="PHONE_NUMBER",
                severity="MEDIUM"
            ))

        # 3. UPI VPAs
        for m in UPI_VPA_REGEX.finditer(text):
            spans.append(HighlightSpan(
                start=m.start(),
                end=m.end(),
                text=m.group(),
                label="UPI_VPA",
                severity="MEDIUM"
            ))

        # 4. Credential theft words
        for m in CREDENTIAL_REGEX.finditer(text):
            spans.append(HighlightSpan(
                start=m.start(),
                end=m.end(),
                text=m.group(),
                label="CREDENTIAL_THEFT",
                severity="CRITICAL"
            ))

        # 5. Urgency markers
        for m in URGENCY_REGEX.finditer(text):
            spans.append(HighlightSpan(
                start=m.start(),
                end=m.end(),
                text=m.group(),
                label="URGENCY_THREAT",
                severity="HIGH"
            ))

        # 6. Collect request tokens
        for m in COLLECT_REGEX.finditer(text):
            spans.append(HighlightSpan(
                start=m.start(),
                end=m.end(),
                text=m.group(),
                label="COLLECT_TRICK",
                severity="HIGH"
            ))

        # 7. Remote desktop apps
        for m in REMOTE_REGEX.finditer(text):
            spans.append(HighlightSpan(
                start=m.start(),
                end=m.end(),
                text=m.group(),
                label="REMOTE_APP",
                severity="CRITICAL"
            ))

        # Sort spans by start offset
        spans.sort(key=lambda s: s.start)
        return spans

    def generate_actions(
        self,
        verdict: str,
        category: str,
        signals_detected: Dict[str, bool],
        lang: str = "en"
    ) -> List[str]:
        actions = []

        if signals_detected.get("has_otp_request"):
            if lang == "hi":
                actions.append("अपना ओटीपी (OTP), यूपीआई पिन या सीवीवी किसी के साथ साझा न करें। बैंक कभी फोन पर पिन नहीं मांगता।")
            elif lang == "te":
                actions.append("మీ OTP, UPI పిన్ లేదా CVV నంబర్‌ను ఎవరితోనూ పంచుకోవద్దు. బ్యాంక్ అధికారులు ఎప్పుడూ పిన్ అడగరు.")
            else:
                actions.append("Do NOT share your OTP, UPI PIN, or CVV. Bank employees will NEVER ask for your secret PIN.")

        if signals_detected.get("has_collect_trick"):
            if lang == "hi":
                actions.append("कलेक्ट रिक्वेस्ट स्वीकार न करें। यूपीआई में पैसे पाने या कैशबैक के लिए कभी भी पिन दर्ज करने की आवश्यकता नहीं होती।")
            elif lang == "te":
                actions.append("కలెక్ట్ రిక్వెస్ట్‌ను ఆమోదించవద్దు. UPI లో డబ్బు పొందడానికి ఎప్పుడూ పిన్ నమోదు చేయాల్సిన అవసరం లేదు.")
            else:
                actions.append("Do NOT accept this collect request. In UPI architecture, receiving money NEVER requires entering your PIN.")

        if signals_detected.get("has_remote_app"):
            if lang == "hi":
                actions.append("AnyDesk या TeamViewer जैसे रिमोट ऐप डाउनलोड न करें। फोन से स्क्रीन शेयरिंग तुरंत बंद करें।")
            elif lang == "te":
                actions.append("AnyDesk లేదా TeamViewer వంటి రిమోట్ యాప్‌లను ఇన్‌స్టాల్ చేయవద్దు. మీ స్క్రీన్ షేర్ చేయవద్దు.")
            else:
                actions.append("Do NOT download AnyDesk, TeamViewer, or QuickSupport. Never share 9-digit remote codes with callers.")

        if signals_detected.get("has_link"):
            if lang == "hi":
                actions.append("संदेश में दिए गए किसी भी संदिग्ध लिंक पर क्लिक न करें। केवल आधिकारिक ऐप या बैंक शाखा से संपर्क करें।")
            elif lang == "te":
                actions.append("మెసేజ్‌లోని అనుమానాస్పద లింక్‌లపై క్లిక్ చేయవద్దు. మీ అధికారిక బ్యాంక్ యాప్‌ను మాత్రమే ఉపయోగించండి.")
            else:
                actions.append("Do NOT click the link. Always navigate directly to official bank websites or verified mobile apps.")

        if category == "electricity_disconnection":
            if lang == "hi":
                actions.append("एसएमएस में दिए गए मोबाइल नंबर पर फोन न करें। अपने बिजली बिल की सही स्थिति आधिकारिक पोर्टल या बिजली दफ्तर पर जांचें।")
            elif lang == "te":
                actions.append("మెసేజ్‌లోని ఫోన్ నంబర్‌కు కాల్ చేయవద్దు. అధికారిక విద్యుత్ సంస్థ వెబ్‌సైట్ ద్వారా మాత్రమే మీ బిల్లు తనిఖీ చేయండి.")
            else:
                actions.append("Do NOT call the personal mobile number. Verify overdue electricity bills directly on official DISCOM portals.")

        if category == "courier_customs_scam":
            if lang == "hi":
                actions.append("डिजिटल अरेस्ट या नारकोटिक्स के नाम पर पैसे न भेजें। पुलिस कभी स्काइप या व्हाट्सएप वीडियो कॉल पर जांच नहीं करती।")
            elif lang == "te":
                actions.append("డిజిటల్ అరెస్ట్ పేరుతో ఎవరికీ డబ్బు పంపవద్దు. పోలీసులు ఎప్పుడూ వీడియో కాల్స్‌లో విచారణ చేయరు.")
            else:
                actions.append("Do NOT transfer money under threat of 'Digital Arrest' or customs parcel contraband. Real law enforcement never interrogates via Skype.")

        # Universal fallback actions
        if verdict in ["HIGH RISK", "SUSPICIOUS"]:
            if lang == "hi":
                actions.append("यदि आपने पैसे भेज दिए हैं, तो तुरंत 1930 साइबर हेल्पलाइन पर कॉल करें या cybercrime.gov.in पर रिपोर्ट दर्ज करें।")
            elif lang == "te":
                actions.append("మీరు మోసపోయినట్లయితే వెంటనే 1930 జాతీయ సైబర్ హెల్ప్‌లైన్‌కు కాల్ చేయండి లేదా cybercrime.gov.in లో ఫిర్యాదు చేయండి.")
            else:
                actions.append("If defrauded, immediately dial National Cybercrime Helpline 1930 or lodge an incident report at cybercrime.gov.in.")
        else:
            if lang == "hi":
                actions.append("यह संदेश सामान्य प्रतीत होता है। फिर भी किसी अनजान व्यक्ति से गुप्त पिन या पासवर्ड कभी साझा न करें।")
            elif lang == "te":
                actions.append("ఈ సందేశం సురక్షితమైనదిగా కనిపిస్తుంది. ఎప్పుడూ మీ వ్యక్తిగత వివరాలను జాగ్రత్తగా ఉంచుకోండి.")
            else:
                actions.append("Content matches normal communications. Maintain standard digital payment safety and never share credentials.")

        return actions[:5]

    def generate_plain_explanation(
        self,
        verdict: str,
        score: int,
        category: str,
        evidence: List[EvidenceItem],
        lang: str = "en"
    ) -> str:
        cat_name = CATEGORY_NAMES_I18N.get(category, {}).get(lang, category)
        key_signals = [e.signal for e in evidence if e.weight > 0][:2]
        signals_text = "; ".join(key_signals) if key_signals else "Pattern anomalies detected"

        if lang == "hi":
            if verdict == "HIGH RISK":
                return f"उच्च जोखिम चेतावनी (स्कोर {score}/100): यह {cat_name} का गंभीर संकेत है। प्रमुख संकेत: {signals_text}। किसी भी लिंक पर क्लिक न करें और न ही पिन/ओटीपी साझा करें।"
            elif verdict == "SUSPICIOUS":
                return f"संदेहास्पद गतिविधि (स्कोर {score}/100): इसमें चेतावनी संकेत मिले हैं ({signals_text})। अत्यधिक सावधानी बरतें और आधिकारिक चैनल से पुष्टि करें।"
            else:
                return f"कोई मजबूत धोखाधड़ी संकेत नहीं (स्कोर {score}/100): यह संदेश प्रामाणिक प्रतीत होता है। हमेशा सामान्य सुरक्षा सतर्कता बनाए रखें।"
        elif lang == "te":
            if verdict == "HIGH RISK":
                return f"అధిక ప్రమాద హెచ్చరిక (స్కోరు {score}/100): ఇది {cat_name} మోసానికి బలమైన నిదర్శనం. ముఖ్య సంకేతాలు: {signals_text}. లింక్‌లపై క్లిక్ చేయవద్దు మరియు పిన్ పంచుకోవద్దు."
            elif verdict == "SUSPICIOUS":
                return f"అనుమానాస్పద లావాదేవీ (స్కోరు {score}/100): ఇందులో అనుమానాస్పద సంకేతాలు ఉన్నాయి ({signals_text}). అత్యంత జాగ్రత్తగా ఉండండి."
            else:
                return f"మోసపూరిత సంకేతాలు లేవు (స్కోరు {score}/100): ఈ కంటెంట్ సాధారణమైనదిగా కనిపిస్తోంది. ఎల్లప్పుడూ బ్యాంకింగ్ భద్రతను పాటించండి."
        else:
            if verdict == "HIGH RISK":
                return f"High Risk Alert (Score {score}/100): Strong evidence of {cat_name}. Key detected signals: {signals_text}. Do not click links or reveal credentials."
            elif verdict == "SUSPICIOUS":
                return f"Suspicious Activity Detected (Score {score}/100): Contains warning signals ({signals_text}). Exercise extreme caution and verify independently."
            else:
                return f"No Strong Scam Signals Found (Score {score}/100): Content does not match known scam patterns and appears to be legitimate communications. Always maintain standard security vigilance."

    def generate_prefilled_1930_summary(
        self,
        text: str,
        category: str,
        score: int,
        evidence: List[EvidenceItem],
        urls: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        phones = list(set(PHONE_REGEX.findall(text)))
        vpas = list(set(UPI_VPA_REGEX.findall(text)))
        extracted_urls = [u["url"] for u in urls]

        key_reasons = [e.signal for e in evidence if e.weight > 0][:4]
        cat_title = CATEGORY_NAMES_I18N.get(category, {}).get("en", category)

        narrative = (
            f"INCIDENT COMPLAINT SUMMARY FOR 1930 HELPLINE / CYBERCRIME.GOV.IN:\n"
            f"1. Threat Classification: {cat_title} (AI Heuristic Risk Score: {score}/100)\n"
            f"2. Suspect Identifiers:\n"
            f"   - Phone Number(s): {', '.join(phones) if phones else 'Not disclosed / Sender header'}\n"
            f"   - Suspect URL(s): {', '.join(extracted_urls) if extracted_urls else 'None'}\n"
            f"   - Suspect UPI VPA(s): {', '.join(vpas) if vpas else 'None'}\n"
            f"3. Verifiable Technical Evidence:\n" +
            "\n".join([f"   * {r}" for r in key_reasons]) +
            f"\n4. Original Content Snippet:\n   \"{text[:300]}\"\n"
            f"5. Requested Cyber Police Action: Immediate block of beneficiary UPI VPA, blacklisting of sender headers, and suspension of malicious domains."
        )

        return {
            "helpline": "1930",
            "portal": "https://cybercrime.gov.in",
            "incident_category": cat_title,
            "suspect_phones": phones,
            "suspect_urls": extracted_urls,
            "suspect_vpas": vpas,
            "formal_complaint_narrative": narrative
        }

    def fuse(
        self,
        input_type: str,
        text: str,
        nlp_result: Dict[str, Any],
        rule_result: Dict[str, Any],
        url_results: List[Dict[str, Any]],
        qr_result: Optional[Dict[str, Any]] = None,
        ocr_result: Optional[Dict[str, Any]] = None,
        language_override: Optional[str] = "auto"
    ) -> SafetyReport:
        # Determine language
        detected_lang = nlp_result.get("language", "en")
        effective_lang = language_override if language_override in ["en", "hi", "te"] else detected_lang

        evidence_items: List[EvidenceItem] = []
        waterfall_steps: List[WaterfallStep] = []
        running_score = 0.0

        # Baseline
        waterfall_steps.append(WaterfallStep(
            component="Baseline Score",
            points=0.0,
            running_total=0.0,
            explanation="Initial clean state prior to signal evaluation."
        ))

        # 1. Collect Rule signals
        rule_signals = rule_result.get("matched_rules", [])
        for r in rule_signals:
            evidence_items.append(EvidenceItem(
                signal=r["signal"],
                source_module=r["source_module"],
                weight=r["weight"],
                severity=r.get("severity", "MEDIUM")
            ))

        rule_score = rule_result.get("rule_score", 0.0)
        is_genuine_alert = rule_result.get("is_genuine_alert", False)
        hard_override = rule_result.get("hard_override_high_risk", False)

        # 2. Collect URL signals
        max_url_score = 0.0
        for u in url_results:
            if u["url_score"] > max_url_score:
                max_url_score = u["url_score"]
            for s in u["signals"]:
                evidence_items.append(EvidenceItem(
                    signal=s["signal"],
                    source_module=s["source_module"],
                    weight=s["weight"],
                    severity=s.get("severity", "MEDIUM")
                ))

        # 3. Collect QR signals
        qr_score = 0.0
        if qr_result and qr_result.get("has_qr"):
            qr_score = qr_result.get("qr_score", 0.0)
            for s in qr_result.get("signals", []):
                evidence_items.append(EvidenceItem(
                    signal=s["signal"],
                    source_module=s["source_module"],
                    weight=s["weight"],
                    severity=s.get("severity", "MEDIUM")
                ))

        # 4. Calibrated NLP contribution
        predicted_category = nlp_result.get("category", "legitimate")
        nlp_confidence = nlp_result.get("confidence", 0.5)
        
        if predicted_category != "legitimate":
            nlp_risk_score = 42.0 + (nlp_confidence * 48.0)
            evidence_items.append(EvidenceItem(
                signal=f"NLP Scam Intent Classifier: Categorized as '{predicted_category}' with {nlp_confidence * 100:.1f}% confidence.",
                source_module="NLP_CLASSIFIER",
                weight=round(nlp_risk_score * 0.5, 1),
                severity="HIGH" if nlp_confidence >= 0.70 else "MEDIUM"
            ))
        else:
            nlp_risk_score = 0.0
            if nlp_confidence >= 0.70:
                evidence_items.append(EvidenceItem(
                    signal=f"NLP Classifier: Pattern matches verified legitimate service notification ({nlp_confidence * 100:.1f}% confidence).",
                    source_module="NLP_CLASSIFIER",
                    weight=-25.0,
                    severity="INFO"
                ))

        # Build Waterfall steps
        running_score += nlp_risk_score if predicted_category != "legitimate" else 0.0
        waterfall_steps.append(WaterfallStep(
            component="NLP Scam Classifier",
            points=round(nlp_risk_score if predicted_category != "legitimate" else 0.0, 1),
            running_total=round(running_score, 1),
            explanation=f"Calibrated probability on category '{predicted_category}' ({nlp_confidence * 100:.1f}% confidence)."
        ))

        if rule_score > 0:
            running_score += rule_score
            waterfall_steps.append(WaterfallStep(
                component="Rule Safety Layer",
                points=round(rule_score, 1),
                running_total=round(running_score, 1),
                explanation="Deterministic security rules matched (e.g. credential theft, collect trick, urgency threat)."
            ))

        if max_url_score > 0:
            running_score += max_url_score
            waterfall_steps.append(WaterfallStep(
                component="Static URL Scanner",
                points=round(max_url_score, 1),
                running_total=round(running_score, 1),
                explanation="Static lexical analysis flagged brand typosquatting, suspicious TLD, or IP host."
            ))

        if qr_score > 0:
            running_score += qr_score
            waterfall_steps.append(WaterfallStep(
                component="QR / VPA Verification",
                points=round(qr_score, 1),
                running_total=round(running_score, 1),
                explanation="UPI URI anomalies detected (collect request pre-fill or payee mismatch)."
            ))

        # 4b. Community Reputation Consensus Check (Strictly Capped)
        community_bonus = 0.0
        candidate_entities = []
        if text:
            for ph in PHONE_REGEX.findall(text):
                candidate_entities.append(("phone", ph))
            for vpa in UPI_VPA_REGEX.findall(text):
                candidate_entities.append(("vpa", vpa))
        for u in url_results:
            if u.get("url"):
                candidate_entities.append(("url", u["url"]))

        for ent_type, ent_val in candidate_entities[:5]:
            try:
                rep = lookup_community_reputation(ent_type, ent_val)
                if rep.get("consensus_reached") and rep.get("fusion_points", 0) > 0:
                    pts = min(15.0, rep["fusion_points"])
                    if pts > community_bonus:
                        community_bonus = pts
                    evidence_items.append(EvidenceItem(
                        signal=f"Community Reputation Consensus: Entity '{rep['masked_display']}' confirmed suspicious by {rep['distinct_reporters']} independent reporters.",
                        source_module="COMMUNITY_REPUTATION",
                        weight=pts,
                        severity="HIGH" if pts >= 10 else "MEDIUM"
                    ))
            except Exception:
                pass

        if community_bonus > 0:
            running_score += community_bonus
            waterfall_steps.append(WaterfallStep(
                component="Community Reputation Consensus",
                points=round(community_bonus, 1),
                running_total=round(running_score, 1),
                explanation="Entity flagged by verified independent community reporters."
            ))

        # 5. Multi-Detector Evidence Fusion
        has_official_url = any(u.get("is_official") for u in url_results)

        max_signal = max(
            nlp_risk_score if predicted_category != "legitimate" else 0.0,
            rule_score,
            max_url_score,
            qr_score
        )
        if community_bonus > 0:
            # Strictly cap community reputation: can never push a safe message to HIGH RISK on its own
            if max_signal <= settings.SAFE_MAX_SCORE:
                max_signal = min(49.0, max_signal + community_bonus)
            else:
                max_signal = min(100.0, max_signal + community_bonus)

        # Corroborating signals boost
        corroborating = 0
        if predicted_category != "legitimate" and nlp_confidence >= 0.70: corroborating += 1
        if rule_score >= 35.0: corroborating += 1
        if max_url_score >= 35.0: corroborating += 1
        if qr_score >= 35.0: corroborating += 1

        if corroborating >= 2:
            max_signal = min(100.0, max_signal + 12.0)
            waterfall_steps.append(WaterfallStep(
                component="Multi-Detector Corroboration",
                points=12.0,
                running_total=round(max_signal, 1),
                explanation="Cross-module verification bonus: Multiple independent engines confirmed the threat."
            ))

        # Hard Overrides
        if hard_override:
            max_signal = max(max_signal, 85.0)
            override_msg = rule_result.get("override_reason", "Safety Hard Override Triggered: High-severity pattern detected.")
            evidence_items.append(EvidenceItem(
                signal=override_msg,
                source_module="RULE_SAFETY_LAYER",
                weight=50.0,
                severity="CRITICAL"
            ))
            waterfall_steps.append(WaterfallStep(
                component="Safety Hard Override",
                points=round(max_signal - running_score, 1) if max_signal > running_score else 0.0,
                running_total=round(max_signal, 1),
                explanation=override_msg
            ))
        elif max_url_score >= 70.0 and any("Brand Impersonation" in e.signal or "Typosquatting" in e.signal for e in evidence_items):
            max_signal = max(max_signal, 85.0)
            waterfall_steps.append(WaterfallStep(
                component="Brand Spoofing Override",
                points=15.0,
                running_total=round(max_signal, 1),
                explanation="Critical brand impersonation of authorized financial institution."
            ))
        elif qr_score >= 70.0:
            max_signal = max(max_signal, 82.0)

        # Genuine alert or verified official URL suppression
        has_active_otp_request = rule_result.get("signals_detected", {}).get("has_otp_request", False)
        if (is_genuine_alert or has_official_url) and not hard_override and not has_active_otp_request and max_url_score < 35.0 and qr_score < 35.0:
            suppression_delta = max_signal - min(max_signal, 20.0)
            max_signal = min(max_signal, 20.0)
            waterfall_steps.append(WaterfallStep(
                component="Legitimate Safety Suppression",
                points=-round(suppression_delta, 1),
                running_total=round(max_signal, 1),
                explanation="Verified safety advisory context ('NEVER share OTP') or authorized official registry domain."
            ))

        final_risk_score = int(round(max(0.0, min(100.0, max_signal))))

        # Final verdict thresholding
        if final_risk_score <= settings.SAFE_MAX_SCORE:
            verdict = "SAFE"
        elif final_risk_score <= settings.SUSPICIOUS_MAX_SCORE:
            verdict = "SUSPICIOUS"
        else:
            verdict = "HIGH RISK"

        # Sort evidence items by severity / weight
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
        evidence_items.sort(key=lambda x: (severity_order.get(x.severity, 5), -abs(x.weight)))

        # Recommended actions
        signals_detected = rule_result.get("signals_detected", {})
        actions = self.generate_actions(verdict, predicted_category, signals_detected, effective_lang)

        # Plain language explanation
        explanation = self.generate_plain_explanation(
            verdict, final_risk_score, predicted_category, evidence_items, effective_lang
        )

        # RAG citations
        retrieval_query = f"{predicted_category} {text[:200]}"
        raw_citations = rag_retriever.retrieve(retrieval_query, category=predicted_category, top_k=2)
        citations = [
            RAGCitation(
                title=c["title"],
                content=c["content"],
                source=c["source"],
                relevance_score=c.get("relevance_score", 0.0)
            )
            for c in raw_citations
        ]

        # Extract highlight spans
        highlight_spans = self.extract_highlight_spans(text)

        # Localized Scam Story Timeline
        scam_story = scam_story_engine.get_timeline(predicted_category, lang=effective_lang) if verdict in ["HIGH RISK", "SUSPICIOUS"] else None

        # Pre-filled 1930 Cybercrime Summary
        prefilled_1930 = self.generate_prefilled_1930_summary(text, predicted_category, final_risk_score, evidence_items, url_results) if verdict in ["HIGH RISK", "SUSPICIOUS"] else None

        return SafetyReport(
            verdict=verdict,
            risk_score=final_risk_score,
            detected_category=predicted_category,
            language=effective_lang,
            confidence=round(nlp_confidence, 2),
            evidence=evidence_items,
            highlight_spans=highlight_spans,
            waterfall=waterfall_steps,
            scam_story=scam_story,
            prefilled_1930_summary=prefilled_1930,
            recommended_actions=actions,
            citations=citations,
            plain_language_explanation=explanation,
            masked_input="",
            is_simulated=False
        )

risk_engine = RiskFusionEngine()
