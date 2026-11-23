import re
from typing import List, Dict, Any, Optional
from ..models.schemas import SafetyReport

# Curated Human-Reviewed Translations for the 9 Core Procedural Topics
KB_TOPIC_TRANSLATIONS = {
    "kb_helpline_1930_golden_hour": {
        "en": {
            "title": "Reporting Cyber Fraud: National Helpline 1930 & Golden Hour Freezing",
            "summary": "To report financial fraud to the 1930 helpline within the Golden Hour, prepare your transaction details and call immediately.",
            "steps": [
                "Call 1930 immediately to connect with the National Cyber Crime Reporting Desk.",
                "Keep details ready: 12-digit transaction UTR number, debited bank name, transaction time, and scammer UPI ID or phone number.",
                "The officer logs a CFCFRMS ticket to alert the beneficiary bank and freeze funds in transit before withdrawal.",
                "Within 24 hours, visit cybercrime.gov.in to upload transaction screenshots, SMS evidence, and complete formal complaint registration."
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "Ministry of Home Affairs (MHA) — Citizen Financial Cyber Fraud Reporting System"
        },
        "hi": {
            "title": "राष्ट्रीय साइबर हेल्पलाइन 1930 पर शिकायत दर्ज करने की प्रक्रिया",
            "summary": "1930 हेल्पलाइन पर साइबर फ्रॉड की रिपोर्ट करने के लिए अपने लेन-देन के विवरण तैयार रखें और 'गोल्डन ऑवर' (पहले 2-3 घंटे) के भीतर तुरंत कॉल करें।",
            "steps": [
                "तुरंत राष्ट्रीय साइबर हेल्पलाइन 1930 पर कॉल करें।",
                "जरूरी जानकारी तैयार रखें: 12-अंकों का UTR नंबर, अपना बैंक नाम व खाता संख्या, समय, और जालसाज का UPI ID या मोबाइल नंबर।",
                "अधिकारी आपकी शिकायत दर्ज कर लाभार्थी बैंक को धोखाधड़ी की रकम रोकने (फ़्रीज़ करने) का अलर्ट भेजेंगे।",
                "24 घंटे के भीतर cybercrime.gov.in पर जाकर ट्रांजेक्शन के स्क्रीनशॉट और एसएमएस अपलोड करके औपचारिक शिकायत दर्ज करें।"
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "गृह मंत्रालय (MHA) — राष्ट्रीय साइबर हेल्पलाइन 1930"
        },
        "te": {
            "title": "జాతీయ సైబర్ హెల్ప్‌లైన్ 1930 కు ఫిర్యాదు చేసే విధానం",
            "summary": "1930 హెల్ప్‌లైన్‌కు సైబర్ మోసం గురించి ఫిర్యాదు చేయడానికి మీ లావాదేవీ వివరాలను సిద్ధం చేసుకుని గోల్డెన్ అవర్‌లో వెంటనే కాల్ చేయండి.",
            "steps": [
                "వెంటనే జాతీయ సైబర్ హెల్ప్‌లైన్ 1930 కు కాల్ చేయండి.",
                "వివరాలు సిద్ధంగా ఉంచుకోండి: 12 అంకెల UTR నంబర్, మీ బ్యాంక్ పేరు, సమయం, మరియు మోసగాడి UPI ID లేదా ఫోన్ నంబర్.",
                "అధికారి టిక్కెట్ నమోదు చేసి డబ్బు డ్రా కాకముందే లబ్ధిదారుడి ఖాతాను ఫ్రీజ్ చేయమని బ్యాంక్‌కు ఆదేశిస్తారు.",
                "24 గంటల లోపు cybercrime.gov.in లో లావాదేవీ స్క్రీన్‌షాట్లు మరియు ఎస్ఎంఎస్ ఆధారాలను అప్‌లోడ్ చేసి పూర్తి ఫిర్యాదు చేయండి."
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "హోం వ్యవహారాల మంత్రిత్వ శాఖ (MHA) — సైబర్ క్రైమ్ హెల్ప్‌లైన్ 1930"
        }
    },
    "kb_cybercrime_portal_filing": {
        "en": {
            "title": "Step-by-Step Formal Complaint Filing on Cybercrime.gov.in",
            "summary": "Filing an official complaint on the National Cyber Crime Reporting Portal generates a police acknowledgement number required for insurance and bank dispute reversals.",
            "steps": [
                "Visit the official portal at https://cybercrime.gov.in and select 'Report Crime' -> 'Financial Fraud'.",
                "Register/login with your mobile number and verify via OTP.",
                "Enter transaction details: Incident date/time, victim bank account, and 12-digit transaction UTR reference number.",
                "Enter suspect details: Scammer phone number, UPI ID, bank account, or phishing website URL.",
                "Upload evidence: Bank statement showing debit, screenshots of fraudulent chats/calls, and download your Acknowledgement PDF."
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "Indian Cyber Crime Coordination Centre (I4C), MHA"
        },
        "hi": {
            "title": "Cybercrime.gov.in पोर्टल पर औपचारिक शिकायत दर्ज करने के चरण",
            "summary": "राष्ट्रीय साइबर क्राइम रिपोर्टिंग पोर्टल पर औपचारिक शिकायत दर्ज करने से आपको एक पावती (Acknowledgement) संख्या मिलती है जो बैंक रिफंड के लिए अनिवार्य है।",
            "steps": [
                "आधिकारिक पोर्टल https://cybercrime.gov.in पर जाएं और 'Report Financial Fraud' चुनें।",
                "अपने मोबाइल नंबर और ओटीपी के माध्यम से लॉगिन करें।",
                "घटना का विवरण दर्ज करें: तारीख, समय, आपका बैंक खाता और 12-अंकों का UTR नंबर।",
                "संदिग्ध का विवरण भरें: जालसाज का फोन नंबर, UPI ID, बैंक खाता या फर्जी वेबसाइट लिंक।",
                "साक्ष्य अपलोड करें: बैंक स्टेटमेंट, मैसेज के स्क्रीनशॉट, और अपनी पावती रसीद (Acknowledgement PDF) सुरक्षित रखें।"
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "भारतीय साइबर अपराध समन्वय केंद्र (I4C), गृह मंत्रालय"
        },
        "te": {
            "title": "Cybercrime.gov.in పోర్టల్‌లో అధికారిక ఫిర్యాదు నమోదు చేసే విధానం",
            "summary": "జాతీయ సైబర్ క్రైమ్ పోర్టల్‌లో అధికారిక ఫిర్యాదు నమోదు చేయడం ద్వారా లభించే రశీదు నంబర్ బ్యాంక్ వివాద పరిష్కారానికి తప్పనిసరి.",
            "steps": [
                "https://cybercrime.gov.in అధికారిక పోర్టల్‌ను సందర్శించి 'Report Financial Fraud' ఎంచుకోండి.",
                "మీ మొబైల్ నంబర్ మరియు ఓటీపీ ద్వారా లాగిన్ అవ్వండి.",
                "లావాదేవీ వివరాలు నమోదు చేయండి: సంఘటన తేదీ, సమయం, మీ బ్యాంక్ ఖాతా మరియు 12 అంకెల UTR నంబర్.",
                "మోసగాడి వివరాలు ఇవ్వండి: ఫోన్ నంబర్, UPI ID, బ్యాంక్ ఖాతా లేదా ఫేక్ వెబ్‌సైట్ లింక్.",
                "సాక్ష్యాధారాలు అప్‌లోడ్ చేయండి: బ్యాంక్ స్టేట్‌మెంట్, స్క్రీన్‌షాట్లు మరియు రశీదు పీడీఎఫ్‌ను భద్రపరుచుకోండి."
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "ఇండియన్ సైబర్ క్రైమ్ కోఆర్డినేషన్ సెంటర్ (I4C)"
        }
    },
    "kb_money_lost_emergency_protocol": {
        "en": {
            "title": "Golden Hour Protocol: What to Do Immediately When Money is Lost",
            "summary": "If money was wrongfully debited from your account, act within the first 1-2 hours to stop the funds before cash withdrawal.",
            "steps": [
                "Call your bank's 24x7 emergency fraud desk immediately to report unauthorized debit and freeze your account/cards.",
                "Dial 1930 (National Cyber Crime Helpline) within the Golden Hour to freeze funds across beneficiary accounts.",
                "Block your UPI ID and netbanking access through your mobile banking app or bank customer support.",
                "Preserve all evidence: Do not delete SMS, WhatsApp messages, or receipts; take full screenshots.",
                "Lodge an official report on https://cybercrime.gov.in and share the acknowledgement number with your bank."
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "Reserve Bank of India (RBI) & I4C MHA Advisory"
        },
        "hi": {
            "title": "गोल्डन ऑवर प्रोटोकॉल: खाते से पैसे कट जाने पर तुरंत क्या करें",
            "summary": "यदि आपके खाते से धोखाधड़ी में पैसे कट गए हैं, तो पहले 1-2 घंटों में तुरंत यह कदम उठाएं ताकि पैसा ट्रांसफर होने से रुक सके।",
            "steps": [
                "तुरंत अपने बैंक के 24x7 इमरजेंसी फ्रॉड नंबर पर कॉल करें और खाता/कार्ड तुरंत ब्लॉक करवाएं।",
                "गोल्डन ऑवर में तुरंत राष्ट्रीय साइबर हेल्पलाइन 1930 पर कॉल करें ताकि पैसा आगे ट्रांसफर न हो सके।",
                "अपने मोबाइल बैंकिंग ऐप से UPI ID और नेटबैंकिंग को तुरंत डिएक्टिवेट करें।",
                "सभी साक्ष्य संभाल कर रखें: एसएमएस, व्हाट्सएप चैट और पेमेंट रसीद के स्क्रीनशॉट लें।",
                "https://cybercrime.gov.in पर आधिकारिक शिकायत दर्ज करके पावती संख्या अपने बैंक को दें।"
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "भारतीय रिज़र्व बैंक (RBI) एवं गृह मंत्रालय एडवाइजरी"
        },
        "te": {
            "title": "గోల్డెన్ అవర్ ప్రోటోకాల్: ఖాతా నుండి డబ్బు పోయినప్పుడు వెంటనే ఏం చేయాలి",
            "summary": "ఖాతా నుండి డబ్బు మోసపూరితంగా కట్ అయితే, మొదటి 1-2 గంటల్లో తక్షణమే ఈ చర్యలు తీసుకోండి.",
            "steps": [
                "వెంటనే మీ బ్యాంక్ 24x7 ఎమర్జెన్సీ నంబర్‌కు కాల్ చేసి ఖాతా/కార్డులను ఫ్రీజ్ చేయించండి.",
                "డబ్బులు ఇతర ఖాతాల్లోకి వెళ్లకుండా ఆపడానికి తక్షణమే 1930 కు కాల్ చేయండి.",
                "మీ మొబైల్ బ్యాంకింగ్ యాప్ ద్వారా UPI ID మరియు నెట్‌బ్యాంకింగ్‌ను నిలిపివేయండి.",
                "సాక్ష్యాధారాలన్నీ భద్రపరచండి: మెసేజ్‌లు, వాట్సాప్ చాట్లు మరియు రశీదుల స్క్రీన్‌షాట్లు తీసుకోండి.",
                "https://cybercrime.gov.in లో అధికారిక ఫిర్యాదు నమోదు చేసి ఆ రశీదును మీ బ్యాంక్‌కు సమర్పించండి."
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "రిజర్వ్ బ్యాంక్ ఆఫ్ ఇండియా (RBI) & I4C మార్గదర్శకాలు"
        }
    },
    "kb_shared_otp_pin_emergency": {
        "en": {
            "title": "Emergency Steps if You Shared an OTP, UPI PIN, or Password",
            "summary": "If you mistakenly disclosed your OTP, UPI PIN, or banking passwords, secure your accounts immediately.",
            "steps": [
                "Open your UPI app immediately (Google Pay / PhonePe / Paytm / BHIM) -> Bank Accounts -> Reset / Change UPI PIN.",
                "Call your bank customer care immediately to temporarily lock Internet Banking credentials and hotlist debit/credit cards.",
                "Check your bank account statement right now for any unfamiliar deductions.",
                "If money was deducted, dial 1930 immediately and notify the bank within 3 days for RBI Zero-Liability protection."
            ],
            "official_url": "https://www.rbi.org.in",
            "source": "Reserve Bank of India (RBI) Cybersecurity Directives"
        },
        "hi": {
            "title": "अगर किसी को OTP या UPI PIN बता दिया तो तुरंत क्या करें",
            "summary": "यदि आपने गलती से अपना ओटीपी, यूपीआई पिन या पासवर्ड किसी को बता दिया है, तो तुरंत अपने खाते सुरक्षित करें।",
            "steps": [
                "तुरंत अपने यूपीआई ऐप (GPay / PhonePe / Paytm / BHIM) में जाएं और Bank Account में जाकर UPI PIN बदलें।",
                "तुरंत अपने बैंक कस्टमर केयर को कॉल करके नेटबैंकिंग और डेबिट कार्ड ब्लॉक करवाएं।",
                "अपने बैंक स्टेटमेंट में चेक करें कि कोई अनधिकृत लेन-देन तो नहीं हुआ।",
                "यदि पैसे कट चुके हैं, तो तुरंत 1930 पर कॉल करें और 3 दिन के भीतर बैंक को लिखित सूचना दें।"
            ],
            "official_url": "https://www.rbi.org.in",
            "source": "भारतीय रिज़र्व बैंक (RBI) सुरक्षा निर्देश"
        },
        "te": {
            "title": "ఎవరికైనా ఓటీపీ లేదా యూపీఐ పిన్ చెబితే వెంటనే ఏం చేయాలి",
            "summary": "పొరపాటున మీ ఓటీపీ లేదా యూపీఐ పిన్ ఎవరికైనా చెబితే, ఖాతాలను సురక్షితం చేయడానికి వెంటనే ఈ పనులు చేయండి.",
            "steps": [
                "వెంటనే మీ యూపీఐ యాప్ (GPay / PhonePe / Paytm) ఓపెన్ చేసి యూపీఐ పిన్ (UPI PIN) మార్చండి.",
                "మీ బ్యాంక్ కస్టమర్ కేర్‌కు కాల్ చేసి నెట్‌బ్యాంకింగ్ మరియు కార్డులను తాత్కాలికంగా బ్లాక్ చేయించండి.",
                "మీ బ్యాంక్ ఖాతా స్టేట్‌మెంట్‌లో ఏదైనా అనధికారిక లావాదేవీ జరిగిందో లేదో చూడండి.",
                "డబ్బులు కట్ అయితే, వెంటనే 1930 కు కాల్ చేసి 3 రోజుల్లోపు బ్యాంక్‌కు సమాచారం ఇవ్వండి."
            ],
            "official_url": "https://www.rbi.org.in",
            "source": "రిజర్వ్ బ్యాంక్ ఆఫ్ ఇండియా (RBI) సైబర్ సెక్యూరిటీ డైరెక్టివ్స్"
        }
    },
    "kb_remote_access_scam_playbook": {
        "en": {
            "title": "Remote Desktop Screen Sharing Fraud: What to Do if an App Was Installed",
            "summary": "Remote desktop apps (AnyDesk, TeamViewer, RustDesk) grant attackers visual control of your screen to steal OTPs. Disconnect and uninstall immediately.",
            "steps": [
                "Disconnect Internet immediately: Turn on Airplane Mode or turn off Wi-Fi and Mobile Data.",
                "Uninstall the remote application (AnyDesk, TeamViewer, RustDesk) from your phone settings immediately.",
                "Reset your netbanking and email passwords using a different, clean phone or computer.",
                "Call your bank's fraud desk to check for unauthorized debits and temporarily block netbanking.",
                "Run a malware scan using Google Play Protect before re-enabling internet."
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "Cyber Crime Investigation Cell & RBI Social Engineering Advisory"
        },
        "hi": {
            "title": "AnyDesk या TeamViewer ऐप डाउनलोड हो जाने पर क्या करें",
            "summary": "रिमोट ऐप (AnyDesk, TeamViewer) के जरिए धोखेबाज आपकी स्क्रीन देखकर ओटीपी चुरा लेते हैं। तुरंत इंटरनेट बंद करें और ऐप हटाएं।",
            "steps": [
                "तुरंत इंटरनेट बंद करें: अपने फोन में एयरप्लेन मोड (Airplane Mode) ऑन करें या वाई-फाई/डेटा बंद करें।",
                "फोन सेटिंग्स में जाकर AnyDesk, TeamViewer या QuickSupport ऐप को तुरंत अनइंस्टॉल (डिलीट) करें।",
                "किसी दूसरे सुरक्षित फोन या कंप्यूटर से अपने बैंक, यूपीआई और ईमेल के पासवर्ड बदलें।",
                "अपने बैंक के फ्रॉड हेल्पडेस्क पर कॉल करके नेटबैंकिंग ब्लॉक करवाएं और खाते की जांच करें।",
                "इंटरनेट चालू करने से पहले Google Play Protect से मोबाइल को स्कैन करें।"
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "साइबर क्राइम सेल एवं भारतीय रिज़र्व बैंक एडवाइजरी"
        },
        "te": {
            "title": "AnyDesk లేదా TeamViewer యాప్ ఇన్‌స్టాల్ చేసుకుంటే వెంటనే ఏం చేయాలి",
            "summary": "రిమోట్ యాప్స్ ద్వారా మోసగాళ్ళు మీ స్క్రీన్‌ను చూస్తూ ఓటీపీలు దొంగిలిస్తారు. వెంటనే ఇంటర్నెట్ ఆపి యాప్‌ను తొలగించండి.",
            "steps": [
                "వెంటనే ఇంటర్నెట్ నిలిపివేయండి: ఫోన్‌లో ఏరోప్లేన్ మోడ్ (Airplane Mode) ఆన్ చేయండి.",
                "ఫోన్ సెట్టింగ్స్‌లోకి వెళ్లి AnyDesk, TeamViewer లేదా QuickSupport యాప్‌ను వెంటనే అన్‌ఇన్‌స్టాల్ చేయండి.",
                "వేరే సురక్షిత ఫోన్ ద్వారా మీ నెట్‌బ్యాంకింగ్ మరియు ఈమెయిల్ పాస్‌వర్డ్‌లను మార్చండి.",
                "బ్యాంక్ కస్టమర్ కేర్‌కు కాల్ చేసి నెట్‌బ్యాంకింగ్ బ్లాక్ చేయించి ఖాతాను చెక్ చేయండి.",
                "ఇంటర్నెట్ ఆన్ చేసే ముందు Google Play Protect తో ఫోన్‌ను స్కాన్ చేయండి."
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "సైబర్ క్రైమ్ ఇన్వెస్టిగేషన్ సెల్ & RBI మార్గదర్శకాలు"
        }
    },
    "kb_how_to_block_upi_id": {
        "en": {
            "title": "How to Block, Disable, or De-link a UPI ID",
            "summary": "You can block or delete a compromised UPI handle directly in your UPI app or request your bank to disable UPI services.",
            "steps": [
                "In your UPI app: Go to Profile -> Bank Account / Payment Settings -> Select UPI ID -> Delete or Disable.",
                "Call your bank customer care: Request the executive to immediately disable UPI / IMPS services on your account.",
                "Use Bank NetBanking / SMS: Access netbanking security settings to disable UPI / E-Commerce, or send bank-specific emergency SMS (e.g. BLOCK UPI).",
                "De-register: Remove your bank account from Google Pay, PhonePe, and Paytm until your security check is complete."
            ],
            "official_url": "https://www.npci.org.in",
            "source": "National Payments Corporation of India (NPCI) & IBA"
        },
        "hi": {
            "title": "UPI ID को ब्लॉक, डिलीट या डिएक्टिवेट कैसे करें",
            "summary": "आप अपने यूपीआई ऐप से सीधे यूपीआई आईडी हटा सकते हैं या अपने बैंक से यूपीआई सेवा बंद करने का अनुरोध कर सकते हैं।",
            "steps": [
                "अपने यूपीआई ऐप में: Profile -> Bank Account -> UPI IDs में जाएं और संबंधित आईडी को Delete या Remove करें।",
                "बैंक कस्टमर केयर को कॉल करें: अपने बैंक को कॉल करके कहें कि 'मेरे खाते पर UPI/IMPS सेवाएं तुरंत बंद करें'।",
                "नेटबैंकिंग या एसएमएस: बैंक के नेटबैंकिंग सिक्योरिटी सेटिंग्स से UPI ब्लॉक करें या बैंक के नंबर पर 'BLOCK UPI' एसएमएस भेजें।",
                "खाता हटाएं: सुरक्षा जांच पूरी होने तक पेमेंट ऐप्स (GPay, PhonePe, Paytm) से अपना बैंक खाता डी-लिंक (Remove) कर दें।"
            ],
            "official_url": "https://www.npci.org.in",
            "source": "भारतीय राष्ट्रीय भुगतान निगम (NPCI)"
        },
        "te": {
            "title": "యూపీఐ ఐడీని బ్లాక్ చేయడం లేదా డిలీట్ చేయడం ఎలా",
            "summary": "మీరు నేరుగా యూపీఐ యాప్‌లో మీ ఐడీని తొలగించవచ్చు లేదా బ్యాంక్ ద్వారా యూపీఐ సేవలను నిలిపివేయవచ్చు.",
            "steps": [
                "మీ యూపీఐ యాప్‌లో: Profile -> Bank Account -> Manage UPI IDs లోకి వెళ్లి Delete లేదా Remove ఎంచుకోండి.",
                "బ్యాంక్ కస్టమర్ కేర్‌కు కాల్ చేయండి: మీ ఖాతాపై UPI సేవలను తాత్కాలికంగా బ్లాక్ చేయమని కోరండి.",
                "నెట్‌బ్యాంకింగ్ లేదా ఎస్ఎంఎస్: నెట్‌బ్యాంకింగ్ సెక్యూరిటీ సెట్టింగ్స్ ద్వారా UPI నిలిపివేయండి లేదా బ్యాంక్ సూచించిన ఫార్మాట్‌లో ఎస్ఎంఎస్ పంపండి.",
                "ఖాతాను డీలింక్ చేయండి: భద్రతా పరిశీలన పూర్తయ్యే వరకు పేమెంట్ యాప్‌ల నుండి బ్యాంక్ ఖాతాను తొలగించండి."
            ],
            "official_url": "https://www.npci.org.in",
            "source": "నేషనల్ పేమెంట్స్ కార్పొరేషన్ ఆఫ్ ఇండియా (NPCI)"
        }
    },
    "kb_upi_collect_request_rules": {
        "en": {
            "title": "UPI Collect Requests: How They Work & Why Receiving Money Never Needs a PIN",
            "summary": "A collect request is a pull transaction that debits money from your account. Receiving money never requires entering a UPI PIN.",
            "steps": [
                "The Golden Rule: You NEVER need to enter your 4 or 6-digit UPI PIN to receive money, refunds, or cashback.",
                "Check the prompt: If a screen asks for your UPI PIN, money will be DEDUCTED from your account, NOT added.",
                "Decline unknown requests: Reject all collect requests from unverified individuals or marketplace buyers.",
                "Report fraudulent handles: Tap 'Report Scam / Spam' inside your UPI app to block the attacker's VPA with NPCI."
            ],
            "official_url": "https://www.npci.org.in/what-we-do/upi/security",
            "source": "NPCI Security Circular on Collect Requests & Limits"
        },
        "hi": {
            "title": "UPI कलेक्ट रिक्वेस्ट कैसे काम करता है: पैसे लेने के लिए पिन क्यों नहीं लगता",
            "summary": "कलेक्ट रिक्वेस्ट आपके खाते से पैसे काटने (Debit) की मांग होती है। पैसे प्राप्त करने के लिए कभी भी यूपीआई पिन दर्ज नहीं करना पड़ता।",
            "steps": [
                "गोल्डन नियम: पैसे, रिफंड या कैशबैक प्राप्त करने के लिए कभी भी 4 या 6 अंकों का UPI PIN डालने की जरूरत नहीं होती।",
                "स्क्रीन चेक करें: अगर स्क्रीन पर पिन डालने को कहा जा रहा है, तो आपके खाते से पैसे कटेंगे, आएंगे नहीं।",
                "कलेक्ट रिक्वेस्ट अस्वीकार करें: किसी भी अनजान व्यक्ति द्वारा भेजी गई कलेक्ट रिक्वेस्ट को Decline या Reject करें।",
                "रिपोर्ट करें: ऐप में 'Report as Scam' विकल्प चुनकर जालसाज के UPI ID की शिकायत NPCI से करें।"
            ],
            "official_url": "https://www.npci.org.in/what-we-do/upi/security",
            "source": "एनपीसीआई (NPCI) यूपीआई सुरक्षा नियम"
        },
        "te": {
            "title": "యూపీఐ కలెక్ట్ రిక్వెస్ట్ ఎలా పనిచేస్తుంది: డబ్బులు తీసుకోవడానికి పిన్ ఎందుకు అవసరం లేదు",
            "summary": "కలెక్ట్ రిక్వెస్ట్ అనేది మీ ఖాతా నుండి డబ్బులను డెబిట్ చేయడానికి పంపే అభ్యర్థన. డబ్బులు పొందడానికి పిన్ ఎప్పుడూ అవసరం లేదు.",
            "steps": [
                "బంగారు నియమం: డబ్బులు, రీఫండ్ లేదా క్యాష్‌బ్యాక్ పొందడానికి ఎప్పుడూ యూపీఐ పిన్ (UPI PIN) నమోదు చేయాల్సిన అవసరం లేదు.",
                "స్క్రీన్‌ను గమనించండి: పిన్ అడుగుతుంటే మీ ఖాతా నుండి డబ్బులు కట్ అవుతాయని అర్థం, జమ కావు.",
                "రిక్వెస్ట్‌ను తిరస్కరించండి: తెలియని వ్యక్తుల నుండి వచ్చే కలెక్ట్ రిక్వెస్ట్‌లను Decline చేయండి.",
                "రిపోర్ట్ చేయండి: యాప్‌లోనే 'Report as Scam' ఎంచుకుని ఆ యూపీఐ ఐడీపై ఫిర్యాదు చేయండి."
            ],
            "official_url": "https://www.npci.org.in/what-we-do/upi/security",
            "source": "ఎన్‌పీసీఐ (NPCI) భద్రతా మార్గదర్శకాలు"
        }
    },
    "kb_digital_arrest_customs_scam": {
        "en": {
            "title": "Digital Arrest & Fake Police Video Calls: Statutory Legal Facts",
            "summary": "Under Indian Law (CrPC and BNSS Section 35), 'Digital Arrest' is completely non-existent. Real police never arrest citizens over video calls.",
            "steps": [
                "Recognize the statutory fact: Indian Law does NOT recognize any concept of 'Digital Arrest'. Video call arrests are 100% fraudulent.",
                "Real police rules: Real police, CBI, ED, or Customs NEVER interrogate citizens or demand bail via Skype or WhatsApp video.",
                "No 'Safe Accounts': Real agencies never ask citizens to transfer money to 'RBI verification accounts' or 'clearing accounts'.",
                "Immediate Action: Disconnect the call immediately, block the caller, and report to 1930 and cybercrime.gov.in."
            ],
            "official_url": "https://mha.gov.in",
            "source": "Ministry of Home Affairs, CBI & Delhi Police Advisory"
        },
        "hi": {
            "title": "डिजिटल अरेस्ट और फर्जी पुलिस वीडियो कॉल का कानूनी सच",
            "summary": "भारतीय कानून (CrPC / BNSS धारा 35) में 'डिजिटल अरेस्ट' का कोई प्रावधान नहीं है। असली पुलिस कभी वीडियो कॉल पर गिरफ्तारी नहीं करती।",
            "steps": [
                "कानूनी सच जानें: भारतीय कानून में 'डिजिटल अरेस्ट' नाम की कोई चीज नहीं होती। यह पूरी तरह से जालसाजी है।",
                "पुलिस के नियम: असली पुलिस, सीबीआई, नारकोटिक्स या जज कभी भी व्हाट्सएप या स्काइप वीडियो कॉल पर पूछताछ या गिरफ्तारी नहीं करते।",
                "कोई सत्यापन खाता नहीं: कोई भी सरकारी एजेंसी 'आरबीआई वेरिफिकेशन अकाउंट' में पैसे ट्रांसफर करने की मांग नहीं करती।",
                "तुरंत यह करें: वीडियो कॉल तुरंत काटें, नंबर ब्लॉक करें और राष्ट्रीय साइबर हेल्पलाइन 1930 पर शिकायत दर्ज करें।"
            ],
            "official_url": "https://mha.gov.in",
            "source": "गृह मंत्रालय (MHA) एवं केंद्रीय जांच ब्यूरो (CBI) परामर्श"
        },
        "te": {
            "title": "డిజిటల్ అరెస్ట్ మరియు ఫేక్ పోలీస్ వీడియో కాల్స్ చట్టపరమైన నిజం",
            "summary": "భారతీయ చట్టం (CrPC / BNSS సెక్షన్ 35) ప్రకారం 'డిజిటల్ అరెస్ట్' అనేది లేదు. నిజమైన పోలీసులు ఎప్పుడూ వీడియో కాల్స్‌లో అరెస్టులు చేయరు.",
            "steps": [
                "చట్టపరమైన వాస్తవం: భారతీయ చట్టంలో 'డిజిటల్ అరెస్ట్' అనే పద్ధతి లేదు. ఇది 100% మోసపూరితమైన బెదిరింపు.",
                "పోలీస్ నిబంధనలు: నిజమైన పోలీసులు, సీబీఐ లేదా కస్టమ్స్ అధికారులు వాట్సాప్ లేదా స్కైప్ వీడియో కాల్ ద్వారా విచారణ లేదా అరెస్టు చేయరు.",
                "ఖాతాలోకి డబ్బు బదిలీ ఉండదు: ఏ ప్రభుత్వ సంస్థ కూడా 'ఆర్బీఐ వెరిఫికేషన్ అకౌంట్' కు డబ్బులు పంపమని అడగదు.",
                "వెంటనే చేయాల్సిన పని: కాల్ వెంటనే కట్ చేసి, నంబర్‌ను బ్లాక్ చేసి 1930 హెల్ప్‌లైన్‌కు రిపోర్ట్ చేయండి."
            ],
            "official_url": "https://mha.gov.in",
            "source": "హోం వ్యవహారాల మంత్రిత్వ శాఖ (MHA) & CBI హెచ్చరిక"
        }
    },
    "kb_verify_bank_upi_message": {
        "en": {
            "title": "How to Verify if a Bank or UPI Message is Genuine or Fake",
            "summary": "Check the 6-character TRAI DLT SMS header, verify the official domain name, and never call phone numbers sent inside an SMS.",
            "steps": [
                "Check Sender ID: Authentic bank SMS uses 6-character TRAI DLT alphanumeric headers (e.g. AD-SBIINB, VK-HDFCBK). Standard 10-digit mobile numbers are NOT banks.",
                "Check Website Links: Genuine banks operate only on official domains (sbi.co.in, hdfcbank.com). Avoid .xyz, .top, .live, .cc, or raw IP addresses.",
                "Never call numbers in SMS: Call your bank only using the verified phone number printed on the back of your physical debit card.",
                "Verify in App: Log in to your bank's official mobile application directly to inspect whether any account alert actually exists."
            ],
            "official_url": "https://trai.gov.in",
            "source": "Telecom Regulatory Authority of India (TRAI) & RBI Financial Education"
        },
        "hi": {
            "title": "बैंक या यूपीआई संदेश असली है या फर्जी, इसकी पहचान कैसे करें",
            "summary": "एसएमएस का 6-अक्षरों वाला DLT हेडर चेक करें, आधिकारिक वेबसाइट डोमेन देखें, और कभी भी एसएमएस में दिए नंबर पर कॉल न करें।",
            "steps": [
                "हेडर चेक करें: असली बैंक एसएमएस में 6-अक्षरों का कोड होता है (जैसे AD-SBIINB, VK-HDFCBK)। 10-अंकों वाले मोबाइल नंबर से आने वाले मैसेज बैंक के नहीं होते।",
                "वेबसाइट लिंक देखें: असली बैंक हमेशा आधिकारिक डोमेन (जैसे sbi.co.in, hdfcbank.com) का उपयोग करते हैं। .xyz, .top, .cc वाले लिंक फर्जी होते हैं।",
                "एसएमएस के नंबर पर कॉल न करें: अपने डेबिट कार्ड के पीछे छपे आधिकारिक कस्टमर केयर नंबर पर ही कॉल करें।",
                "ऐप में चेक करें: सीधे अपने बैंक के आधिकारिक मोबाइल ऐप में लॉगिन करके देखें कि क्या वाकई कोई अलर्ट है।"
            ],
            "official_url": "https://trai.gov.in",
            "source": "भारतीय दूरसंचार विनियामक प्राधिकरण (TRAI) एवं RBI"
        },
        "te": {
            "title": "బ్యాంక్ లేదా యూపీఐ మెసేజ్ అసలైనదో కాదో ఎలా గుర్తించాలి",
            "summary": "ఎస్ఎంఎస్ యొక్క 6 అక్షరాల DLT హెడర్‌ను తనిఖీ చేయండి, అధికారిక డొమైన్‌ను చూడండి మరియు మెసేజ్‌లోని ఫోన్ నంబర్లకు కాల్ చేయవద్దు.",
            "steps": [
                "హెడర్ పరిశీలించండి: అసలైన బ్యాంక్ ఎస్ఎంఎస్‌కు 6 అక్షరాల కోడ్ ఉంటుంది (ఉదా. AD-SBIINB, VK-HDFCBK). 10 అంకెల మొబైల్ నంబర్ల నుండి బ్యాంక్ మెసేజ్‌లు రావు.",
                "లింక్ చూడండి: నిజమైన బ్యాంకులు ఎప్పుడూ అధికారిక వెబ్‌సైట్లను మాత్రమే ఉపయోగిస్తాయి (sbi.co.in). .xyz, .top వంటివి నకిలీ లింక్‌లు.",
                "మెసేజ్‌లోని నంబర్లకు కాల్ చేయవద్దు: మీ ఏటీఎం కార్డు వెనుక ఉండే అధికారిక కస్టమర్ కేర్ నంబర్‌కు మాత్రమే కాల్ చేయండి.",
                "యాప్‌లో చూడండి: నేరుగా అధికారిక మొబైల్ బ్యాంకింగ్ యాప్‌లోకి లాగిన్ అయ్యి ఎలాంటి హెచ్చరిక ఉందో చూసుకోండి."
            ],
            "official_url": "https://trai.gov.in",
            "source": "టెలికాం రెగ్యులేటరీ అథారిటీ ఆఫ్ ఇండియా (TRAI) & RBI"
        }
    },
    "kb_fake_debit_alert_callback": {
        "en": {
            "title": "Fake Debit Alert & Callback Scam: How to Identify & Protect Yourself",
            "summary": "Never call the phone number or message the WhatsApp contact in an unsolicited debit alert. Verify balances only in your bank's official app.",
            "steps": [
                "Verify independently: Open your bank's official mobile application or check NetBanking directly to verify your true balance.",
                "Do NOT dial the SMS number: Scammers pose as bank fraud executives to convince you to install remote screen-sharing apps or share OTPs.",
                "Check for genuine markers: Real bank alerts contain masked account numbers (A/C **1234), valid transaction reference IDs (UTR/RRN), and merchant names.",
                "Call verified helplines: Only call the toll-free number printed on the back of your physical card or listed on your bank's official website."
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "RBI Customer Protection Framework & I4C Cyber Threat Advisory"
        },
        "hi": {
            "title": "फर्जी डेबिट अलर्ट कॉल-बैक फ्रॉड: पहचान और बचाव के उपाय",
            "summary": "खाते से पैसे कटने के किसी भी संदिग्ध एसएमएस में दिए गए नंबर पर कभी कॉल न करें। केवल आधिकारिक बैंक ऐप में बैलेंस जांचें।",
            "steps": [
                "सीधे ऐप में जांचें: अपने बैंक के आधिकारिक मोबाइल ऐप या नेटबैंकिंग में लॉगिन करके अपना सही खाता बैलेंस और स्टेटमेंट देखें।",
                "एसएमएस में दिए नंबर पर कॉल न करें: जालसाज बैंक अधिकारी बनकर रिमोट ऐप (AnyDesk) डाउनलोड करने या ओटीपी मांगने का प्रयास करते हैं।",
                "असली बैंक संदेश के संकेत पहचानें: असली बैंक अलर्ट में खाते के अंतिम 4 अंक (**1234), ट्रांजेक्शन रेफरेंस आईडी (UTR) और शेष बैलेंस होता है।",
                "कार्ड के पीछे दिए नंबर पर संपर्क करें: सहायता के लिए केवल अपने डेबिट कार्ड के पीछे छपे बैंक के आधिकारिक टोल-फ्री नंबर पर कॉल करें।"
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "भारतीय रिजर्व बैंक (RBI) ग्राहक सुरक्षा ढांचा एवं I4C"
        },
        "te": {
            "title": "నకిలీ డెబిట్ అలర్ట్ మరియు కాల్-బ్యాక్ మోసం: ఎలా గుర్తించాలి మరియు రక్షణ చర్యలు",
            "summary": "డెబిట్ సందేశంలోని ఫోన్ నంబర్‌కు ఎప్పుడూ కాల్ చేయవద్దు. మీ అధికారిక బ్యాంక్ యాప్‌లో మాత్రమే ఖాతా బ్యాలెన్స్ తనిఖీ చేయండి.",
            "steps": [
                "యాప్‌లో తనిఖీ చేయండి: మీ అధికారిక మొబైల్ బ్యాంకింగ్ యాప్ లేదా నెట్‌బ్యాంకింగ్‌లోకి లాగిన్ అయ్యి మీ ఖచ్చితమైన బ్యాలెన్స్ చూడండి.",
                "మెసేజ్‌లోని నంబర్‌కు కాల్ చేయవద్దు: మోసగాళ్లు బ్యాంక్ అధికారులుగా నటిస్తూ స్క్రీన్ షేరింగ్ యాప్‌లు ఇన్‌స్టాల్ చేయమని లేదా ఓటీపీలు అడుగుతారు.",
                "అసలైన అలర్ట్ లక్షణాలు: అసలైన బ్యాంక్ అలర్ట్‌లో ఖాతా చివరి 4 అంకెలు (**1234), లావాదేవీ రిఫరెన్స్ నంబర్ (UTR) మరియు నిల్వ ఉంటాయి.",
                "కార్డు వెనుక ఉన్న నంబర్‌ను సంప్రదించండి: మీ ఏటీఎం లేదా డెబిట్ కార్డు వెనుక ముద్రించిన అధికారిక టోల్-ఫ్రీ నంబర్‌కు మాత్రమే కాల్ చేయండి."
            ],
            "official_url": "https://cybercrime.gov.in",
            "source": "రిజర్వ్ బ్యాంక్ ఆఫ్ ఇండియా (RBI) మరియు I4C సైబర్ హెచ్చరిక"
        }
    }
}


def format_how_to_response(chunk: Dict[str, Any], lang: str = "en") -> str:
    """
    Formats a clean, markdown-friendly help answer from the knowledge base.
    No raw ### or #### artifacts; short answer first, then steps, then official source link.
    """
    chunk_id = chunk.get("id", "")
    target_lang = lang if lang in ["hi", "te"] else "en"

    # Check if curated translation exists for this core topic
    if chunk_id in KB_TOPIC_TRANSLATIONS and target_lang in KB_TOPIC_TRANSLATIONS[chunk_id]:
        entry = KB_TOPIC_TRANSLATIONS[chunk_id][target_lang]
        title = entry["title"]
        summary = entry["summary"]
        steps = entry["steps"]
        official_url = entry["official_url"]
        source = entry["source"]
    else:
        # Fallback to general chunk attributes
        title = chunk.get("title", "Safety Guidance")
        summary = chunk.get("actionable_guidance") or chunk.get("content", "")[:200]
        steps = chunk.get("steps") or [chunk.get("actionable_guidance", "Follow safety guidelines.")]
        official_url = chunk.get("official_url", "https://cybercrime.gov.in")
        source = chunk.get("source", "Official Cyber Safety Guidelines")

    steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])

    if target_lang == "hi":
        verify_label = "आधिकारिक पोर्टल पर पुष्टि करें"
        steps_heading = "ज़रूरी कदम (Step-by-Step)"
    elif target_lang == "te":
        verify_label = "అధికారిక పోర్టల్‌లో ధృవీకరించండి"
        steps_heading = "తీసుకోవాల్సిన చర్యలు (దశల వారీగా)"
    else:
        verify_label = "Verify on the official site"
        steps_heading = "Recommended Action Steps"

    return f"""**{title}**

{summary}

**{steps_heading}:**
{steps_text}

🔗 **{verify_label}:** [{source}]({official_url})"""


def format_emergency_response(lang: str = "en") -> str:
    """
    Formats the immediate Golden Hour emergency action protocol.
    No scam score, direct critical steps with 1930 guidance.
    """
    target_lang = lang if lang in ["hi", "te"] else "en"

    if target_lang == "hi":
        return """**🚨 आपातकालीन सुरक्षा प्रोटोकॉल (Golden Hour Action)**

यदि आपके खाते से पैसे कट चुके हैं या साइबर फ्रॉड हुआ है, तो बिना देर किए तुरंत ये 4 कदम उठाएं:

1. **तुरंत बैंक को कॉल करें**: अपने बैंक के 24x7 इमरजेंसी फ्रॉड हेल्पडेस्क पर कॉल करके खाता, UPI और कार्ड तुरंत फ्रीज (ब्लॉक) करवाएं।
2. **1930 पर कॉल करें**: 'गोल्डन ऑवर' (पहले 2-3 घंटे) के भीतर राष्ट्रीय साइबर हेल्पलाइन **1930** पर कॉल करें ताकि पैसा लाभार्थी बैंक में रोका जा सके।
3. **ओटीपी / रिमोट ऐप सुरक्षा**: यदि AnyDesk डाला था तो तुरंत इंटरनेट बंद कर ऐप अनइंस्टॉल करें। यदि पिन साझा किया तो तुरंत UPI PIN बदलें।
4. **सबूत सुरक्षित रखें**: एसएमएस, कॉल रिकॉर्ड और ट्रांजेक्शन UTR नंबर के स्क्रीनशॉट लें और [cybercrime.gov.in](https://cybercrime.gov.in) पर औपचारिक शिकायत दर्ज करें।

🔗 **आधिकारिक पोर्टल पर पुष्टि करें:** [राष्ट्रीय साइबर अपराध रिपोर्टिंग पोर्टल (I4C, गृह मंत्रालय)](https://cybercrime.gov.in)"""

    elif target_lang == "te":
        return """**🚨 తక్షణ అత్యవసర భద్రతా ప్రోటోకాల్ (Golden Hour Action)**

మీ బ్యాంక్ ఖాతా నుండి డబ్బు పోయినా లేదా మోసం జరిగినా, వెంటనే ఈ 4 అత్యవసర చర్యలు తీసుకోండి:

1. **బ్యాంక్‌కు వెంటనే కాల్ చేయండి**: మీ బ్యాంక్ 24x7 ఎమర్జెన్సీ నంబర్‌కు కాల్ చేసి ఖాతా, యూపీఐ మరియు కార్డులను తక్షణమే ఫ్రీజ్ చేయించండి.
2. **1930 కు కాల్ చేయండి**: మొదటి 2-3 గంటల 'గోల్డెన్ అవర్' లోపు జాతీయ సైబర్ హెల్ప్‌లైన్ **1930** కు కాల్ చేసి డబ్బులు డ్రా కాకుండా ఆపండి.
3. **ఓటీపీ / యాప్ జాగ్రత్తలు**: ఎనీడెస్క్ వేస్తే వెంటనే ఇంటర్నెట్ ఆపి యాప్ డిలీట్ చేయండి. పిన్ చెబితే వెంటనే UPI PIN మార్చండి.
4. **సాక్ష్యాధారాలు దాచండి**: ఎస్ఎంఎస్, వాట్సాప్ చాట్లు, UTR నంబర్ల స్క్రీన్‌షాట్లు భద్రపరిచి [cybercrime.gov.in](https://cybercrime.gov.in) లో ఫిర్యాదు చేయండి.

🔗 **అధికారిక పోర్టల్‌లో ధృవీకరించండి:** [జాతీయ సైబర్ క్రైమ్ రిపోర్టింగ్ పోర్టల్ (హోం వ్యవహారాల మంత్రిత్వ శాఖ)](https://cybercrime.gov.in)"""

    else:
        return """**🚨 Emergency Safety Protocol (Golden Hour Action)**

If money was debited or you experienced cyber fraud, take these 4 immediate actions without delay:

1. **Call Your Bank Immediately**: Contact your bank's 24x7 emergency fraud desk to report unauthorized debit and freeze your account, UPI, and cards.
2. **Dial 1930 Helpline**: Call the National Cyber Crime Helpline **1930** within the 'Golden Hour' (first 2-3 hours) to freeze the stolen funds in transit.
3. **Secure Credentials & Device**: If AnyDesk/TeamViewer was installed, disconnect internet immediately and uninstall it. If an OTP or PIN was shared, change your UPI PIN right now.
4. **Preserve Evidence & Lodge Formal Report**: Take clear screenshots of debit SMS, chat history, and 12-digit UTR numbers, then file on [cybercrime.gov.in](https://cybercrime.gov.in).

🔗 **Verify on the official site:** [National Cyber Crime Reporting Portal (I4C, Ministry of Home Affairs)](https://cybercrime.gov.in)"""


def format_small_talk_response(lang: str = "en") -> str:
    """
    Friendly greeting and capability introduction. No verdict or score.
    """
    target_lang = lang if lang in ["hi", "te"] else "en"

    if target_lang == "hi":
        return """**नमस्ते! मैं यूपीआई रक्षक (UPI Rakshak) सुरक्षा सहायक हूँ।**

मैं डिजिटल भुगतान धोखाधड़ी, संदिग्ध मैसेज और साइबर सुरक्षा के लिए एक साक्ष्य-आधारित सहायक हूँ।

**मैं आपकी कैसे मदद कर सकता हूँ:**
- **संदिग्ध संदेश जांच**: कोई भी एसएमएस, व्हाट्सएप संदेश, लिंक, क्यूआर कोड या यूपीआई आईडी पेस्ट करके जांचें।
- **सहायता और नियम**: 1930 पर शिकायत, बैंक फ्रॉड से बचाव, डिजिटल अरेस्ट का सच आदि के बारे में पूछें।
- **आपातकालीन कदम**: यदि पैसे कट गए हों तो त्वरित सुरक्षा कदम जानें।

आप नीचे दिए गए विकल्पों में से चुन सकते हैं या सीधे अपना सवाल पूछ सकते हैं।"""

    elif target_lang == "te":
        return """**నమస్కారం! నేను యూపీఐ రక్షక్ (UPI Rakshak) భద్రతా సహాయకుడిని.**

నేను డిజిటల్ చెల్లింపు మోసాలు, అనుమానాస్పద మెసేజ్‌ల నుండి మిమ్మల్ని రక్షించే సాక్ష్యాధార-ఆధారిత సహాయకుడిని.

**నేను మీకు ఎలా సహాయపడగలను:**
- **సందేశాల పరిశీలన**: ఏదైనా అనుమానాస్పద ఎస్ఎంఎస్, లింక్, క్యూఆర్ లేదా యూపీఐ ఐడీని పేస్ట్ చేసి తనిఖీ చేయండి.
- **మార్గదర్శకాలు**: 1930 కు ఫిర్యాదు చేయడం, పోయిన డబ్బును ఆపడం, డిజిటల్ అరెస్ట్ గురించి తెలుసుకోండి.
- **అత్యవసర రక్షణ**: డబ్బులు కట్ అయితే తక్షణ గోల్డెన్ అవర్ చర్యలను పొందండి.

మీరు కింద ఉన్న బటన్లపై క్లిక్ చేయవచ్చు లేదా నేరుగా సందేశాన్ని పంపవచ్చు."""

    else:
        return """**Hello! I am UPI Rakshak Safety Assistant.**

I am an evidence-based cyber safety assistant protecting citizens from digital payment fraud and coercive cyber threats.

**How I can assist you:**
- **Check a Suspicious Message**: Paste any SMS, WhatsApp forward, payment link, QR screenshot, or UPI ID to evaluate threat risk.
- **Procedural Guidance**: Ask how to report to the 1930 helpline, how to block a UPI ID, what to do if an OTP was shared, or what digital arrest means.
- **Emergency Action**: Get immediate Golden-Hour steps if you experienced an unauthorized transaction.

Feel free to choose a quick prompt below or paste a message to inspect."""


def format_unclear_response(lang: str = "en") -> str:
    """
    Clarification prompt when user query is ambiguous. Never guesses.
    """
    target_lang = lang if lang in ["hi", "te"] else "en"

    if target_lang == "hi":
        return """**मैं ठीक से समझ नहीं पाया।**

क्या आप किसी संदिग्ध संदेश या लिंक की जांच करना चाहते हैं, या साइबर अपराध से जुड़ी कोई जानकारी या मदद चाहिए? 

कृपया नीचे दिए गए विकल्पों में से चुनें:"""

    elif target_lang == "te":
        return """**నాకు సరిగ్గా అర్థం కాలేదు.**

మీరు ఏదైనా అనుమానాస్పద సందేశాన్ని తనిఖీ చేయాలనుకుంటున్నారా, లేదా సైబర్ మోసాల నివేదిక గురించి సమాచారం కావాలా?

దయచేసి కింద ఉన్న ఎంపికలలో ఒకదాన్ని ఎంచుకోండి:"""

    else:
        return """**I didn't quite catch that.**

Would you like me to analyze a suspicious payment message/link for fraud, or do you need help with cybercrime reporting procedures and safety guidelines?

Please select an option below:"""


def format_low_confidence_fallback(lang: str = "en") -> str:
    """
    Low-confidence retrieval fallback. Never hallucinates unreviewed answers.
    """
    target_lang = lang if lang in ["hi", "te"] else "en"

    if target_lang == "hi":
        return "मुझे इस बारे में सटीक जानकारी नहीं है। कृपया आधिकारिक पोर्टल [cybercrime.gov.in](https://cybercrime.gov.in) देखें या राष्ट्रीय साइबर हेल्पलाइन 1930 पर संपर्क करें।"
    elif target_lang == "te":
        return "నాకు దీని గురించి ఖచ్చితమైన సమాచారం లేదు. దయచేసి అధికారిక పోర్టల్ [cybercrime.gov.in](https://cybercrime.gov.in) చూడండి లేదా 1930 కు సంప్రదించండి."
    else:
        return "I'm not sure. Please check [cybercrime.gov.in](https://cybercrime.gov.in) or call the national cyber helpline at 1930 for verified guidance."


def format_out_of_scope_response(lang: str = "en") -> str:
    """
    Polite redirect when user asks a general-knowledge or non-cybersecurity question.
    Explains UPI Rakshak AI's specialized role and offers immediate security assistance.
    """
    target_lang = lang if lang in ["hi", "te"] else "en"
    if target_lang == "hi":
        return (
            "मैं **UPI रक्षक AI** हूँ—डिजिटल भुगतान, UPI सुरक्षा और साइबर अपराध से बचाव के लिए विशेष रूप से बनाया गया सहायक।\n\n"
            "मैं सामान्य ज्ञान या असंबंधित विषयों के प्रश्नों के उत्तर नहीं दे सकता।\n\n"
            "यदि आपको किसी संदिग्ध संदेश, कॉल, लिंक या बैंक धोखाधड़ी की जांच करवानी है, तो कृपया यहाँ साझा करें।"
        )
    elif target_lang == "te":
        return (
            "నేను **UPI రక్షక్ AI**—డిజిటల్ చెల్లింపులు, UPI భద్రత మరియు సైబర్ మోసాల నివారణలో సహాయం చేయడానికి రూపొందించబడ్డాను.\n\n"
            "సాధారణ విషయాలు లేదా సంబంధం లేని ప్రశ్నలకు నేను సమాధానం ఇవ్వలేను.\n\n"
            "మీకు ఏదైనా అనుమానాస్పద మెసేజ్, లింక్ లేదా సైబర్ మోసం గురించి సహాయం కావాలంటే ఇక్కడ అడగండి."
        )
    else:
        return (
            "I am **UPI Rakshak AI**, specialized exclusively in digital payment safety, scam detection, and cybercrime defense.\n\n"
            "I cannot answer general-knowledge questions outside cybersecurity and digital payments.\n\n"
            "If you received a suspicious message, link, call, or need assistance reporting cyber fraud, paste it here or ask below."
        )


def format_threat_analysis_response(report: SafetyReport, lang: str = "en") -> str:
    """
    Formats an evidence-based threat analysis response for ANALYZE intent.
    No raw ### or #### artifacts; clean markdown typography.
    """
    verdict = report.verdict
    score = report.risk_score
    evidence_items = report.evidence[:3]
    actions = report.recommended_actions
    citations = report.citations
    target_lang = lang if lang in ["hi", "te"] else "en"

    if target_lang == "te":
        if verdict == "HIGH RISK":
            ev_bullets = "\n".join([f"• **ముఖ్య ఆధారం**: {e.signal}" for e in evidence_items])
            act_bullets = "\n".join([f"• {a}" for a in actions])
            rag_note = citations[0].content if citations else "UPI లో డబ్బు పొందడానికి పిన్ నమోదు చేయాల్సిన అవసరం లేదు."
            return f"""**🚨 అధిక ప్రమాదం (HIGH RISK) — స్కోర్: {score}/100**

మీరు పంపిన సందేశాన్ని విశ్లేషించిన తర్వాత, ఇది **మోసపూరితమైనది (SCAM)** అని బలమైన ఆధారాలు కనిపించాయి.

**🔍 కనిపించిన అనుమానాస్పద ఆధారాలు:**
{ev_bullets}

**🛑 మీరు ఏమి చేయకూడదు:**
• సందేశంలోని లింక్‌లపై ఎట్టి పరిస్థితుల్లోనూ క్లిక్ చేయవద్దు.
• ఎవరికీ మీ **UPI పిన్ (PIN)**, **OTP** లేదా కార్డు వివరాలు చెప్పవద్దు.
• డబ్బు తీసుకోవడానికి కలెక్ట్ రిక్వెస్ట్‌లను ఆమోదించవద్దు.

**✅ ఇప్పుడు మీరు తీసుకోవాల్సిన చర్యలు:**
{act_bullets}

**📋 సహాయం కోసం:**
1. డబ్బు కట్ అయితే, వెంటనే జాతీయ సైబర్ హెల్ప్‌లైన్ **1930** కు కాల్ చేయండి.
2. [cybercrime.gov.in](https://cybercrime.gov.in) లో అధికారిక ఫిర్యాదు నమోదు చేయండి.

🔗 **అధికారిక మార్గదర్శకం:** {rag_note}"""
        elif verdict == "SUSPICIOUS":
            ev_bullets = "\n".join([f"• {e.signal}" for e in evidence_items])
            return f"""**⚠️ అనుమానాస్పద కంటెంట్ హెచ్చరిక — స్కోర్: {score}/100**

ఈ సందేశంలో కొన్ని అసాధారణ సంకేతాలు గుర్తించబడ్డాయి. పూర్తిగా నిర్ధారించుకునే వరకు జాగ్రత్తగా ఉండండి.

**🔍 కనిపించిన సంకేతాలు:**
{ev_bullets}

**✅ జాగ్రత్తలు:**
• మీ బ్యాంక్ లేదా సర్వీస్ ప్రొవైడర్‌ను అధికారిక నంబర్ ద్వారా మాత్రమే సంప్రదించండి.
• మోసం జరిగితే **1930** హెల్ప్‌లైన్ నంబర్‌ను సంప్రదించండి."""
        else:
            return f"""**✅ సురక్షితంగా కనిపిస్తోంది — స్కోర్: {score}/100**

ఈ సందేశంలో ఎలాంటి ప్రమాదకరమైన లింక్‌లు లేదా మోసపూరిత సంకేతాలు కనిపించలేదు.

**🛡️ భద్రతా చిట్కా:**
• బ్యాంకులు ఎప్పుడూ ఫోన్ ద్వారా మీ రహస్య పాస్‌వర్డ్‌లు అడగవని గుర్తుంచుకోండి."""

    elif target_lang == "hi":
        if verdict == "HIGH RISK":
            ev_bullets = "\n".join([f"• **मुख्य प्रमाण**: {e.signal}" for e in evidence_items])
            act_bullets = "\n".join([f"• {a}" for a in actions])
            rag_note = citations[0].content if citations else "यूपीआई में पैसे प्राप्त करने के लिए कभी भी पिन डालने की आवश्यकता नहीं होती।"
            return f"""**🚨 उच्च जोखिम चेतावनी (HIGH RISK) — स्कोर: {score}/100**

आपके द्वारा भेजे गए संदेश के विश्लेषण से स्पष्ट होता है कि यह एक **धोखाधड़ी (SCAM)** का प्रयास है।

**🔍 क्या संदिग्ध पाया गया:**
{ev_bullets}

**🛑 आपको क्या बिल्कुल नहीं करना है:**
• संदेश में दिए गए किसी भी लिंक पर क्लिक न करें।
• अपना **यूपीआई पिन (UPI PIN)**, **ओटीपी (OTP)** या सीवीवी किसी को न बताएं।
• पैसे पाने के लिए कलेक्ट रिक्वेस्ट स्वीकार न करें।

**✅ अब आपको क्या करना चाहिए:**
{act_bullets}

**📞 शिकायत और सहायता:**
1. यदि खाते से पैसे कट चुके हैं, तो तुरंत राष्ट्रीय साइबर हेल्पलाइन **1930** पर कॉल करें।
2. [cybercrime.gov.in](https://cybercrime.gov.in) पर औपचारिक शिकायत दर्ज करें।

🔗 **आधिकारिक सुरक्षा नियम:** {rag_note}"""
        elif verdict == "SUSPICIOUS":
            ev_bullets = "\n".join([f"• {e.signal}" for e in evidence_items])
            return f"""**⚠️ संदिग्ध गतिविधि चेतावनी — स्कोर: {score}/100**

इस संदेश में कुछ असामान्य या जोखिम भरे लक्षण पाए गए हैं।

**🔍 मिले हुए संकेत:**
{ev_bullets}

**✅ सावधानियां:**
• संदेश में दिए नंबर के बजाय बैंक के आधिकारिक नंबर पर संपर्क करें।
• किसी भी संदेह पर **1930** हेल्पलाइन पर परामर्श लें।"""
        else:
            return f"""**✅ सुरक्षित प्रतीत होता है — स्कोर: {score}/100**

इस संदेश में कोई स्पष्ट दुर्भावनापूर्ण पैटर्न या खतरनाक लिंक नहीं मिले हैं।

**🛡️ सुरक्षा सलाह:**
• बैंक कभी भी फोन या एसएमएस के जरिए गोपनीय पिन नहीं मांगते।"""

    else:
        if verdict == "HIGH RISK":
            ev_bullets = "\n".join([f"• **Key Evidence**: {e.signal}" for e in evidence_items])
            act_bullets = "\n".join([f"• {a}" for a in actions])
            rag_note = citations[0].content if citations else "Receiving money on UPI never requires entering a PIN."
            return f"""**🚨 High Risk Threat Detected — Risk Score: {score}/100**

This message displays verifiable indicators of **fraudulent extortion or credential theft**.

**🔍 Key Malicious Indicators:**
{ev_bullets}

**🛑 Prohibited Actions:**
• Do NOT click on any link inside the message.
• NEVER enter your **UPI PIN**, **OTP**, or card details to receive funds.
• Do not install any remote screen-sharing tools (e.g. AnyDesk).

**✅ Recommended Actions:**
{act_bullets}

**📞 Reporting Assistance:**
1. If money was debited, call the National Cyber Crime Helpline **1930** immediately.
2. File a formal complaint at [cybercrime.gov.in](https://cybercrime.gov.in).

🔗 **Official Guidance:** {rag_note}"""
        elif verdict == "SUSPICIOUS":
            ev_bullets = "\n".join([f"• {e.signal}" for e in evidence_items])
            return f"""**⚠️ Suspicious Content Advisory — Risk Score: {score}/100**

This content exhibits anomalies or unverified urgency tactics. Exercise caution.

**🔍 Observed Signals:**
{ev_bullets}

**✅ Advisory:**
• Do not share financial credentials or authorize unknown payment requests.
• Contact your bank using official customer care channels only."""
        else:
            return f"""**✅ Likely Safe Communication — Risk Score: {score}/100**

No overt phishing patterns or malicious URLs were identified in this message.

**🛡️ Best Practice:**
• Remember that official institutions never ask for your UPI PIN or OTP over SMS or phone calls."""
