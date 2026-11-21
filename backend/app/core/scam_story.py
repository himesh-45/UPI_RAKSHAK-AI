from typing import Dict, Any, List, Optional
from backend.app.models.schemas import ScamStoryTimeline, ScamStoryStep

SCAM_STORIES_DATA = {
    "fake_bank_kyc": {
        "name": {"en": "Bank KYC Suspension Phishing", "hi": "फर्जी बैंक केवाईसी धोखाधड़ी", "te": "నకిలీ బ్యాంక్ కేవైసీ మోసం"},
        "overview": {
            "en": "Scammers pose as your bank claiming your NetBanking or debit card will be blocked immediately due to unverified KYC, directing you to a phishing portal.",
            "hi": "धोखेबाज बैंक अधिकारी बनकर संदेश भेजते हैं कि केवाईसी पूरा न होने पर आपका खाता आज रात ब्लॉक हो जाएगा और फर्जी लिंक पर जानकारी मांगते हैं।",
            "te": "కేవైసీ అప్‌డేట్ చేయకపోతే మీ బ్యాంక్ ఖాతా బ్లాక్ చేయబడుతుందని మోసగాళ్లు నకిలీ లింక్‌లను పంపి వ్యక్తిగత వివరాలను దొంగిలిస్తారు."
        },
        "steps": [
            {
                "en": {"stage": "Stage 1: Urgent Coercion", "title": "Panic Warning", "desc": "Victim receives an SMS stating their bank account or debit card will be blocked tonight.", "flag": "Artificial deadline ('tonight 9:30 PM' or 'within 2 hours')."},
                "hi": {"stage": "चरण 1: कृत्रिम घबराहट", "title": "धमकी भरा संदेश", "desc": "खाता आज रात ब्लॉक होने का फर्जी एसएमएस प्राप्त होता है।", "flag": "आपातकालीन समय सीमा ('आज रात 9:30 बजे')।"},
                "te": {"stage": "దశ 1: అత్యవసర హెచ్చరిక", "title": "బెదిరింపు సందేశం", "desc": "మీ బ్యాంక్ ఖాతా ఈ రాత్రే రద్దు చేయబడుతుందని సందేశం వస్తుంది.", "flag": "తక్షణ గడువు ('ఈ రాత్రి 9:30 గంటలకు')."}
            },
            {
                "en": {"stage": "Stage 2: Deceptive Redirection", "title": "Phishing Portal", "desc": "Victim clicks link leading to a cloned bank website ending in .top, .xyz, or .site.", "flag": "URL is not the verified official domain (e.g. sbi.co.in or hdfcbank.com)."},
                "hi": {"stage": "चरण 2: फर्जी वेबसाइट", "title": "क्लोन बैंक पोर्टल", "desc": "पीड़ित .top या .xyz वाली फर्जी बैंक वेबसाइट पर रीडायरेक्ट होता है।", "flag": "आधिकारिक डोमेन की जगह संदेहास्पद टीएलडी (.top, .xyz)।"},
                "te": {"stage": "దశ 2: నకిలీ వెబ్‌సైట్", "title": "క్లోన్డ్ బ్యాంకింగ్ పేజీ", "desc": "బాధితుడు .top లేదా .xyz డొమైన్‌తో ఉన్న నకిలీ బ్యాంక్ పేజీని తెరుస్తాడు.", "flag": "అధికారిక బ్యాంక్ డొమైన్ కాకపోవడం."}
            },
            {
                "en": {"stage": "Stage 3: Credential Harvesting", "title": "OTP & PIN Theft", "desc": "Page requests NetBanking password, debit card CVV, and 6-digit OTP to 'verify identity'.", "flag": "Banks NEVER ask for your password, PIN, or OTP over web links."},
                "hi": {"stage": "चरण 3: पासवर्ड चोरी", "title": "ओटीपी व पिन दर्ज करना", "desc": "पेज पर सत्यापन के नाम पर नेटबैंकिंग पासवर्ड, सीवीवी और ओटीपी मांगा जाता है।", "flag": "बैंक कभी भी ऑनलाइन लिंक पर गुप्त पिन या पासवर्ड नहीं मांगता।"},
                "te": {"stage": "దశ 3: రహస్య వివరాల తస్కరణ", "title": "పిన్ మరియు ఓటీపీ నమోదు", "desc": "వెరిఫికేషన్ పేరుతో నెట్‌బ్యాంకింగ్ పాస్‌వర్డ్ మరియు ఓటీపీ అడుగుతారు.", "flag": "బ్యాంకులు ఎప్పుడూ వెబ్ లింక్‌లలో పిన్ లేదా ఓటీపీ అడగవు."}
            },
            {
                "en": {"stage": "Stage 4: Unauthorized Debit", "title": "Account Drained", "desc": "Scammer uses harvested credentials to initiate immediate fund transfers or purchases.", "flag": "Multiple unauthorized debit alerts received immediately."},
                "hi": {"stage": "चरण 4: खाते से निकासी", "title": "पैसे चोरी", "desc": "धोखेबाज चोरी की गई जानकारी से तुरंत खाते से पैसे निकाल लेता है।", "flag": "खाते से अनधिकृत डेबिट का संदेश आना।"},
                "te": {"stage": "దశ 4: డబ్బు మాయం", "title": "ఖాతా ఖాళీ", "desc": "దొంగిలించిన వివరాలతో మీ ఖాతా నుండి డబ్బును ఇతర ఖాతాలకు బదిలీ చేస్తారు.", "flag": "వెంటనే ఖాతా నుండి డబ్బు కట్ అయినట్లు అలర్ట్ రావడం."}
            }
        ]
    },
    "collect_request_fraud": {
        "name": {"en": "UPI Collect Request Fraud", "hi": "यूपीआई कलेक्ट रिक्वेस्ट धोखा", "te": "యూపీఐ కలెక్ట్ రిక్వెస్ట్ మోసం"},
        "overview": {
            "en": "Attacker claims they are sending you money or a refund, but sends a 'Collect Request' instead, tricking you into entering your UPI PIN.",
            "hi": "धोखेबाज पैसे भेजने का झूठा दावा करके कलेक्ट रिक्वेस्ट भेजता है और पैसे प्राप्त करने के लिए पिन डालने को कहता है।",
            "te": "డబ్బులు పంపిస్తున్నామని నమ్మించి, కలెక్ట్ రిక్వెస్ట్ పంపి, డబ్బు జమ అవ్వడానికి మీ UPI పిన్ ఎంటర్ చేయాలని మోసం చేస్తారు."
        },
        "steps": [
            {
                "en": {"stage": "Stage 1: Lure of Funds", "title": "Payment Promise", "desc": "Scammer claims to buy an item on OLX, pay an advance, or process a pending cashback.", "flag": "Buyer is overly eager and refuses cash or direct in-person payment."},
                "hi": {"stage": "चरण 1: पैसे का लालच", "title": "भुगतान का वादा", "desc": "धोखेबाज ओएलएक्स सामान का अग्रिम या रिफंड भेजने का दावा करता है।", "flag": "व्यक्ति नकद या आमने-सामने मिलने से इनकार करता है।"},
                "te": {"stage": "దశ 1: ఆశ చూపడం", "title": "డబ్బు చెల్లింపు హామీ", "desc": "మీ వస్తువును కొంటామని లేదా అడ్వాన్స్ ఇస్తామని చెబుతారు.", "flag": "ప్రత్యక్షంగా కలవడానికి లేదా నగదు ఇవ్వడానికి నిరాకరిస్తారు."}
            },
            {
                "en": {"stage": "Stage 2: Trap Notification", "title": "Collect Request Sent", "desc": "Attacker pushes a 'Collect Request' or 'Pay Request' to victim's UPI app (GPay/PhonePe).", "flag": "App notification says 'Pay Rs. X' or 'Collect Request', NOT 'Credited'."},
                "hi": {"stage": "चरण 2: कलेक्ट रिक्वेस्ट", "title": "पेमेंट रिक्वेस्ट भेजना", "desc": "धोखेबाज पीड़ित के फोनपे/गूगलपे पर 'कलेक्ट' या 'पे' रिक्वेस्ट भेजता है।", "flag": "नोटिफिकेशन में 'Pay' लिखा होता है, 'Received' नहीं।"},
                "te": {"stage": "దశ 2: కలెక్ట్ రిక్వెస్ట్", "title": "నోటిఫికేషన్ రావడం", "desc": "మీ ఫోన్ పే లేదా గూగుల్ పే యాప్‌కు 'కలెక్ట్ రిక్వెస్ట్' పంపుతారు.", "flag": "యాప్‌లో 'Pay' లేదా 'Approve' అని ఉంటుంది, డబ్బు జమ అయినట్లు ఉండదు."}
            },
            {
                "en": {"stage": "Stage 3: Architectural Lie", "title": "PIN Entry Trick", "desc": "Scammer claims: 'Click Approve and enter your secret UPI PIN to receive the money.'", "flag": "GOLDEN RULE: Receiving money on UPI NEVER requires entering a PIN."},
                "hi": {"stage": "चरण 3: तकनीकी झूठ", "title": "पिन डालने का भ्रम", "desc": "धोखेबाज कहता है: 'पैसे खाते में पाने के लिए अपना यूपीआई पिन डालें।'", "flag": "स्वर्ण नियम: यूपीआई में पैसे प्राप्त करने के लिए कभी पिन की जरूरत नहीं होती।"},
                "te": {"stage": "దశ 3: మోసపూరిత అబద్ధం", "title": "పిన్ నమోదు చేయమనడం", "desc": "డబ్బులు మీ ఖాతాకు రావాలంటే పిన్ ఎంటర్ చేయాలని చెబుతారు.", "flag": "ముఖ్య నియమం: UPI లో డబ్బులు స్వీకరించడానికి ఎప్పుడూ పిన్ అవసరం లేదు."}
            },
            {
                "en": {"stage": "Stage 4: Instant Debit", "title": "Immediate Loss", "desc": "Entering the PIN authorizes a DEBIT. The money is transferred to the scammer's VPA instantly.", "flag": "Victim's balance decreases instantly."},
                "hi": {"stage": "चरण 4: पैसे कट जाना", "title": "तत्काल नुकसान", "desc": "पिन डालते ही पीड़ित के खाते से पैसे कटकर धोखेबाज के पास चले जाते हैं।", "flag": "पैसे आने के बजाय खाते से कटने का एसएमएस आना।"},
                "te": {"stage": "దశ 4: డబ్బు డెబిట్", "title": "నగదు నష్టం", "desc": "పిన్ కొట్టగానే మీ అకౌంట్ నుండి డబ్బులు మోసగాడి ఖాతాకు వెళ్ళిపోతాయి.", "flag": "ఖాతా నుండి డబ్బు కట్ అయినట్లు సందేశం రావడం."}
            }
        ]
    },
    "electricity_disconnection": {
        "name": {"en": "Electricity Disconnection Threat", "hi": "बिजली बिल डिस्कनेक्शन धोखा", "te": "విద్యుత్ సరఫరా రద్దు బెదిరింపు మోసం"},
        "overview": {
            "en": "Scammer sends a fake power disconnection threat due to unpaid bills, prompting the victim to call a personal phone number or install a malicious APK.",
            "hi": "बिजली विभाग का फर्जी नोटिस भेजकर आज रात बिजली काटने की धमकी दी जाती है और अज्ञात नंबर पर कॉल करने या ऐप डाउनलोड करने को कहा जाता है।",
            "te": "కరెంట్ బిల్లు చెల్లించలేదని, ఈ రాత్రే విద్యుత్ కట్ చేస్తామని బెదిరిస్తూ గుర్తుతెలియని నంబర్‌కు కాల్ చేయమని లేదా యాప్ ఎక్కించమని మోసం చేస్తారు."
        },
        "steps": [
            {
                "en": {"stage": "Stage 1: Ultimatums", "title": "Power Cut Notice", "desc": "SMS warns: 'Power line will be disconnected TONIGHT at 9:30 PM due to unpaid balance.'", "flag": "Utility companies never send individual threats with personal mobile contacts."},
                "hi": {"stage": "चरण 1: धमकी", "title": "बिजली काटने की चेतावनी", "desc": "एसएमएस आता है: 'पिछला बिल न भरने के कारण आज रात 9:30 बजे बिजली काट दी जाएगी।'", "flag": "बिजली विभाग कभी व्यक्तिगत मोबाइल नंबर से धमकी भरे एसएमएस नहीं भेजता।"},
                "te": {"stage": "దశ 1: బెదిరింపు", "title": "కరెంట్ కట్ నోటీసు", "desc": "గత నెల బిల్లు కట్టలేదని ఈ రాత్రి 9:30 కు కరెంట్ కట్ చేస్తామని మెసేజ్ వస్తుంది.", "flag": "విద్యుత్ శాఖ వ్యక్తిగత నంబర్లతో ఇలాంటి సందేశాలు పంపదు."}
            },
            {
                "en": {"stage": "Stage 2: Panic Call", "title": "Contacting Imposter", "desc": "Victim calls the 10-digit mobile number provided in the message out of panic.", "flag": "Contact is a standard 10-digit mobile number, not an official utility DISCOM call center."},
                "hi": {"stage": "चरण 2: फर्जी कॉल", "title": "अधिकारी से बातचीत", "desc": "घबराकर पीड़ित संदेश में दिए गए 10 अंकों के मोबाइल नंबर पर कॉल करता है।", "flag": "नंबर किसी आधिकारिक कॉल सेंटर का नहीं, बल्कि व्यक्तिगत मोबाइल होता है।"},
                "te": {"stage": "దశ 2: మోసగాడికి కాల్", "title": "అధికారితో మాట్లాడటం", "desc": "కంగారులో బాధితుడు మెసేజ్‌లోని 10 అంకెల మొబైల్ నంబర్‌కు ఫోన్ చేస్తాడు.", "flag": "అది అధికారిక కస్టమర్ కేర్ నంబర్ కాదు, సాధారణ మొబైల్ నంబర్."}
            },
            {
                "en": {"stage": "Stage 3: Malware / Remote Access", "title": "Malicious App / Re-charge", "desc": "Imposter tells victim to download an APK or QuickSupport app to 'update meter records'.", "flag": "Never install unknown APKs or remote desktop apps on advice of callers."},
                "hi": {"stage": "चरण 3: रिमोट ऐप", "title": "ऐप डाउनलोड करवाना", "desc": "धोखेबाज मीटर अपडेट के नाम पर AnyDesk या संदिग्ध APK डाउनलोड करवाता है।", "flag": "फोन में कभी भी अनजान व्यक्ति के कहने पर रिमोट ऐप न डालें।"},
                "te": {"stage": "దశ 3: యాప్ ఇన్‌స్టాలేషన్", "title": "మాల్‌వేర్ లేదా రిమోట్ యాప్", "desc": "మీటర్ అప్‌డేట్ చేయాలని AnyDesk లేదా నకిలీ APK ఫైల్ డౌన్‌లోడ్ చేయిస్తారు.", "flag": "ఎవరి మాటలు విని మీ ఫోన్‌లో స్క్రీన్ షేరింగ్ యాప్‌లు ఇన్‌స్టాల్ చేయవద్దు."}
            },
            {
                "en": {"stage": "Stage 4: Silent Takeover", "title": "Bank Siphoning", "desc": "Once screen access is granted, scammer observes banking credentials and transfers funds.", "flag": "Phone screen turns black or unresponsive while debits occur."},
                "hi": {"stage": "चरण 4: खाते से चोरी", "title": "रुपये गायब", "desc": "स्क्रीन देखते हुए धोखेबाज नेटबैंकिंग या यूपीआई से पूरे पैसे निकाल लेता है।", "flag": "स्क्रीन पर अनधिकृत लेनदेन होना।"},
                "te": {"stage": "దశ 4: ఖాతా ఖాళీ", "title": "డబ్బు చోరీ", "desc": "మీ స్క్రీన్ చూస్తూ బ్యాంక్ ఓటీపీలు మరియు వివరాలను ఉపయోగించి డబ్బు కాజేస్తారు.", "flag": "బ్యాంక్ ఖాతా నుండి పెద్ద మొత్తంలో డబ్బు కట్ అవ్వడం."}
            }
        ]
    },
    "remote_access_scam": {
        "name": {"en": "Remote Device Takeover Scam", "hi": "रिमोट एक्सेस ऐप धोखा", "te": "రిమోట్ యాక్సెస్ యాప్ మోసం"},
        "overview": {
            "en": "Imposter instructs you to install AnyDesk, TeamViewer, or QuickSupport to 'resolve' a refund or KYC issue, gaining full control over your smartphone.",
            "hi": "कस्टमर सपोर्ट बनकर धोखेबाज रिमोट ऐप (AnyDesk/TeamViewer) इनस्टॉल करवाता है और फोन का पूरा नियंत्रण हासिल कर लेता है।",
            "te": "రీఫండ్ ఇస్తామని చెప్పి AnyDesk లేదా TeamViewer యాప్‌లను ఇన్‌స్టాల్ చేయించి, మీ ఫోన్ నియంత్రణను వారి చేతుల్లోకి తీసుకుంటారు."
        },
        "steps": [
            {
                "en": {"stage": "Stage 1: Support Pretence", "title": "Helpdesk Trap", "desc": "Victim seeks help for failed UPI transfer; finds fake toll-free number on search engine.", "flag": "Search engine ads often host fake customer care numbers."},
                "hi": {"stage": "चरण 1: हेल्पडेस्क का झांसा", "title": "सहायता केंद्र", "desc": "विफल लेनदेन पर मदद ढूंढते समय पीड़ित को फर्जी कस्टमर केयर नंबर मिलता है।", "flag": "गूगल सर्च पर मिलने वाले नंबर अक्सर फर्जी होते हैं।"},
                "te": {"stage": "దశ 1: సహాయ కేంద్రం వల", "title": "నకిలీ కస్టమర్ కేర్", "desc": "ఫెయిల్ అయిన లావాదేవీ కోసం గూగుల్‌లో వెతికినప్పుడు నకిలీ నంబర్ దొరుకుతుంది.", "flag": "గూగుల్ సెర్చ్‌లో కనిపించే నకిలీ హెల్ప్‌లైన్ నంబర్లు."}
            },
            {
                "en": {"stage": "Stage 2: App Download", "title": "Screen Sharing Tool", "desc": "Agent asks victim to install AnyDesk/RustDesk from app store and share 9-digit code.", "flag": "Official bank employees NEVER ask to install remote access tools."},
                "hi": {"stage": "चरण 2: ऐप डाउनलोड", "title": "9 अंकों का कोड", "desc": "अधिकारी बनकर धोखेबाज AnyDesk इनस्टॉल करवाकर 9 अंकों का कोड मांगता है।", "flag": "बैंक कभी भी रिमोट डेस्कटॉप ऐप डाउनलोड करने को नहीं कहता।"},
                "te": {"stage": "దశ 2: యాప్ డౌన్‌లోడ్", "title": "9 అంకెల కోడ్ అడగడం", "desc": "AnyDesk లేదా QuickSupport డౌన్‌లోడ్ చేయించి 9 అంకెల కోడ్ చెప్పమంటారు.", "flag": "బ్యాంక్ ఉద్యోగులు ఎప్పుడూ స్క్రీన్ షేరింగ్ యాప్‌లను అడగరు."}
            },
            {
                "en": {"stage": "Stage 3: Screen Monitoring", "title": "Observing UPI PIN", "desc": "Agent tells victim to open UPI app and 'type a test amount' or enter PIN.", "flag": "Never enter PIN while any remote screen-sharing session is active."},
                "hi": {"stage": "चरण 3: स्क्रीन रिकॉर्डिंग", "title": "पिन देखते हुए", "desc": "धोखेबाज यूपीआई ऐप खोलने को कहता है और स्क्रीन पर दर्ज पिन देख लेता है।", "flag": "स्क्रीन शेयरिंग के दौरान कभी भी पिन या पासवर्ड न डालें।"},
                "te": {"stage": "దశ 3: స్క్రీన్ పర్యవేక్షణ", "title": "పిన్ గమనించడం", "desc": "మీ బ్యాంక్ యాప్ ఓపెన్ చేయించి మీరు కొట్టే రహస్య పిన్‌ను వారు చూస్తారు.", "flag": "స్క్రీన్ షేర్ అవుతున్నప్పుడు ఎప్పుడూ పాస్‌వర్డ్ కొట్టవద్దు."}
            },
            {
                "en": {"stage": "Stage 4: Complete Compromise", "title": "Unauthorized Transfers", "desc": "Attacker initiates transfers while victim is distracted on call.", "flag": "Immediate SMS alerts of money debited to third-party accounts."},
                "hi": {"stage": "चरण 4: खाते की लूट", "title": "रुपये ट्रांसफर", "desc": "धोखेबाज कॉल पर उलझाकर खाते से सारे पैसे ट्रांसफर कर लेता है।", "flag": "कॉल चालू रहते ही खाते से पैसे कट जाना।"},
                "te": {"stage": "దశ 4: సర్వం లూటీ", "title": "ఖాతా ఖాళీ", "desc": "కాల్‌లో మాట్లాడుతూనే మీ ఖాతాలోని మొత్తం డబ్బును బదిలీ చేసుకుంటారు.", "flag": "ఫోన్ మాట్లాడుతుండగానే డబ్బు కట్ అయిన మెసేజ్‌లు రావడం."}
            }
        ]
    }
}

