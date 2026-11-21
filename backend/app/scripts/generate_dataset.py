import os
import random
import pandas as pd

CATEGORIES = [
    "fake_bank_kyc",
    "electricity_disconnection",
    "fake_upi_refund_cashback",
    "lottery_prize",
    "fake_customer_support",
    "otp_pin_theft",
    "fake_govt_scheme",
    "legitimate"
]

BANKS = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "PNB", "Kotak Bank", "Bank of Baroda", "Canara Bank", "Paytm Bank"]
POWER_BOARDS = ["BESCOM", "TSSPDCL", "APCPDCL", "UPPCL", "TNEB", "MSEDCL", "BSES Yamuna", "PSPCL", "WBSEDCL"]
GOVT_SCHEMES = ["PM Kisan Samman Nidhi", "Rythu Bharosa Yojana", "PM Awas Yojana", "Ladli Behna Scheme", "Ayushman Card Subsidy", "Free Solar Chulha Scheme"]
REMOTE_APPS = ["AnyDesk", "TeamViewer", "QuickSupport", "RustDesk", "UltraViewer", "AirDroid"]
SHORTENERS = ["bit.ly/3xFake", "tinyurl.com/kyc99", "is.gd/refund9", "cutt.ly/bill-pay", "t.co/claim7"]
FAKE_DOMAINS = ["bank-kyc-verify.top", "bill-pay-help.online", "upi-reward-cashback.xyz", "gov-subsidy-claim.site", "customer-care-tollfree.club"]

def get_random_time():
    return random.choice(["Tonight 9:30 PM", "within 24 hours", "in next 2 hours", "by midnight", "today strictly"])

def get_fake_link():
    if random.random() < 0.4:
        return f"http://{random.choice(SHORTENERS)}"
    return f"http://{random.choice(FAKE_DOMAINS)}/auth?ref={random.randint(1000, 9999)}"

