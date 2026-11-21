from typing import List, Dict, Any, Optional
from ..models.schemas import SafetyReport

def format_assistant_response(report: SafetyReport, user_query: str, lang: str = "en") -> str:
    verdict = report.verdict
    score = report.risk_score
    cat = report.detected_category
    evidence_items = report.evidence[:3]
    actions = report.recommended_actions
    citations = report.citations

    # 1. Telugu Response Template
    if lang == "te":
        if verdict == "HIGH RISK":
            suspicious_bullets = "\n".join([f"- **ముఖ్య ఆధారం**: {e.signal}" for e in evidence_items])
            actions_bullets = "\n".join([f"- {a}" for a in actions])
            rag_note = citations[0].content if citations else "UPI లో డబ్బు పొందడానికి పిన్ నమోదు చేయాల్సిన అవసరం లేదు."

            return f"""### 🚨 అధిక ప్రమాదం (హై రిస్క్ హెచ్చరిక) — స్కోర్: {score}/100

మీరు అడిగిన సందేశం/కంటెంట్ పరిశీలించిన తర్వాత, ఇది **మోసపూరితమైనది (SCAM)** అని స్పష్టమైన ఆధారాలు లభించాయి.

#### 🔍 ఏమి అనుమానాస్పదంగా ఉంది?
{suspicious_bullets}

#### 🛑 మీరు ఏమి చేయకూడదు?
- సందేశంలోని లింక్‌లపై ఎట్టి పరిస్థితుల్లోనూ క్లిక్ చేయవద్దు.
- ఎవరికీ మీ **UPI పిన్ (PIN)**, **OTP** లేదా **CVV** నంబర్ చెప్పవద్దు.
- AnyDesk లేదా TeamViewer వంటి రిమోట్ కంట్రోల్ యాప్‌లను డౌన్‌లోడ్ చేయవద్దు.
- డబ్బు పొందడానికి కలెక్ట్ రిక్వెస్ట్‌లను ఆమోదించవద్దు (డబ్బు తీసుకోవడానికి పిన్ అవసరం లేదు).

#### ✅ ఇప్పుడు మీరు ఏమి చేయాలి?
{actions_bullets}

#### 📋 రిపోర్ట్ చేసే విధానం (సాయం కోసం):
1. మీకు డబ్బు కట్ అయితే, తక్షణమే జాతీయ సైబర్ హెల్ప్‌లైన్ **1930** కు కాల్ చేయండి.
2. వెంటనే మీ బ్యాంక్ కస్టమర్ కేర్‌కు ఫిర్యాదు చేసి UPI మరియు కార్డులను బ్లాక్ చేయించండి.
3. [cybercrime.gov.in](https://cybercrime.gov.in) పోర్టల్‌లో ఆన్‌లైన్ ఫిర్యాదు నమోదు చేయండి.

> **అధికారిక మార్గదర్శకం**: {rag_note}
"""
        elif verdict == "SUSPICIOUS":
            suspicious_bullets = "\n".join([f"- {e.signal}" for e in evidence_items])
            return f"""### ⚠️ అనుమానాస్పద కంటెంట్ హెచ్చరిక — స్కోర్: {score}/100

ఈ సందేశంలో కొన్ని అనుమానాస్పద సంకేతాలు గుర్తించబడ్డాయి. పూర్తిగా నిర్ధారించుకునే వరకు జాగ్రత్తగా ఉండండి.

#### 🔍 కనిపించిన సంకేతాలు:
{suspicious_bullets}

#### ✅ జాగ్రత్తలు:
- మీ బ్యాంక్ లేదా సర్వీస్ ప్రొవైడర్‌ను అధికారిక నంబర్ ద్వారా సంప్రదించండి.
- ఎవరికీ వ్యక్తిగత పాస్‌వర్డ్‌లు లేదా బ్యాంకింగ్ వివరాలు పంపవద్దు.
- మోసం జరిగితే **1930** హెల్ప్‌లైన్ నంబర్‌ను సంప్రదించండి.
"""
        else:
            return f"""### ✅ సురక్షితంగా కనిపిస్తోంది — స్కోర్: {score}/100

ఈ సందేశంలో ఎలాంటి బలమైన మోసపూరిత సంకేతాలు లేదా ప్రమాదకరమైన లింక్‌లు కనిపించలేదు. ఇది సాధారణ సమాచారంగా కనిపిస్తోంది.

#### 🛡️ భద్రతా చిట్కా:
- బ్యాంక్ లేదా ఆన్‌లైన్ సేవలు ఎప్పుడూ ఫోన్ ద్వారా మీ రహస్య పాస్‌వర్డ్‌లు అడగవని గుర్తుంచుకోండి.
- ఎల్లప్పుడూ అధికారిక యాప్‌లను మాత్రమే ఉపయోగించండి.
"""

    # 2. Hindi Response Template
    elif lang == "hi":
        if verdict == "HIGH RISK":
            suspicious_bullets = "\n".join([f"- **मुख्य प्रमाण**: {e.signal}" for e in evidence_items])
            actions_bullets = "\n".join([f"- {a}" for a in actions])
            rag_note = citations[0].content if citations else "यूपीआई में पैसे प्राप्त करने के लिए कभी भी पिन डालने की आवश्यकता नहीं होती।"

            return f"""### 🚨 उच्च जोखिम चेतावनी (HIGH RISK) — स्कोर: {score}/100

आपके द्वारा भेजे गए संदेश/सामग्री के विश्लेषण से स्पष्ट होता है कि यह एक **धोखाधड़ी (SCAM)** का प्रयास है।

#### 🔍 क्या संदिग्ध पाया गया?
{suspicious_bullets}

#### 🛑 आपको क्या बिल्कुल नहीं करना है?
- संदेश में दिए गए किसी भी लिंक पर क्लिक न करें।
- अपना **यूपीआई पिन (UPI PIN)**, **ओटीपी (OTP)** या **सीवीवी (CVV)** किसी को न बताएं।
- पैसे पाने के लिए कलेक्ट रिक्वेस्ट स्वीकार न करें (पैसे लेने के लिए पिन नहीं लगता)।
- AnyDesk या TeamViewer जैसे स्क्रीन-शेयरिंग ऐप डाउनलोड न करें।

#### ✅ अब आपको क्या करना चाहिए?
{actions_bullets}

#### 📞 शिकायत और सहायता के कदम:
1. यदि आपके खाते से पैसे कट चुके हैं, तो तुरंत राष्ट्रीय साइबर हेल्पलाइन **1930** पर कॉल करें।
2. तुरंत अपने बैंक के कस्टमर केयर से संपर्क करके अपना खाता/कार्ड ब्लॉक करवाएं।
3. [cybercrime.gov.in](https://cybercrime.gov.in) पर औपचारिक शिकायत दर्ज करें।

> **आधिकारिक सुरक्षा नियम**: {rag_note}
"""
        elif verdict == "SUSPICIOUS":
            suspicious_bullets = "\n".join([f"- {e.signal}" for e in evidence_items])
            return f"""### ⚠️ संदिग्ध गतिविधि चेतावनी — स्कोर: {score}/100

इस संदेश में कुछ असामान्य या जोखिम भरे लक्षण पाए गए हैं।

#### 🔍 पाए गए लक्षण:
{suspicious_bullets}

#### ✅ सुरक्षा सुझाव:
- सीधे अपने बैंक की शाखा या आधिकारिक ऐप से संपर्क करके स्थिति स्पष्ट करें।
- अनजान कॉलर के कहने पर कोई भुगतान न करें।
- जरूरत पड़ने पर राष्ट्रीय साइबर हेल्पलाइन **1930** पर संपर्क करें।
"""
        else:
            return f"""### ✅ सुरक्षित प्रतीत होता है — स्कोर: {score}/100

इस संदेश में किसी ज्ञात धोखाधड़ी के मजबूत संकेत नहीं मिले हैं। यह एक प्रामाणिक सूचना प्रतीत होती है।

#### 🛡️ सावधानी:
- सुरक्षित रहें और याद रखें कि कोई भी बैंक कर्मचारी कभी आपका पासवर्ड या ओटीपी नहीं मांगता।
"""

    # 3. English Response Template (Default)
    else:
        if verdict == "HIGH RISK":
            suspicious_bullets = "\n".join([f"- **Evidence**: {e.signal}" for e in evidence_items])
            actions_bullets = "\n".join([f"- {a}" for a in actions])
            rag_note = citations[0].content if citations else "In UPI architecture, receiving money never requires entering a PIN."

            return f"""### 🚨 High Risk Scam Warning — Score: {score}/100

Based on multi-layer evidence analysis, this content exhibits **confirmed fraud indicators**.

#### 🔍 What Looks Suspicious?
{suspicious_bullets}

#### 🛑 What NOT To Do:
- **Do NOT click** any link provided in the message.
- **Do NOT enter or share your UPI PIN, OTP, or CVV** under any circumstance.
- **Do NOT accept UPI collect requests**; receiving money NEVER requires entering your PIN.
- **Do NOT download** remote desktop apps (AnyDesk, TeamViewer, QuickSupport).

#### ✅ What To Do Right Now:
{actions_bullets}

#### 📞 Emergency Reporting Steps:
1. **Call 1930 Immediately**: Dial the National Cyber Crime Reporting Helpline (within the Golden Hour) to freeze illicit transfers.
2. **Alert Your Bank**: Contact your bank's 24x7 fraud desk to freeze NetBanking and hotlist cards.
3. **Lodge Official Complaint**: File an incident report with transaction UTR at [cybercrime.gov.in](https://cybercrime.gov.in).

> **Verified Security Knowledge**: {rag_note}
"""
        elif verdict == "SUSPICIOUS":
            suspicious_bullets = "\n".join([f"- {e.signal}" for e in evidence_items])
            return f"""### ⚠️ Suspicious Content Warning — Score: {score}/100

This content displays several anomalous patterns that warrant caution.

#### 🔍 Warning Signals:
{suspicious_bullets}

#### ✅ Recommended Actions:
- Do not make payments or provide information based solely on this message.
- Verify directly through your bank's official helpline or official website.
- In case of unauthorized debits, immediately dial **1930**.
"""
        else:
            return f"""### ✅ Safe — No Strong Scam Signals Found (Score: {score}/100)

Our multi-signal detectors analyzed this content and found no indicators of credential theft, urgency coercion, deceptive links, or malicious QR codes.

#### 🛡️ Security Best Practice:
- Always maintain vigilance: banks will never ask for your PIN or OTP via unsolicited communications.
"""
