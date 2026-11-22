import re
from typing import Dict, Any, List, Optional

# Agency Impersonation Patterns (English uses \b, Indic scripts avoid \b)
AGENCY_PATTERNS = [
    re.compile(r'(?i)\b(?:cbi|central bureau of investigation|ed|enforcement directorate|nia|ncb|narcotics control bureau|mumbai crime branch|delhi police|mumbai police|crime branch|cyber crime cell|cyber cell|cyber police|supreme court(?: of india)?|customs department|customs officer|customs investigation|interpol|national central bureau)\b'),
    re.compile(r'(?i)(?:सीबीआई|ईडी|प्रवर्तन निदेशालय|नारकोटिक्स|क्राइम ब्रांच|मुंबई पुलिस|दिल्ली पुलिस|कस्टम्स|साइबर सेल|साइबर पुलिस|सुप्रीम कोर्ट|इंटरपोल|मजिस्ट्रेट)'),
    re.compile(r'(?i)(?:సీబీఐ|ఈడీ|నార్కోటిక్స్|క్రైమ్ బ్రాంచ్|ముంబై పోలీస్|ఢిల్లీ పోలీస్|కస్టమ్స్|సైబర్ క్రైమ్|సైబర్ సెల్|సైబర్ పోలీస్|సుప్రీం కోర్టు|ఇంటర్[\u200c]?పోల్|మేజిస్ట్రేట్)')
]

# Contraband / Crimes Patterns
CONTRABAND_PATTERNS = [
    re.compile(r'(?i)\b(?:parcel|consignment|courier|fedex|dhl|bluedart|package)\b.*?\b(?:mdma|drugs|narcotics|contraband|fake passports?|illegal sims?|weapons|money laundering|terror (?:funding|financing)|hawala|counterfeit)\b'),
    re.compile(r'(?i)\b(?:mdma|drugs|narcotics|contraband|illegal sims?|weapons|hawala|money laundering|terror (?:funding|financing)|fake passports?)\b.*?\b(?:parcel|consignment|courier|seized|customs|confiscated|intercepted|compromised)\b'),
    re.compile(r'(?i)\b(?:hawala racket|money laundering|terror financing|child exploitation)\b'),
    re.compile(r'(?i)(?:पार्सल|कूरियर|कंसाइनमेंट).*?(?:ड्रग्स|एमडीएमए|नशीला|अवैध सिम|मनी लॉन्ड्रिंग|जब्त|हथियार|फर्जी पासपोर्ट|हवाला)'),
    re.compile(r'(?i)(?:ड्रग्स|एमडीएमए|नशीला पदार्थ|अवैध सिम|हवाला|मनी लॉन्ड्रिंग).*?(?:पार्सल|जब्त|बरामद)'),
    re.compile(r'(?i)(?:పార్శిల్|కొరియర్|కన్సైన్‌మెంట్).*?(?:డ్రగ్స్|గంజాయి|నార్కోటిక్స్|సీజ్|అక్రమ సిమ్|మనీ లాండరింగ్|నకిలీ పాస్‌పోర్ట్|హవాలా)'),
    re.compile(r'(?i)(?:డ్రగ్స్|గంజాయి|నార్కోటిక్స్|అక్రమ సిమ్|హవాలా|మనీ లాండరింగ్).*?(?:పార్శిల్|సీజ్|లభించాయి|పట్టుబడింది)')
]

# Video Confinement / "Digital Arrest" Patterns
CONFINEMENT_PATTERNS = [
    re.compile(r'(?i)\b(?:digital arrest|virtual court|virtual hearing|virtual interrogation|virtual detention|virtual custody|stay on (?:skype|video call|whatsapp call)|keep (?:your )?camera on|do not (?:disconnect|cut the call|speak to anyone)|under (?:continuous )?surveillance|room isolation|digital custody)\b'),
    re.compile(r'(?i)\b(?:skype|video call|video conference)\b.*?\b(?:statement|interrogation|custody|detention|hearing|clearance)\b'),
    re.compile(r'(?i)(?:डिजिटल अरेस्ट|डिजिटल हिरासत|डिजिटल कस्टडी|वर्चुअल कस्टडी|वर्चुअल कोर्ट|स्काइप|वीडियो कॉल|कैमरा ऑन|कैमरा चालू|कॉल मत काटना|डिस्कनेक्ट न करें|कमरे का दरवाजा बंद|वीडियो जांच)'),
    re.compile(r'(?i)(?:డిజిటల్ అరెస్ట్|డిజిటల్ అదుపు|డిజిటల్ కస్టడీ|వర్చువల్ కస్టడీ|వర్చువల్ కోర్టు|స్కైప్|వీడియో కాల్|వీడియో ద్వారా|కెమెరా ఆన్|కాల్ కట్ చేయవద్దు|గదిలో ఒంటరిగా|వీడియో విచారణ)')
]