# Template banks per category & language
TEMPLATES = {
    "fake_bank_kyc": {
        "en": [
            "Dear customer, your {bank} account will be BLOCKED {time} due to pending KYC. Click here immediately to update: {link}",
            "Urgent: Your NetBanking access is suspended. Submit Aadhaar and PAN immediately at {link} to avoid permanent deactivation.",
            "{bank} Alert: Your debit card has been disabled due to expired KYC documentation. Reactivate now at {link}",
            "Your account is put on temporary hold. Complete video KYC verification now to prevent account closure: {link}",
            "Dear user, your bank profile is flagged for unverified status. Visit {link} and update credentials immediately."
        ],
        "hi": [
            "प्रिय ग्राहक, आपका {bank} खाता आज रात निलंबित कर दिया जाएगा क्योंकि केवाईसी लंबित है। तुरंत अपडेट करें: {link}",
            "सावधान: आपका बैंक खाता 24 घंटे में ब्लॉक हो जाएगा। पैन कार्ड और आधार तुरंत लिंक करने के लिए क्लिक करें: {link}",
            "{bank} सूचना: आपकी नेटबैंकिंग सेवा बंद कर दी गई है। केवाईसी नवीनीकरण के लिए तुरंत यहां जाएं: {link}",
            "आपका बैंक खाता तुरंत ब्लॉक होने वाला है। अपना केवाईसी पूरा करने के लिए इस लिंक पर जाएं: {link}"
        ],
        "te": [
            "ప్రియమైన వినియోగదారుడా, మీ {bank} ఖాతా కేవైసీ పెండింగ్ ఉన్నందున ఈ రాత్రి బ్లాక్ చేయబడుతుంది. వెంటనే నవీకరించండి: {link}",
            "అత్యవసరం: మీ బ్యాంక్ ఖాతా నిలిపివేయబడింది. పాన్ మరియు ఆధార్ వివరాలను ఇక్కడ నమోదు చేయండి: {link}",
            "{bank} హెచ్చరిక: కేవైసీ గడువు ముగిసింది. మీ ఏటీఎం కార్డు పనిచేయదు. వెంటనే యాక్టివేట్ చేసుకోండి: {link}",
            "మీ ఖాతా శాశ్వతంగా రద్దు చేయబడకుండా ఉండటానికి వెంటనే కేవైసీ వివరాలు సమర్పించండి: {link}"
        ],
        "hinglish": [
            "Dear user, aapka {bank} account suspended ho jayega {time} KYC pending hone ki wajah se. Turant update kare: {link}",
            "Aapka Netbanking block kar diya gaya hai. Unblock karne ke liye apna KYC submit kare: {link}",
            "Urgent notice: Bank account band hone se bachane ke liye abhi link par click karke verify kare: {link}"
        ],
        "roman_te": [
            "Mee {bank} account block avvakunda undalante ventane ee link open chesi KYC update cheyandi: {link}",
            "Urgent: Mee bank account freeze aindi. Unfreeze cheyadaniki ventane Aadhaar update cheyandi: {link}"
        ]
    },
    "electricity_disconnection": {
        "en": [
            "Dear Consumer, your electricity power will be disconnected {time} from electricity office because your previous month bill was not updated. Please immediately contact our power officer at +91-98765-43210 or pay at {link}",
            "URGENT NOTICE: {board} power supply will be cut off tonight at 9:30 PM due to unpaid balance of Rs. 4,850. Call electricity manager immediately or click {link}",
            "Electricity Alert: Bill overdue. Power line will be disconnected in 2 hours. Pay online now to avoid penalty: {link}",
            "Power Department: Your meter has been scheduled for disconnection today. Clear pending bill immediately at {link}"
        ],
        "hi": [
            "प्रिय उपभोक्ता, आपके बिजली का बिल अपडेट नहीं होने के कारण आज रात 9:30 बजे बिजली काट दी जाएगी। तुरंत हमारे बिजली अधिकारी से संपर्क करें या यहां भुगतान करें: {link}",
            "{board} सूचना: आपका पिछला बिजली बिल जमा नहीं हुआ है। आज कनेक्शन काट दिया जाएगा। तुरंत संपर्क करें: +91-98765-01234",
            "बिजली विभाग चेतावनी: बिल बकाया है। लाइन कटने से बचने के लिए तुरंत दिए गए लिंक पर जाएं: {link}"
        ],
        "te": [
            "ప్రియమైన వినియోగదారుడా, మీ విద్యుత్ బిల్లు చెల్లించనందున ఈ రాత్రి 9:30 గంటలకు విద్యుత్ సరఫరా నిలిపివేయబడుతుంది. వెంటనే మా విద్యుత్ అధికారిని సంప్రదించండి లేదా చెల్లించండి: {link}",
            "{board} హెచ్చరిక: మీ మీటర్ బకాయి ఉన్నందున విద్యుత్ కట్ చేయబడుతుంది. వెంటనే సంప్రదించండి: +91-98765-11223",
            "విద్యుత్ శాఖ అత్యవసర ప్రకటన: పెండింగ్ బిల్లును వెంటనే క్లియర్ చేయండి లేదా కనెక్షన్ రద్దు చేయబడుతుంది: {link}"
        ],
        "hinglish": [
            "Dear consumer, aapka bijli connection {time} cut kar diya jayega kyunki pichle mahine ka bill update nahi hua hai. Call kare: +91-98765-33221 ya visit kare {link}",
            "Bijli vibhag alert: Aaj raat 9:30 baje electricity disconnect ho jayegi. Turant bill bhare: {link}"
        ],
        "roman_te": [
            "Mee current bill update kaledu kabatti ee ratri power cut chestunnaru. Ventane power officer ki call cheyandi: +91-98765-99887",
            "Current supply cut avvakunda undalante ventane ee link lo bill pay cheyandi: {link}"
        ]
    },
    "fake_upi_refund_cashback": {
        "en": [
            "Congratulations! You have received a cashback refund of Rs. 3,500 on your UPI transaction. Click here to claim into your account: {link}",
            "Google Pay Reward: You won scratch card of Rs. 2,999. Accept the UPI collect request in PhonePe/Paytm and enter your UPI PIN to claim reward.",
            "PhonePe Refund Alert: Failed transaction refund of Rs. 4,200 is credited. Enter UPI PIN to receive money in your bank account immediately.",
            "Your UPI cashback voucher of Rs. 1,500 is expiring today! Click {link} and scan QR code to transfer directly to account.",
            "Payment reversed: Claim your disputed UPI transaction refund of Rs. 6,800. Accept collect request sent to your VPA."
        ],
        "hi": [
            "बधाई हो! आपको फोनपे/गूगलपे पर 2,999 रुपये का कैशबैक मिला है। पैसे सीधे खाते में पाने के लिए अपना यूपीआई पिन दर्ज करें: {link}",
            "यूपीआई रिफंड सूचना: आपके विफल लेनदेन का 4,500 रुपये का रिफंड वापस किया जा रहा है। कलेक्ट रिक्वेस्ट स्वीकार करें और पिन डालें।",
            "पेटीएम लकी ड्रॉ: आपको 3,000 रुपये का रिवॉर्ड मिला है। इसे क्लेम करने के लिए तुरंत क्लिक करें: {link}"
        ],
        "te": [
            "అభినందనలు! మీకు UPI లావాదేవీపై రూ. 3,500 క్యాష్‌బ్యాక్ వచ్చింది. మీ బ్యాంక్ ఖాతాలో జమ చేసుకోవడానికి ఇక్కడ క్లిక్ చేసి UPI పిన్ నమోదు చేయండి: {link}",
            "PhonePe రివార్డ్: మీకు రూ. 2,500 స్క్రాచ్ కార్డ్ వచ్చింది. డబ్బును పొందడానికి కలెక్ట్ రిక్వెస్ట్‌ను ఆమోదించి మీ పిన్ ఎంటర్ చేయండి.",
            "మీ విఫలమైన లావాదేవీ రీఫండ్ రూ. 5,000 సిద్ధంగా ఉంది. ఖాతాలోకి బదిలీ చేయడానికి లింక్ ఓపెన్ చేయండి: {link}"
        ],
        "hinglish": [
            "Badhai ho! Aapko Google Pay par Rs. 2,499 ka cashback mila hai. Claim karne ke liye collect request approve kare aur PIN dale.",
            "Aapka UPI refund Rs. 3,850 pending hai. Paise lene ke liye UPI PIN enter kare: {link}"
        ],
        "roman_te": [
            "Congratulations! Meeku Rs. 3,000 UPI cashback vachindi. Account loki collect cheyadaniki UPI PIN enter cheyandi.",
            "Mee failed UPI payment refund vachindi. Collect request accept chesi PIN kottandi: {link}"
        ]
    },
    "lottery_prize": {
        "en": [
            "KBC Jio Lucky Draw: Congratulations! Your mobile number won 25 Lakh Rupees in KBC all-India lottery. Call Lottery Manager Rana Pratap Singh at +91-98765-22110 to claim prize.",
            "You have won 1st prize of Rs. 15,00,000 in Maruti Car Mega Lucky Contest! Pay refundable registration fee of Rs. 4,999 to bank account immediately: {link}",
            "CONGRATULATIONS! Your WhatsApp number has won 50 Lakhs in international consumer lottery. Send bank details and claim processing fee now.",
            "Prize Notification: You are selected for iPhone 16 Pro Diwali Giveaway. Click {link} and pay Rs. 99 shipping fee to confirm delivery."
        ],
        "hi": [
            "केबीसी जियो लकी ड्रॉ: बधाई हो! आपके मोबाइल नंबर ने 25 लाख रुपये की लॉटरी जीती है। अपने इनाम का दावा करने के लिए तुरंत कॉल करें: +91-98765-88776",
            "बधाई! आपके नाम पर 15 लाख का इनाम निकला है। फाइल चार्ज 2,500 रुपये जमा करके अपनी लॉटरी राशि प्राप्त करें: {link}",
            "व्हाट्सएप लॉटरी में आपका 30 लाख का इनाम निकला है। मैनेजर से तुरंत संपर्क करें।"
        ],
        "te": [
            "కేబీసీ లక్కీ డ్రా: అభినందనలు! మీ నంబర్‌కు 25 లక్షల రూపాయల బహుమతి వచ్చింది. మేనేజర్‌ను సంప్రదించండి: +91-98765-44332",
            "మీరు 10 లక్షల రూపాయల కార్ లక్కీ డ్రా గెలుచుకున్నారు! రిజిస్ట్రేషన్ ఫీజు రూ. 1,999 చెల్లించి బహుమతి పొందండి: {link}",
            "భారీ బహుమతి: మీకు మొదటి బహుమతి లభించింది. వెంటనే మీ వివరాలు పంపండి."
        ],
        "hinglish": [
            "KBC All India Lucky Draw me aapka 25 Lakh ka lottery laga hai. Prize lene ke liye lottery officer ko WhatsApp kare: +91-98765-55443",
            "Aapne jita hai 10 Lakh cash prize. Claim karne ke liye registration fees jama kare: {link}"
        ],
        "roman_te": [
            "Meeku 25 Lakhs KBC lottery vachindi. Cash transfer cheyadaniki ventane call cheyandi: +91-98765-77665",
            "Lucky draw lo car geluchukunnaru. Processing fees pay chesi claim cheyandi: {link}"
        ]
    },
    "fake_customer_support": {
        "en": [
            "Dear user, for your pending refund query on {bank}, please download {app} app from Play Store and share the 9-digit remote access code with our support officer.",
            "Toll Free Support Desk: Facing UPI payment failed error? Install {app} on your smartphone and connect with our live technical agent immediately.",
            "Customer Care: To resolve your unauthorized transaction debit of Rs. 8,500, install {app} quick support tool and verify your screen with our representative.",
            "Official Support Helpline: Please install QuickSupport app and enter code 482-192-384 to allow bank supervisor to rectify your transaction."
        ],
        "hi": [
            "प्रिय ग्राहक, अपनी रिफंड समस्या के समाधान के लिए प्ले स्टोर से {app} ऐप डाउनलोड करें और हमारे कस्टमर केयर अधिकारी को 9 अंकों का कोड बताएं।",
            "कस्टमर सपोर्ट: कटे हुए पैसे वापस पाने के लिए तुरंत {app} इनस्टॉल करें और हमारी तकनीकी टीम से संपर्क करें।",
            "बैंक हेल्पडेस्क: अपने खाते से कटी राशि वापस पाने के लिए अपने फोन में {app} चालू करें।"
        ],
        "te": [
            "ప్రియమైన కస్టమర్, మీ రీఫండ్ సమస్య పరిష్కారం కోసం ప్లే స్టోర్ నుండి {app} యాప్‌ను డౌన్‌లోడ్ చేసి, 9 అంకెల కోడ్‌ను మా కస్టమర్ కేర్ ఎగ్జిక్యూటివ్‌తో షేర్ చేయండి.",
            "సహాయ కేంద్రం: మీ ఖాతా నుండి కట్ అయిన డబ్బును తిరిగి పొందడానికి వెంటనే {app} ఇన్‌స్టాల్ చేసుకోండి.",
            "కస్టమర్ కేర్ హెచ్చరిక: మీ సమస్యను తనిఖీ చేయడానికి మా అధికారికి {app} యాక్సెస్ ఇవ్వండి."
        ],
        "hinglish": [
            "Customer care support: Payment fas gaya hai to abhi {app} app download kare aur screen share karke support agent ko code bataye.",
            "Refund issue solve karne ke liye {app} install kare aur executive ko connect kare."
        ],
        "roman_te": [
            "Mee transaction problem solve cheyadaniki ventane {app} install chesi code share cheyandi.",
            "Customer support: Cut aina dabbulu venakki ravali ante {app} download cheyandi."
        ]
    },
    "otp_pin_theft": {
        "en": [
            "Bank Security Verification: Enter your 6-digit UPI PIN and debit card CVV to authenticate your identity and stop fraudulent withdrawal: {link}",
            "Dear customer, your card is used for international purchase of Rs. 49,999. If not done by you, immediately share OTP received on SMS with bank manager.",
            "URGENT: Suspicious transaction attempt detected. Enter your NetBanking password and OTP at {link} to freeze your funds safely.",
            "Verification needed: Please tell the 6-digit one-time password (OTP) received on your phone to cancel the pending debit order.",
            "To confirm cancellation of Rs. 12,000 transfer, please share your secret OTP code immediately with customer officer."
        ],
        "hi": [
            "बैंक सुरक्षा अलर्ट: अपने खाते से फर्जी निकासी रोकने के लिए तुरंत अपना 6 अंकों का यूपीआई पिन और ओटीपी यहां दर्ज करें: {link}",
            "सावधान: आपके खाते से 35,000 रुपये कटने का प्रयास हुआ है। इसे रद्द करने के लिए बैंक अधिकारी को एसएमएस पर आया ओटीपी बताएं।",
            "खाता सत्यापन: तुरंत अपना नेटबैंकिंग पासवर्ड और ओटीपी साझा करें ताकि आपका खाता सुरक्षित किया जा सके।"
        ],
        "te": [
            "బ్యాంక్ భద్రతా హెచ్చరిక: అనధికారిక లావాదేవీని రద్దు చేయడానికి మీ మొబైల్‌కు వచ్చిన 6 అంకెల ఓటీపీ (OTP) మరియు మీ UPI పిన్‌ను నమోదు చేయండి: {link}",
            "మీ ఖాతా నుండి రూ. 45,000 డ్రా చేసే ప్రయత్నం జరిగింది. దానిని ఆపడానికి మీ ఓటీపీ నంబర్‌ను వెంటనే మా మేనేజర్‌తో పంచుకోండి.",
            "వెరిఫికేషన్: లావాదేవీ రద్దు చేయడానికి మీ ఫోన్‌కు వచ్చిన రహస్య కోడ్ చెప్పండి."
        ],
        "hinglish": [
            "Bank verification: Fraud transaction cancel karne ke liye abhi aaya hua 6 digit OTP bank officer ko share kare.",
            "Apna account surakshit karne ke liye turant Debit card CVV aur ATM PIN verify kare: {link}"
        ],
        "roman_te": [
            "Fraud transaction aagadaniki mee mobile ki vachina OTP number ventane cheppandi.",
            "Account verify cheyadaniki UPI PIN and OTP link lo enter cheyandi: {link}"
        ]
    },
    "fake_govt_scheme": {
        "en": [
            "Government of India announcement: Under {scheme}, all Indian citizens are eligible for direct benefit transfer of Rs. 6,000. Apply now at: {link}",
            "Prime Minister Special Grant: Free smartphone and Rs. 5,000 cash subsidy approved for your ration card. Register within 24 hours at {link}",
            "Ministry of Finance: Claim your pending welfare subsidy of Rs. 12,500 under central government relief fund. Verify your bank account: {link}",
            "{scheme} Direct Benefit: Your registration is approved. Pay Rs. 299 processing fee via UPI to release funds into your bank account: {link}"
        ],
        "hi": [
            "भारत सरकार घोषणा: {scheme} के तहत सभी नागरिकों के खाते में 6,000 रुपये भेजे जा रहे हैं। तुरंत अपना नाम चेक करें और अप्लाई करें: {link}",
            "प्रधानमंत्री राहत कोष: आपके खाते में 5,000 रुपये की आर्थिक सहायता स्वीकृत हुई है। तुरंत रजिस्टर करें: {link}",
            "सरकारी योजना: मुफ्त मोबाइल और 3,000 रुपये की मासिक पेंशन पाने के लिए तुरंत इस पोर्टल पर जाएं: {link}"
        ],
        "te": [
            "భారత ప్రభుత్వం పథకం: {scheme} కింద అర్హులైన ప్రతి ఒక్కరికీ రూ. 6,000 నేరుగా బ్యాంక్ ఖాతాలో జమ చేయబడుతుంది. వెంటనే దరఖాస్తు చేసుకోండి: {link}",
            "ప్రభుత్వ సహాయ నిధి: మీ రేషన్ కార్డుపై రూ. 5,000 నగదు సాయం మంజూరైంది. ఈ లింక్‌లో రిజిస్టర్ చేసుకోండి: {link}",
            "{scheme} ప్రయోజనం: మీ పేరు లిస్ట్‌లో ఉంది. నగదు పొందడానికి వెంటనే క్లిక్ చేయండి: {link}"
        ],
        "hinglish": [
            "Govt of India update: {scheme} ke tahat har nagrik ko Rs. 6,000 mil rahe hain. Abhi apna form bhare: {link}",
            "PM Yojana: Sabhi ration card holders ko 5,000 rupaye ki sahayata rashi mil rahi hai. Apply kare: {link}"
        ],
        "roman_te": [
            "Govt Scheme: {scheme} kinda direct ga Rs. 6,000 mee account lo padathayi. Ventane apply cheyandi: {link}",
            "Free cash subsidy apply cheyadaniki ee link open chesi bank details fill cheyandi: {link}"
        ]
    },
    "legitimate": {
        "en": [
            "{bank}: An amount of Rs. 1,450.00 is debited from account ending 4821 on 21-Nov-2026 for UPI/Swiggy. Available balance: Rs. 24,190.00. If not done by you, SMS BLOCK to 56767. NEVER share your OTP or PIN with anyone.",
            "{bank} Security Alert: OTP for login to Internet Banking is 482910. Valid for 10 minutes. Do NOT share OTP or password with anyone, including bank employees.",
            "Dear Customer, your {board} electricity bill for account 1092837 is Rs. 1,280. Due date is 28-Nov-2026. Pay safely at official portal or electricity office.",
            "Your Amazon order #402-9182736 has been shipped and will be delivered by tomorrow. Track your package in the official Amazon app.",
            "{bank}: Rs. 5,000.00 credited to your account ending 9102 via UPI from Priya Sharma. Updated balance Rs. 38,400.00.",
            "Dear Customer, your monthly telecom postpaid bill of Rs. 649 is generated. Pay via official MyAirtel / MyJio app before due date.",
            "{bank}: You have requested password reset. Your verification code is 918204. Bank never asks for OTP or CVV over call or SMS.",
            "Transaction successful: Rs. 320 paid to Metro Rail via UPI. Ref No: 492019284719. Save paper, travel smart."
        ],
        "hi": [
            "{bank}: आपके खाते से 1,500 रुपये की राशि यूपीआई द्वारा काटी गई है। शेष राशि 18,500 रुपये है। अपना ओटीपी या पिन किसी से साझा न करें। बैंक कभी भी ओटीपी नहीं मांगता।",
            "{bank}: इंटरनेट बैंकिंग लॉगिन के लिए आपका ओटीपी 394812 है। यह 5 मिनट के लिए वैध है। इसे किसी को न बताएं।",
            "प्रिय उपभोक्ता, आपका बिजली बिल 850 रुपये नियत तिथि 25 तारीख तक देय है। आधिकारिक केंद्र पर सुरक्षित भुगतान करें।"
        ],
        "te": [
            "{bank}: మీ ఖాతా నుండి రూ. 1,200 UPI ద్వారా చెల్లించబడింది. మిగిలిన బ్యాలెన్స్ రూ. 15,300. మీ OTP లేదా PIN ఎవరితోనూ పంచుకోవద్దు. బ్యాంక్ ఎప్పుడూ OTP అడగదు.",
            "{bank}: లాగిన్ కోసం మీ OTP 582910. 10 నిమిషాలు మాత్రమే చెల్లుతుంది. దీనిని ఎవరికీ చెప్పవద్దు.",
            "మీ విద్యుత్ బిల్లు రూ. 940 చెల్లించడానికి ఆఖరి తేదీ 28వ తేదీ. అధికారిక కార్యాలయం లేదా వెబ్‌సైట్ ద్వారా సురక్షితంగా చెల్లించండి."
        ],
        "hinglish": [
            "{bank}: Rs 2,000 debited from your A/C via UPI. Balance Rs 12,400. Kabhi bhi apna OTP, UPI PIN kisi ko share na kare. Bank never calls for PIN.",
            "Aapka OTP 849201 hai. Yeh kisi ke saath share na kare, bank staff ke sath bhi nahi."
        ],
        "roman_te": [
            "{bank}: Rs 1,500 UPI dwara transfer cheyabadindi. Balance Rs 9,800. Mee OTP and PIN eppudu evaritho share cheyavoddu.",
            "Internet banking login kosam mee OTP 749201. Evariki cheppavaddu."
        ]
    }
}

