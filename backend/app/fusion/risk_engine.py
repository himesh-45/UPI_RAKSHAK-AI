from typing import Dict, Any, List, Optional
from ..config import settings
from ..models.schemas import EvidenceItem, RAGCitation, SafetyReport
from ..rag.retriever import rag_retriever

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
    "lottery_prize": {
        "en": "Lottery & Advance-Fee Prize Scam",
        "hi": "केबीसी/लकी ड्रॉ लॉटरी धोखाधड़ी",
        "te": "లక్కీ డ్రా మరియు లాటరీ మోసం"
    },
    "fake_customer_support": {
        "en": "Fake Customer Support & Remote Access",
        "hi": "फर्जी कस्टमर केयर व रिमोट ऐप धोखा",
        "te": "నకిలీ కస్టమర్ కేర్ & రిమోట్ యాక్సెస్ మోసం"
    },
    "otp_pin_theft": {
        "en": "OTP & UPI PIN Theft",
        "hi": "ओटीपी और यूपीआई पिन चोरी",
        "te": "ఓటీపీ మరియు యూపీఐ పిన్ దొంగతనం"
    },
    "fake_govt_scheme": {
        "en": "Fake Government Subsidy Scheme",
        "hi": "फर्जी सरकारी योजना व सब्सिडी धोखा",
        "te": "నకిలీ ప్రభుత్వ పథకం సాయం మోసం"
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
    """

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
                actions.append("Do NOT call the personal mobile number in the message. Check your real balance directly on your state utility portal.")

        # Standard emergency reporting action
        if verdict in ["HIGH RISK", "SUSPICIOUS"]:
            if lang == "hi":
                actions.append("यदि आपने पैसे गंवाए हैं, तो तुरंत राष्ट्रीय साइबर हेल्पलाइन 1930 पर कॉल करें या cybercrime.gov.in पर रिपोर्ट दर्ज करें।")
            elif lang == "te":
                actions.append("ఒకవేళ మోసపోయి డబ్బు కోల్పోతే, వెంటనే జాతీయ సైబర్ హెల్ప్‌లైన్ 1930 కు కాల్ చేయండి లేదా cybercrime.gov.in లో ఫిర్యాదు చేయండి.")
            else:
                actions.append("If you suspect fraud or lost money, immediately call national helpline 1930 or file an incident at cybercrime.gov.in.")
        else:
            if lang == "hi":
                actions.append("सावधानी बरतें: कोई मजबूत धोखा नहीं मिला, लेकिन सतर्क रहें और कभी भी गोपनीय पासवर्ड किसी को न बताएं।")
            elif lang == "te":
                actions.append("జాగ్రత్త వహించండి: బలమైన మోసపూరిత సంకేతాలు కనిపించలేదు. అయినా ఎప్పుడూ OTP ని ఇతరులకు చెప్పవద్దు.")
            else:
                actions.append("Remain cautious: No strong scam patterns were found, but never share credentials or transfer funds to unknown entities.")

        return actions

    def generate_plain_explanation(
        self,
        verdict: str,
        score: int,
        category: str,
        evidence: List[EvidenceItem],
        lang: str = "en"
    ) -> str:
        cat_name = CATEGORY_NAMES_I18N.get(category, {}).get(lang, category)
        top_signals = [e.signal for e in evidence if e.severity in ["CRITICAL", "HIGH"]][:2]
        signals_text = "; ".join(top_signals) if top_signals else "Multiple behavioral risk factors detected."

        if lang == "hi":
            if verdict == "HIGH RISK":
                return f"उच्च जोखिम चेतावनी (स्कोर {score}/100): यह संदेश '{cat_name}' की श्रेणी में आता है। मुख्य खतरे: {signals_text} कृपया किसी लिंक पर क्लिक न करें और न ही पिन/ओटीपी साझा करें।"
            elif verdict == "SUSPICIOUS":
                return f"संदिग्ध गतिविधि (स्कोर {score}/100): इस सामग्री में कुछ अनियमितताएं पाई गई हैं ({signals_text})। आगे बढ़ने से पहले सीधे अपने बैंक या सेवा प्रदाता से पुष्टि करें।"
            else:
                return f"सुरक्षित प्रतीत होता है (स्कोर {score}/100): कोई मजबूत धोखाधड़ी के संकेत नहीं मिले। यह एक सामान्य संदेश लगता है, फिर भी कभी भी अपना पासवर्ड या ओटीपी साझा न करें।"
        elif lang == "te":
            if verdict == "HIGH RISK":
                return f"అధిక ప్రమాద హెచ్చరిక (స్కోర్ {score}/100): ఈ సందేశం '{cat_name}' కు సంబంధించినది. ముఖ్య ఆధారాలు: {signals_text} ఎలాంటి లింక్ ఓపెన్ చేయవద్దు మరియు ఎవరికీ పిన్ లేదా OTP చెప్పవద్దు."
            elif verdict == "SUSPICIOUS":
                return f"అనుమానాస్పద హెచ్చరిక (స్కోర్ {score}/100): ఇందులో కొన్ని అనుమానాస్పద సంకేతాలు గుర్తించబడ్డాయి ({signals_text}). జాగ్రత్తగా ఉండండి."
            else:
                return f"సురక్షితంగా కనిపిస్తోంది (స్కోర్ {score}/100): ఎటువంటి బలమైన మోసపూరిత లక్షణాలు కనిపించలేదు. అయినప్పటికీ మీ రహస్య పిన్ ఎవరితోనూ పంచుకోవద్దు."
        else:
            if verdict == "HIGH RISK":
                return f"High Risk Alert (Score {score}/100): Strong evidence of {cat_name}. Key detected signals: {signals_text}. Do not click links or reveal credentials."
            elif verdict == "SUSPICIOUS":
                return f"Suspicious Activity Detected (Score {score}/100): Contains warning signals ({signals_text}). Exercise extreme caution and verify independently."
            else:
                return f"No Strong Scam Signals Found (Score {score}/100): Content does not match known scam patterns and appears to be legitimate communications. Always maintain standard security vigilance."

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

        # 1. Collect Rule signals
        rule_signals = rule_result.get("matched_rules", [])
        for r in rule_signals:
            evidence_items.append(EvidenceItem(
                signal=r["signal"],
                source_module=r["source_module"],
                weight=r["weight"],
                severity=r.get("severity", "MEDIUM")
            ))

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

        # 4. NLP contribution
        predicted_category = nlp_result.get("category", "legitimate")
        nlp_confidence = nlp_result.get("confidence", 0.5)
        
        # 4. Calibrated NLP contribution
        predicted_category = nlp_result.get("category", "legitimate")
        nlp_confidence = nlp_result.get("confidence", 0.5)
        
        if predicted_category != "legitimate":
            nlp_risk_score = nlp_confidence * 85.0
            evidence_items.append(EvidenceItem(
                signal=f"NLP Scam Intent Classifier: Categorized as '{predicted_category}' with {nlp_confidence * 100:.1f}% confidence.",
                source_module="NLP_CLASSIFIER",
                weight=round(nlp_risk_score * 0.5, 1),
                severity="HIGH" if nlp_confidence >= 0.75 else "MEDIUM"
            ))
        else:
            nlp_risk_score = max(0.0, (1.0 - nlp_confidence) * 30.0)
            if nlp_confidence >= 0.70:
                evidence_items.append(EvidenceItem(
                    signal=f"NLP Classifier: Pattern matches verified legitimate service notification ({nlp_confidence * 100:.1f}% confidence).",
                    source_module="NLP_CLASSIFIER",
                    weight=-25.0,
                    severity="INFO"
                ))

        # 5. Multi-Detector Evidence Fusion
        rule_score = rule_result.get("rule_score", 0.0)
        is_genuine_alert = rule_result.get("is_genuine_alert", False)
        hard_override = rule_result.get("hard_override_high_risk", False)
        has_official_url = any(u.get("is_official") for u in url_results)

        # Primary risk is driven by the strongest detector signal
        max_signal = max(
            nlp_risk_score if predicted_category != "legitimate" else 0.0,
            rule_score,
            max_url_score,
            qr_score
        )

        # Corroborating signals boost confidence
        corroborating = 0
        if predicted_category != "legitimate" and nlp_confidence >= 0.70: corroborating += 1
        if rule_score >= 35.0: corroborating += 1
        if max_url_score >= 35.0: corroborating += 1
        if qr_score >= 35.0: corroborating += 1

        if corroborating >= 2:
            max_signal = min(100.0, max_signal + 12.0)

        # Hard Overrides
        if hard_override:
            max_signal = max(max_signal, 85.0)
            evidence_items.append(EvidenceItem(
                signal=rule_result.get("override_reason", "Safety Hard Override Triggered: High-severity pattern detected."),
                source_module="RULE_SAFETY_LAYER",
                weight=50.0,
                severity="CRITICAL"
            ))
        elif max_url_score >= 70.0 and any("Brand Impersonation" in e.signal or "Typosquatting" in e.signal for e in evidence_items):
            max_signal = max(max_signal, 85.0)
        elif qr_score >= 70.0:
            max_signal = max(max_signal, 82.0)

        # Genuine alert or verified official URL suppression (only when no malicious link or override)
        if (is_genuine_alert or has_official_url) and not hard_override and max_url_score < 35.0 and qr_score < 35.0:
            max_signal = min(max_signal, 20.0)

        final_risk_score = int(round(max(0.0, min(100.0, max_signal))))

        # Verdict thresholding
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

        return SafetyReport(
            verdict=verdict,
            risk_score=final_risk_score,
            detected_category=predicted_category,
            language=effective_lang,
            confidence=round(nlp_confidence, 2),
            evidence=evidence_items,
            recommended_actions=actions,
            citations=citations,
            plain_language_explanation=explanation,
            masked_input="",
            is_simulated=False
        )

risk_engine = RiskFusionEngine()