# Escrow / Verification Transfer Trap
FINANCIAL_TRAP_PATTERNS = [
    re.compile(r'(?i)\b(?:rbi (?:escrow|safe|verification|security) account|reserve bank of india verification|supreme court account|government (?:treasury|safe|escrow) account|verification deposit|fund clearance|refundable security|clearance verification bond|security deposit to avoid arrest)\b'),
    re.compile(r'(?i)(?:आरबीआई.*?(?:सुरक्षित|एस्क्रो|सत्यापन|खाता)|सरकारी (?:एस्क्रो|खाता|ट्रेजरी)|रिफंडेबल राशि|क्लियरेंस के लिए पैसे|खाता सत्यापन|जमानत राशि जमा)'),
    re.compile(r'(?i)(?:ఆర్బీఐ.*?(?:సేఫ్|ఎస్క్రో|సెక్యూరిటీ|ఖాతా)|ప్రభుత్వ ఎస్క్రో|వెరిఫికేషన్ డిపాజిట్|రీఫండబుల్ డిపాజిట్|క్లియరెన్స్ బాండ్|క్లియరెన్స్ డిపాజిట్)')
]

# Coercion Threat Patterns
COERCION_PATTERNS = [
    re.compile(r'(?i)\b(?:arrest warrant|non-bailable warrant|nbw|asset seizure|bank account freeze|account freezing|swat deployment|police team|physical arrest|property attachment|red corner notice)\b'),
    re.compile(r'(?i)(?:गिरफ्तारी वारंट|गैर-जमानती वारंट|खाता फ्रीज|संपत्ति जब्त|घर पर दबिश|पुलिस टीम|रेड कॉर्नर)'),
    re.compile(r'(?i)(?:అరెస్ట్ వారెంట్|నాన్-బెయిలబుల్ వారెంట్|ఖాతా ఫ్రీజ్|ఆస్తుల జప్తు|పోలీసులు ఇంటికి|రెడ్ కార్నర్)')
]

# Negation / Educational Awareness Context
AWARENESS_NEGATIONS = [
    re.compile(r'(?i)\b(?:beware of digital arrest|digital arrest is a scam|police warned against|fake digital arrest|awareness on digital arrest|law enforcement never conducts|no such thing as digital arrest|cyber dost)\b'),
    re.compile(r'(?i)(?:डिजिटल अरेस्ट से सावधान|डिजिटल अरेस्ट एक धोखा|डिजिटल अरेस्ट एक नया ऑनलाइन फ्रॉड|पुलिस की चेतावनी|पुलिस कभी वीडियो कॉल पर जांच नहीं करती|साइबर दोस्त)'),
    re.compile(r'(?i)(?:డిజిటల్ అరెస్ట్ ఒక మోసం|డిజిటల్ అరెస్ట్ అనేది ఒక మోసం|పోలీసులు హెచ్చరించారు|పోలీసులు ఎప్పుడూ వీడియో కాల్ లో అరెస్ట్ చేయరు|సైబర్ సెల్ హెచ్చరిక|పోలీస్ సలహా)')
]