def generate_sample(category: str, lang: str) -> dict:
    template = random.choice(TEMPLATES[category][lang])
    bank = random.choice(BANKS)
    board = random.choice(POWER_BOARDS)
    scheme = random.choice(GOVT_SCHEMES)
    app = random.choice(REMOTE_APPS)
    time_str = get_random_time()
    link = get_fake_link()

    text = template.format(
        bank=bank,
        board=board,
        scheme=scheme,
        app=app,
        time=time_str,
        link=link
    )
    
    # Introduce minor spelling or case variations occasionally for robustness
    if random.random() < 0.15:
        text = text.replace("http://", "hxxp://") if "http://" in text else text

    return {
        "text": text,
        "category": category,
        "language": "hi" if lang == "hinglish" else ("te" if lang == "roman_te" else lang),
        "script_style": lang,
        "is_scam": 0 if category == "legitimate" else 1
    }

def generate_full_dataset(target_total: int = 3600) -> pd.DataFrame:
    random.seed(42)
    samples = []
    samples_per_category = target_total // len(CATEGORIES)

    for cat in CATEGORIES:
        for _ in range(samples_per_category):
            lang_choice = random.choices(
                ["en", "hi", "te", "hinglish", "roman_te"],
                weights=[0.35, 0.25, 0.20, 0.10, 0.10],
                k=1
            )[0]
            samples.append(generate_sample(cat, lang_choice))

    df = pd.DataFrame(samples)
    # Shuffle
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    return df

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "synthetic_scam_dataset.csv")

    print(f"Generating synthetic multilingual scam dataset (target: 3,600+)...")
    dataset = generate_full_dataset(3600)
    dataset.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Saved {len(dataset)} samples to {out_path}")
    print(dataset["category"].value_counts())
    print("\nLanguage breakdown:")
    print(dataset["script_style"].value_counts())