class ScamStoryEngine:
    def get_timeline(self, category: str, lang: str = "en") -> Optional[ScamStoryTimeline]:
        target_lang = lang if lang in ["en", "hi", "te"] else "en"
        data = SCAM_STORIES_DATA.get(category)
        if not data:
            # Fallback generic timeline if category not specifically defined
            return ScamStoryTimeline(
                category=category,
                category_name=category.replace("_", " ").title(),
                overview="Financial fraud pattern targeting digital payment credentials or unverified transfers.",
                steps=[
                    ScamStoryStep(
                        step_number=1,
                        stage="Initial Hook",
                        title="Unsolicited Contact",
                        description="Victim receives an unexpected message offering money, discounts, or threatening immediate block.",
                        warning_sign="Unsolicited urgency or unexpected financial offer."
                    ),
                    ScamStoryStep(
                        step_number=2,
                        stage="Coercion & Lure",
                        title="Credential Extraction",
                        description="Victim is coerced into sharing OTP, scanning a QR code, or clicking a deceptive link.",
                        warning_sign="Requests for PIN, OTP, or remote screen sharing."
                    ),
                    ScamStoryStep(
                        step_number=3,
                        stage="Execution",
                        title="Unauthorized Debit",
                        description="Funds are transferred immediately to fraudulent accounts or mule VPAs.",
                        warning_sign="Receiving money never requires entering a PIN."
                    )
                ]
            )

        cat_name = data["name"].get(target_lang, data["name"]["en"])
        overview = data["overview"].get(target_lang, data["overview"]["en"])
        raw_steps = data["steps"]

        steps = []
        for idx, s in enumerate(raw_steps, 1):
            s_dict = s.get(target_lang, s.get("en", {}))
            steps.append(ScamStoryStep(
                step_number=idx,
                stage=s_dict["stage"],
                title=s_dict["title"],
                description=s_dict["desc"],
                warning_sign=s_dict["flag"]
            ))

        return ScamStoryTimeline(
            category=category,
            category_name=cat_name,
            overview=overview,
            steps=steps
        )

scam_story_engine = ScamStoryEngine()