class DigitalArrestChecker:
    """
    Specialized Coercion Detector for Police / CBI / ED / Narcotics Video Call Extortion
    ("Digital Arrest" scams). Evaluates syntactic coercion tactics, agency spoofing,
    contraband parcel traps, and virtual confinement demands.
    """

    def evaluate(self, text: str) -> Dict[str, Any]:
        if not text or not text.strip():
            return {
                "is_digital_arrest": False,
                "confidence": 0.0,
                "severity": "NONE",
                "coercion_tactics": [],
                "tactic_count": 0,
                "legal_truth": "",
                "emergency_advice": []
            }

        clean_text = text.strip()

        # Check for educational awareness negation
        for pat in AWARENESS_NEGATIONS:
            if pat.search(clean_text):
                return {
                    "is_digital_arrest": False,
                    "confidence": 0.05,
                    "severity": "INFO",
                    "coercion_tactics": ["Educational awareness / scam warning advisory"],
                    "tactic_count": 0,
                    "legal_truth": "Legitimate cyber awareness communication advising caution.",
                    "emergency_advice": ["Maintain digital safety awareness."]
                }

        tactics = []
        score_points = 0.0

        # Tactic 1: Agency Impersonation
        has_agency = any(p.search(clean_text) for p in AGENCY_PATTERNS)
        if has_agency:
            tactics.append("Law Enforcement / Regulatory Impersonation (CBI, ED, Police, Customs, Supreme Court)")
            score_points += 30.0

        # Tactic 2: Contraband Parcel Seizure
        has_contraband = any(p.search(clean_text) for p in CONTRABAND_PATTERNS)
        if has_contraband:
            tactics.append("Fabricated Contraband / Narcotics Parcel Allegation (MDMA, passports, illegal SIMs, hawala)")
            score_points += 35.0

        # Tactic 3: Virtual Confinement ("Digital Arrest" / Video Call Demand)
        has_confinement = any(p.search(clean_text) for p in CONFINEMENT_PATTERNS)
        if has_confinement:
            tactics.append("Virtual Confinement Demand ('Digital Arrest' or mandatory Skype/WhatsApp video surveillance)")
            score_points += 40.0

        # Tactic 4: Coercion / Warrant Threats
        has_coercion = any(p.search(clean_text) for p in COERCION_PATTERNS)
        if has_coercion:
            tactics.append("High-Pressure Coercion (Arrest warrant, NBW, or asset confiscation threats)")
            score_points += 25.0

        # Tactic 5: Financial Escrow / Verification Trap
        has_financial = any(p.search(clean_text) for p in FINANCIAL_TRAP_PATTERNS)
        if has_financial:
            tactics.append("Financial Extortion / Sham 'RBI Verification' Escrow Transfer")
            score_points += 35.0

        tactic_count = len(tactics)

        # A "Digital Arrest" scam is identified if:
        # (1) Virtual confinement is explicitly mentioned OR
        # (2) Agency impersonation + (contraband OR coercion OR financial trap) OR
        # (3) Contraband + coercion OR
        # (4) Score points >= 45.0
        is_scam = (
            has_confinement or
            (has_agency and (has_contraband or has_coercion or has_financial)) or
            (has_contraband and (has_coercion or has_financial)) or
            (tactic_count >= 2 and score_points >= 45.0)
        )

        confidence = min(0.99, max(0.0, score_points / 100.0)) if is_scam else 0.0
        severity = "CRITICAL" if (score_points >= 60.0 or has_confinement) else ("HIGH" if is_scam else "NONE")

        legal_truth = (
            "⚠️ LEGAL FACT: Indian Law, the Code of Criminal Procedure (CrPC), and the Bharatiya Nagarik Suraksha Sanhita (BNSS) "
            "do NOT recognize 'Digital Arrest'. Real police officers, CBI, ED, or judges NEVER interrogate, place citizens under arrest, "
            "or demand funds via Skype, WhatsApp, or video call."
        )

        emergency_advice = [
            "1. Disconnect the call immediately. You are speaking with an extortion gang, NOT law enforcement.",
            "2. Do NOT transfer any money for 'RBI verification', 'clearance fees', or 'bail'. Government agencies have no such escrow accounts.",
            "3. Golden-Hour Recovery: Call 1930 immediately or file a report at cybercrime.gov.in.",
            "4. Inform your family or friends immediately to break psychological isolation."
        ]

        return {
            "is_digital_arrest": is_scam,
            "confidence": round(confidence, 2),
            "severity": severity,
            "coercion_tactics": tactics,
            "tactic_count": tactic_count,
            "legal_truth": legal_truth if is_scam else "",
            "emergency_advice": emergency_advice if is_scam else []
        }

digital_arrest_checker = DigitalArrestChecker()
