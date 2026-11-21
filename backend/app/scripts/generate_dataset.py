import os
import random
import re
import pandas as pd
from typing import List, Dict, Any

# 15 Categories matching modern digital payments threat landscape
CATEGORIES = [
    "fake_bank_kyc",
    "electricity_disconnection",
    "fake_upi_refund_cashback",
    "collect_request_fraud",
    "lottery_prize",
    "fake_customer_support",
    "remote_access_scam",
    "otp_pin_theft",
    "fake_govt_scheme",
    "job_investment_scam",
    "loan_app_extortion",
    "courier_customs_scam",
    "marketplace_qr_scam",
    "accidental_transfer_scam",
    "legitimate"
]

BANKS = [
    "SBI", "State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank",
    "Punjab National Bank", "PNB", "Kotak Mahindra Bank", "Bank of Baroda",
    "Canara Bank", "Union Bank of India", "IndusInd Bank", "Paytm Payments Bank"
]

POWER_BOARDS = [
    "BESCOM", "TSSPDCL", "APCPDCL", "UPPCL", "TNEB", "MSEDCL", "PSPCL",
    "WBSEDCL", "DHBVN", "Tata Power", "BSES Yamuna", "Adani Electricity"
]

GOVT_SCHEMES = [
    "PM Kisan Samman Nidhi", "Rythu Bharosa", "PM Awas Yojana",
    "Ladli Behna Scheme", "Ayushman Golden Card", "Free Solar Chulha Yojana",
    "PM Mudra Loan Scheme", "Kanya Sumangala Yojana", "Annadata Sukhibhava"
]

REMOTE_APPS = ["AnyDesk", "TeamViewer", "QuickSupport", "RustDesk", "UltraViewer", "AirDroid"]
COURIER_BRANDS = ["FedEx India", "BlueDart Express", "India Post SpeedPost", "DHL Express", "Delhivery", "DTDC"]

SHORTENERS = [
    "bit.ly/3xSafe", "tinyurl.com/kyc-fix", "is.gd/upi-pay", "cutt.ly/discom-bill",
    "t.co/claim-now", "rb.gy/bank-alert", "shorturl.at/upi99", "bl.ink/kyc-update"
]

FAKE_DOMAINS = [
    "bank-kyc-verify.top", "bill-pay-help.online", "upi-reward-cashback.xyz",
    "gov-subsidy-claim.site", "customer-care-tollfree.club", "sbi-kyc-update.biz",
    "hdfc-netbanking-portal.top", "power-bill-disconnection.xyz", "customs-parcel-clearance.top",
    "instant-loan-recovery.online", "kbc-lottery-winner.site", "parttime-earning-tasks.club"
]

TIMES = [
    "Tonight 9:30 PM", "within 24 hours", "in next 2 hours", "strictly by midnight",
    "immediately", "within 1 hour", "today before 6 PM", "within 30 minutes"
]

AMOUNTS = [
    "Rs. 1,450", "Rs. 2,999", "Rs. 3,500", "Rs. 4,850", "Rs. 6,200",
    "Rs. 8,500", "Rs. 12,000", "Rs. 15,000", "Rs. 25,000", "Rs. 49,999"
]

LEETSPEAK_SUBS = {
    "OTP": ["0TP", "O T P", "O-T-P", "O.T.P"],
    "PIN": ["P1N", "P I N", "P-I-N", "P.I.N"],
    "KYC": ["K Y C", "K-Y-C", "K.Y.C"],
    "click": ["cl1ck", "cl!ck", "c1ick"],
    "verify": ["v3rify", "ver!fy"],
    "update": ["upd4te", "upd@te"],
    "block": ["bl0ck", "bl0cked"],
    "refund": ["r3fund", "ref-und"],
    "cashback": ["c4shb4ck", "c@shback"]
}

def inject_noise(text: str) -> str:
    """Randomly injects realistic SMS shorthand, leetspeak, zero-width spaces or typos."""
    roll = random.random()
    if roll < 0.20:
        for word, subs in LEETSPEAK_SUBS.items():
            if word in text and random.random() < 0.5:
                text = text.replace(word, random.choice(subs), 1)
    elif roll < 0.30:
        # Zero-width space injection
        pos = random.randint(5, max(6, len(text) - 5))
        text = text[:pos] + "\u200B" + text[pos:]
    return text

def get_fake_link():
    if random.random() < 0.4:
        return f"http://{random.choice(SHORTENERS)}"
    return f"http://{random.choice(FAKE_DOMAINS)}/auth?ref={random.randint(1000, 9999)}"

# Base templates per category and linguistic modality
# Each template has a unique template_id
RAW_TEMPLATE_DEFS = {
    "fake_bank_kyc": {
        "en": [
            ("kyc_en_1", "Dear customer, your {bank} account will be BLOCKED {time} due to pending KYC. Click immediately: {link}"),
            ("kyc_en_2", "URGENT: Your NetBanking access is suspended. Submit Aadhaar and PAN immediately at {link} to avoid deactivation."),
            ("kyc_en_3", "{bank} Alert: Your debit card has been disabled due to expired KYC documentation. Reactivate now at {link}"),
            ("kyc_en_4", "Your account is put on temporary hold. Complete video KYC verification now to prevent account closure: {link}"),
            ("kyc_en_5", "Dear user, your bank profile is flagged for unverified status. Visit {link} and update credentials immediately."),
            ("kyc_en_6", "Mandatory RBI KYC Directive: Update your PAN card for {bank} account within 24 hours at {link} or face fine."),
            ("kyc_en_7", "Security Notice: Suspicious activity detected on {bank} profile. Confirm your KYC credentials here: {link}"),
            ("kyc_en_8", "{bank} NetBanking: Service expired today. Click {link} to submit KYC form online without visiting branch.")
        ],
        "hi": [
            ("kyc_hi_1", "प्रिय ग्राहक, आपका {bank} खाता {time} निलंबित कर दिया जाएगा क्योंकि केवाईसी लंबित है। तुरंत अपडेट करें: {link}"),
            ("kyc_hi_2", "सावधान: आपका बैंक खाता 24 घंटे में ब्लॉक हो जाएगा। पैन कार्ड और आधार तुरंत लिंक करने के लिए क्लिक करें: {link}"),
            ("kyc_hi_3", "{bank} सूचना: आपकी नेटबैंकिंग सेवा बंद कर दी गई है। केवाईसी नवीनीकरण के लिए तुरंत यहां जाएं: {link}"),
            ("kyc_hi_4", "आपका बैंक खाता तुरंत ब्लॉक होने वाला है। अपना केवाईसी पूरा करने के लिए इस लिंक पर जाएं: {link}"),
            ("kyc_hi_5", "आरबीआई निर्देश: अपने {bank} खाते को चालू रखने के लिए तुरंत आधार ई-केवाईसी पूरा करें: {link}")
        ],
        "te": [
            ("kyc_te_1", "ప్రియమైన వినియోగదారుడా, మీ {bank} ఖాతా కేవైసీ పెండింగ్ ఉన్నందున {time} బ్లాక్ చేయబడుతుంది. వెంటనే నవీకరించండి: {link}"),
            ("kyc_te_2", "అత్యవసరం: మీ బ్యాంక్ ఖాతా నిలిపివేయబడింది. పాన్ మరియు ఆధార్ వివరాలను ఇక్కడ నమోదు చేయండి: {link}"),
            ("kyc_te_3", "{bank} హెచ్చరిక: కేవైసీ గడువు ముగిసింది. మీ ఏటీఎం కార్డు పనిచేయదు. వెంటనే యాక్టివేట్ చేసుకోండి: {link}"),
            ("kyc_te_4", "మీ ఖాతా శాశ్వతంగా రద్దు చేయబడకుండా ఉండటానికి వెంటనే కేవైసీ వివరాలు సమర్పించండి: {link}")
        ],
        "hinglish": [
            ("kyc_hn_1", "Dear user, aapka {bank} account suspended ho jayega {time} KYC pending hone ki wajah se. Turant update kare: {link}"),
            ("kyc_hn_2", "Aapka Netbanking block kar diya gaya hai. Unblock karne ke liye apna KYC submit kare: {link}"),
            ("kyc_hn_3", "Urgent notice: Bank account band hone se bachane ke liye abhi link par click karke verify kare: {link}")
        ],
        "roman_te": [
            ("kyc_rt_1", "Mee {bank} account block avvakunda undalante ventane ee link open chesi KYC update cheyandi: {link}"),
            ("kyc_rt_2", "Urgent: Mee bank account freeze aindi. Unfreeze cheyadaniki ventane Aadhaar update cheyandi: {link}")
        ]
    },
    "electricity_disconnection": {
        "en": [
            ("elec_en_1", "Dear Consumer, your electricity power will be disconnected {time} from electricity office because your previous month bill was not updated. Contact officer at +91-98765-43210 or pay at {link}"),
            ("elec_en_2", "URGENT NOTICE: {board} power supply will be cut off {time} due to unpaid balance of {amount}. Call electricity manager immediately or click {link}"),
            ("elec_en_3", "Electricity Alert: Bill overdue. Power line will be disconnected in 2 hours. Pay online now to avoid penalty: {link}"),
            ("elec_en_4", "Power Department: Your meter has been scheduled for disconnection today. Clear pending bill immediately at {link}"),
            ("elec_en_5", "{board} Alert: Meter disconnected notice issued. Pay {amount} immediately to restore line: {link}")
        ],
        "hi": [
            ("elec_hi_1", "प्रिय उपभोक्ता, आपके बिजली का बिल अपडेट नहीं होने के कारण {time} बिजली काट दी जाएगी। तुरंत हमारे बिजली अधिकारी से संपर्क करें या यहां भुगतान करें: {link}"),
            ("elec_hi_2", "{board} सूचना: आपका पिछला बिजली बिल जमा नहीं हुआ है। आज कनेक्शन काट दिया जाएगा। तुरंत संपर्क करें: +91-98765-01234"),
            ("elec_hi_3", "बिजली विभाग चेतावनी: बिल बकाया है। लाइन कटने से बचने के लिए तुरंत दिए गए लिंक पर जाएं: {link}"),
            ("elec_hi_4", "प्रिय उपभोक्ता, आपके बिजली का बिल अपडेट नहीं होने के कारण {time} बिजली काट दी जाएगी।"),
            ("elec_hi_5", "बिजली विभाग: आपका बिल अपडेट न होने के कारण आज कनेक्शन काट दिया जाएगा।")
        ],
        "te": [
            ("elec_te_1", "ప్రియమైన వినియోగదారుడా, మీ విద్యుత్ బిల్లు చెల్లించనందున {time} విద్యుత్ సరఫరా నిలిపివేయబడుతుంది. వెంటనే మా విద్యుత్ అధికారిని సంప్రదించండి లేదా చెల్లించండి: {link}"),
            ("elec_te_2", "{board} హెచ్చరిక: మీ మీటర్ బకాయి ఉన్నందున విద్యుత్ కట్ చేయబడుతుంది. వెంటనే సంప్రదించండి: +91-98765-11223"),
            ("elec_te_3", "విద్యుత్ శాఖ అత్యవసర ప్రకటన: పెండింగ్ బిల్లును వెంటనే క్లియర్ చేయండి లేదా కనెక్షన్ రద్దు చేయబడుతుంది: {link}")
        ],
        "hinglish": [
            ("elec_hn_1", "Dear consumer, aapka bijli connection {time} cut kar diya jayega kyunki pichle mahine ka bill update nahi hua hai. Call kare: +91-98765-33221 ya visit kare {link}"),
            ("elec_hn_2", "Bijli vibhag alert: Aaj raat 9:30 baje electricity disconnect ho jayegi. Turant bill bhare: {link}")
        ],
        "roman_te": [
            ("elec_rt_1", "Mee current bill update kaledu kabatti power cut chestunnaru. Ventane power officer ki call cheyandi: +91-98765-99887"),
            ("elec_rt_2", "Current supply cut avvakunda undalante ventane ee link lo bill pay cheyandi: {link}")
        ]
    },
    "fake_upi_refund_cashback": {
        "en": [
            ("ref_en_1", "Congratulations! You have received a cashback refund of {amount} on your UPI transaction. Click here to claim into your account: {link}"),
            ("ref_en_2", "Google Pay Reward: You won scratch card of {amount}. Accept the UPI collect request in PhonePe/Paytm and enter your UPI PIN to claim reward."),
            ("ref_en_3", "PhonePe Refund Alert: Failed transaction refund of {amount} is credited. Enter UPI PIN to receive money in your bank account immediately."),
            ("ref_en_4", "Your UPI cashback voucher of {amount} is expiring today! Click {link} and scan QR code to transfer directly to account."),
            ("ref_en_5", "Payment reversed: Claim your disputed UPI transaction refund of {amount}. Accept collect request sent to your VPA.")
        ],
        "hi": [
            ("ref_hi_1", "बधाई हो! आपको फोनपे/गूगलपे पर {amount} का कैशबैक मिला है। पैसे सीधे खाते में पाने के लिए अपना यूपीआई पिन दर्ज करें: {link}"),
            ("ref_hi_2", "यूपीआई रिफंड सूचना: आपके विफल लेनदेन का {amount} का रिफंड वापस किया जा रहा है। कलेक्ट रिक्वेस्ट स्वीकार करें और पिन डालें।"),
            ("ref_hi_3", "पेटीएम लकी ड्रॉ: आपको {amount} का रिवॉर्ड मिला है। इसे क्लेम करने के लिए तुरंत क्लिक करें: {link}")
        ],
        "te": [
            ("ref_te_1", "అభినందనలు! మీకు UPI లావాదేవీపై {amount} క్యాష్‌బ్యాక్ వచ్చింది. మీ బ్యాంక్ ఖాతాలో జమ చేసుకోవడానికి ఇక్కడ క్లిక్ చేసి UPI పిన్ నమోదు చేయండి: {link}"),
            ("ref_te_2", "PhonePe రివార్డ్: మీకు {amount} స్క్రాచ్ కార్డ్ వచ్చింది. డబ్బును పొందడానికి కలెక్ట్ రిక్వెస్ట్‌ను ఆమోదించి మీ పిన్ ఎంటర్ చేయండి."),
            ("ref_te_3", "మీ విఫలమైన లావాదేవీ రీఫండ్ {amount} సిద్ధంగా ఉంది. ఖాతాలోకి బదిలీ చేయడానికి లింక్ ఓపెన్ చేయండి: {link}")
        ],
        "hinglish": [
            ("ref_hn_1", "Badhai ho! Aapko Google Pay par {amount} ka cashback mila hai. Claim karne ke liye collect request approve kare aur PIN dale."),
            ("ref_hn_2", "Aapka UPI refund {amount} pending hai. Paise lene ke liye UPI PIN enter kare: {link}")
        ],
        "roman_te": [
            ("ref_rt_1", "Congratulations! Meeku {amount} UPI cashback vachindi. Account loki collect cheyadaniki UPI PIN enter cheyandi."),
            ("ref_rt_2", "Mee failed UPI payment refund vachindi. Collect request accept chesi PIN kottandi: {link}")
        ]
    },
    "collect_request_fraud": {
        "en": [
            ("col_en_1", "I am sending you {amount}. Approve the collect request on Google Pay/PhonePe and enter your secret UPI PIN to receive money into your bank."),
            ("col_en_2", "Collect request of {amount} sent to your UPI ID. Click 'Pay/Authorize' and input your 6-digit PIN to accept the credited funds."),
            ("col_en_3", "Buyer on OLX: I initiated payment of {amount}. Open Paytm, accept the reverse collect mandate and submit PIN to receive payment."),
            ("col_en_4", "To complete receiving {amount} from Ramesh Kumar, accept the payment authorization and enter your UPI PIN.")
        ],
        "hi": [
            ("col_hi_1", "मैंने आपको {amount} भेज दिए हैं। गूगल पे पर आई कलेक्ट रिक्वेस्ट स्वीकार करें और अपना यूपीआई पिन डालें ताकि पैसे आपके खाते में आ जाएं।"),
            ("col_hi_2", "पैसे प्राप्त करने के लिए फोनपे पर आई रिक्वेस्ट को स्वीकृत करें और 6 अंकों का यूपीआई पिन दर्ज करें।")
        ],
        "te": [
            ("col_te_1", "నేను మీకు {amount} పంపించాను. మీ PhonePe లో కలెక్ట్ రిక్వెస్ట్ పంపాను, దాన్ని యాక్సెప్ట్ చేసి UPI పిన్ కొడితే డబ్బులు మీ అకౌంట్ లో పడతాయి."),
            ("col_te_2", "డబ్బులు మీ అకౌంట్ లోకి క్రెడిట్ అవ్వాలంటే వచ్చిన రిక్వెస్ట్ ని అప్రూవ్ చేసి మీ సీక్రెట్ పిన్ ఎంటర్ చేయండి.")
        ],
        "hinglish": [
            ("col_hn_1", "Bhai maine {amount} bhej diya hai PhonePe par. Approve collect request par click karke apna UPI PIN enter karo paise mil jayenge."),
            ("col_hn_2", "Aapke account me paise daalne ke liye maine request bheji hai, jaldi se PIN daal do.")
        ],
        "roman_te": [
            ("col_rt_1", "Meeku advance {amount} pampanu. GPay open chesi request accept chesi PIN kottandi ventane dabbulu vastayi."),
            ("col_rt_2", "Dabbulu pondadaniki collect request meeda click chesi UPI PIN enter cheyandi.")
        ]
    },
    "lottery_prize": {
        "en": [
            ("lot_en_1", "KBC Jio Lucky Draw: Congratulations! Your mobile number won 25 Lakh Rupees in KBC all-India lottery. Call Lottery Manager at +91-98765-22110 to claim prize."),
            ("lot_en_2", "You have won 1st prize of Rs. 15,00,000 in Maruti Car Mega Lucky Contest! Pay refundable registration fee of {amount} to bank account: {link}"),
            ("lot_en_3", "CONGRATULATIONS! Your WhatsApp number has won 50 Lakhs in international consumer lottery. Send bank details and claim fee now."),
            ("lot_en_4", "Prize Notification: You are selected for iPhone 16 Pro Giveaway. Click {link} and pay Rs. 99 shipping fee to confirm delivery.")
        ],
        "hi": [
            ("lot_hi_1", "केबीसी जियो लकी ड्रॉ: बधाई हो! आपके मोबाइल नंबर ने 25 लाख रुपये की लॉटरी जीती है। अपने इनाम का दावा करने के लिए तुरंत कॉल करें: +91-98765-88776"),
            ("lot_hi_2", "बधाई! आपके नाम पर 15 लाख का इनाम निकला है। फाइल चार्ज {amount} जमा करके अपनी लॉटरी राशि प्राप्त करें: {link}")
        ],
        "te": [
            ("lot_te_1", "కేబీసీ లక్కీ డ్రా: అభినందనలు! మీ నంబర్‌కు 25 లక్షల రూపాయల బహుమతి వచ్చింది. మేనేజర్‌ను సంప్రదించండి: +91-98765-44332"),
            ("lot_te_2", "మీరు 10 లక్షల రూపాయల కార్ లక్కీ డ్రా గెలుచుకున్నారు! రిజిస్ట్రేషన్ ఫీజు చెల్లించి బహుమతి పొందండి: {link}")
        ],
        "hinglish": [
            ("lot_hn_1", "KBC All India Lucky Draw me aapka 25 Lakh ka lottery laga hai. Prize lene ke liye lottery officer ko WhatsApp kare: +91-98765-55443"),
            ("lot_hn_2", "Aapne jita hai 10 Lakh cash prize. Claim karne ke liye registration fees jama kare: {link}")
        ],
        "roman_te": [
            ("lot_rt_1", "Meeku 25 Lakhs KBC lottery vachindi. Cash transfer cheyadaniki ventane call cheyandi: +91-98765-77665"),
            ("lot_rt_2", "Lucky draw lo car geluchukunnaru. Processing fees pay chesi claim cheyandi: {link}")
        ]
    },
    "fake_customer_support": {
        "en": [
            ("cs_en_1", "Dear user, for your pending refund query on {bank}, please call our official 24x7 toll-free helpline at +91-98765-43210."),
            ("cs_en_2", "Toll Free Support Desk: Facing UPI payment failed error? Connect with our live technical agent at +91-91234-56789 immediately."),
            ("cs_en_3", "Customer Care: To resolve your unauthorized transaction debit of {amount}, call priority grievance desk at +91-98480-11223."),
            ("cs_en_4", "Google Pay Support: Refund disputed. Call toll-free officer at +91-98765-11223 within 30 minutes to reverse funds.")
        ],
        "hi": [
            ("cs_hi_1", "कस्टमर सपोर्ट: कटे हुए पैसे वापस पाने के लिए तुरंत हमारे हेल्पलाइन नंबर +91-98765-01234 पर कॉल करें।"),
            ("cs_hi_2", "बैंक हेल्पडेस्क: अपने खाते से कटी राशि वापस पाने के लिए तुरंत सहायता केंद्र से संपर्क करें।")
        ],
        "te": [
            ("cs_te_1", "సహాయ కేంద్రం: మీ ఖాతా నుండి కట్ అయిన డబ్బును తిరిగి పొందడానికి వెంటనే మా అధికారిక నంబర్‌కు కాల్ చేయండి: +91-98765-11223"),
            ("cs_te_2", "కస్టమర్ కేర్ హెచ్చరిక: మీ లావాదేవీ సమస్యను పరిష్కరించడానికి మా హెల్ప్‌లైన్ సంప్రదించండి.")
        ],
        "hinglish": [
            ("cs_hn_1", "Customer care support: Payment fas gaya hai to abhi customer care officer ko call kare: +91-98123-45678"),
            ("cs_hn_2", "Refund issue solve karne ke liye toll free number par sampark kare: +91-98765-55666")
        ],
        "roman_te": [
            ("cs_rt_1", "Customer support: Cut aina dabbulu venakki ravali ante ventane call cheyandi: +91-99887-76655"),
            ("cs_rt_2", "Mee transaction problem solve cheyadaniki ventane toll free number ki call cheyandi: +91-98765-43333")
        ]
    },
    "remote_access_scam": {
        "en": [
            ("rem_en_1", "Dear user, to resolve your refund error on {bank}, download {app} app from Play Store and share the 9-digit code with our technician."),
            ("rem_en_2", "Toll Free Support Desk: Install {app} on your smartphone and connect screen share with our live technical agent immediately."),
            ("rem_en_3", "Bank Security Alert: Mobile banking requires security certificate. Install {app} tool and read code aloud to customer desk."),
            ("rem_en_4", "Technical Verification: Install {app} and keep screen open to rectify your disputed UPI debit of {amount}.")
        ],
        "hi": [
            ("rem_hi_1", "प्रिय ग्राहक, अपनी रिफंड समस्या के समाधान के लिए प्ले स्टोर से {app} ऐप डाउनलोड करें और हमारे कस्टमर केयर अधिकारी को 9 अंकों का कोड बताएं।"),
            ("rem_hi_2", "कस्टमर सपोर्ट: कटे हुए पैसे वापस पाने के लिए तुरंत {app} इनस्टॉल करें और हमारी तकनीकी टीम से संपर्क करें।")
        ],
        "te": [
            ("rem_te_1", "ప్రియమైన కస్టమర్, మీ రీఫండ్ సమస్య పరిష్కారం కోసం ప్లే స్టోర్ నుండి {app} యాప్‌ను డౌన్‌లోడ్ చేసి, 9 అంకెల కోడ్‌ను మా ఎగ్జిక్యూటివ్‌తో షేర్ చేయండి."),
            ("rem_te_2", "సహాయ కేంద్రం: మీ సమస్యను తనిఖీ చేయడానికి మా అధికారికి {app} యాక్సెస్ ఇవ్వండి.")
        ],
        "hinglish": [
            ("rem_hn_1", "Refund issue solve karne ke liye {app} install kare aur screen share karke support agent ko code bataye."),
            ("rem_hn_2", "Bank helpdesk: Phone me {app} chalu karke code bataiye tabhi paise wapas aayenge.")
        ],
        "roman_te": [
            ("rem_rt_1", "Mee transaction problem solve cheyadaniki ventane {app} install chesi code share cheyandi."),
            ("rem_rt_2", "Cut aina dabbulu venakki ravali ante {app} download chesi screen share cheyandi.")
        ]
    },
    "otp_pin_theft": {
        "en": [
            ("otp_en_1", "Bank Security Verification: Enter your 6-digit UPI PIN and debit card CVV to authenticate identity and stop fraudulent withdrawal: {link}"),
            ("otp_en_2", "Dear customer, your card is used for international purchase of {amount}. If not done by you, immediately share OTP received on SMS with bank manager."),
            ("otp_en_3", "URGENT: Suspicious transaction attempt detected. Enter your NetBanking password and OTP at {link} to freeze your funds safely."),
            ("otp_en_4", "Verification needed: Please tell the 6-digit one-time password (OTP) received on your phone to cancel pending debit order of {amount}.")
        ],
        "hi": [
            ("otp_hi_1", "बैंक सुरक्षा अलर्ट: अपने खाते से फर्जी निकासी रोकने के लिए तुरंत अपना 6 अंकों का यूपीआई पिन और ओटीपी यहां दर्ज करें: {link}"),
            ("otp_hi_2", "सावधान: आपके खाते से {amount} कटने का प्रयास हुआ है। इसे रद्द करने के लिए बैंक अधिकारी को एसएमएस पर आया ओटीपी बताएं।")
        ],
        "te": [
            ("otp_te_1", "బ్యాంక్ భద్రతా హెచ్చరిక: అనధికారిక లావాదేవీని రద్దు చేయడానికి మీ మొబైల్‌కు వచ్చిన 6 అంకెల ఓటీపీ (OTP) మరియు మీ UPI పిన్‌ను నమోదు చేయండి: {link}"),
            ("otp_te_2", "మీ ఖాతా నుండి {amount} డ్రా చేసే ప్రయత్నం జరిగింది. దానిని ఆపడానికి మీ ఓటీపీ నంబర్‌ను వెంటనే మా మేనేజర్‌తో పంచుకోండి.")
        ],
        "hinglish": [
            ("otp_hn_1", "Bank verification: Fraud transaction cancel karne ke liye abhi aaya hua 6 digit OTP bank officer ko share kare."),
            ("otp_hn_2", "Apna account surakshit karne ke liye turant Debit card CVV aur ATM PIN verify kare: {link}")
        ],
        "roman_te": [
            ("otp_rt_1", "Fraud transaction aagadaniki mee mobile ki vachina OTP number ventane cheppandi."),
            ("otp_rt_2", "Account verify cheyadaniki UPI PIN and OTP link lo enter cheyandi: {link}")
        ]
    },
    "fake_govt_scheme": {
        "en": [
            ("gov_en_1", "Government of India announcement: Under {scheme}, all citizens are eligible for direct benefit transfer of Rs. 6,000. Apply now: {link}"),
            ("gov_en_2", "Prime Minister Special Grant: Free smartphone and Rs. 5,000 cash subsidy approved for your ration card. Register within 24 hours at {link}"),
            ("gov_en_3", "Ministry of Finance: Claim your pending welfare subsidy of {amount} under central relief fund. Verify your bank account: {link}"),
            ("gov_en_4", "{scheme} Direct Benefit: Your registration is approved. Pay Rs. 299 processing fee via UPI to release funds: {link}")
        ],
        "hi": [
            ("gov_hi_1", "भारत सरकार घोषणा: {scheme} के तहत सभी नागरिकों के खाते में 6,000 रुपये भेजे जा रहे हैं। तुरंत अपना नाम चेक करें और अप्लाई करें: {link}"),
            ("gov_hi_2", "प्रधानमंत्री राहत कोष: आपके खाते में 5,000 रुपये की आर्थिक सहायता स्वीकृत हुई है। तुरंत रजिस्टर करें: {link}")
        ],
        "te": [
            ("gov_te_1", "భారత ప్రభుత్వం పథకం: {scheme} కింద అర్హులైన ప్రతి ఒక్కరికీ రూ. 6,000 నేరుగా బ్యాంక్ ఖాతాలో జమ చేయబడుతుంది. వెంటనే దరఖాస్తు చేసుకోండి: {link}"),
            ("gov_te_2", "ప్రభుత్వ సహాయ నిధి: మీ రేషన్ కార్డుపై రూ. 5,000 నగదు సాయం మంజూరైంది. ఈ లింక్‌లో రిజిస్టర్ చేసుకోండి: {link}")
        ],
        "hinglish": [
            ("gov_hn_1", "Govt of India update: {scheme} ke tahat har nagrik ko Rs. 6,000 mil rahe hain. Abhi apna form bhare: {link}"),
            ("gov_hn_2", "PM Yojana: Sabhi ration card holders ko 5,000 rupaye ki sahayata rashi mil rahi hai. Apply kare: {link}")
        ],
        "roman_te": [
            ("gov_rt_1", "Govt Scheme: {scheme} kinda direct ga Rs. 6,000 mee account lo padathayi. Ventane apply cheyandi: {link}"),
            ("gov_rt_2", "Free cash subsidy apply cheyadaniki ee link open chesi bank details fill cheyandi: {link}")
        ]
    },
    "job_investment_scam": {
        "en": [
            ("job_en_1", "Part-time job offer: Earn Rs. 3,000 to Rs. 8,000 daily from home just by liking YouTube videos and rating hotels on Google Maps! Join Telegram: {link}"),
            ("job_en_2", "Amazon Hiring: Work from home product reviewer needed. Daily payout {amount} directly via UPI. Message HR on WhatsApp: +91-98765-43210."),
            ("job_en_3", "Crypto Wealth VIP Group: Guaranteed 300% returns in 24 hours! Invest Rs. 5,000 and get Rs. 20,000 guaranteed payout. Sign up: {link}"),
            ("job_en_4", "Stock Market Trading Robot: AI bot generates 50% daily profits on Telegram. Deposit Rs. 2,000 to start trading today: {link}")
        ],
        "hi": [
            ("job_hi_1", "घर बैठे पार्ट-टाइम काम करके रोजाना 2,000 से 5,000 रुपये कमाएं! केवल यूट्यूब वीडियो लाइक करें और तुरंत यूपीआई से पेमेंट पाएं: {link}"),
            ("job_hi_2", "क्रिप्टो और शेयर मार्केट में निवेश करें और 1 दिन में 4 गुना मुनाफा कमाएं! 100% गारंटीड रिटर्न। तुरंत जुड़ें।")
        ],
        "te": [
            ("job_te_1", "ఇంట్లోనే కూర్చుని రోజూ రూ. 3,000 నుండి రూ. 7,000 వరకు సంపాదించండి! యూట్యూబ్ వీడియోలను లైక్ చేయడం మాత్రమే పని. సంప్రదించండి: +91-98765-11223"),
            ("job_te_2", "రోజుకు 5,000 సంపాదించే సువర్ణావకాశం! ఎలాంటి పెట్టుబడి లేకుండా కేవలం గూగుల్ రేటింగ్స్ ఇవ్వండి.")
        ],
        "hinglish": [
            ("job_hn_1", "Part time online job: Daily 3000-5000 income just by doing simple review tasks. WhatsApp on +91-98123-45678 to start earning today."),
            ("job_hn_2", "Daily task complete karke 4000 kamao. Pehle 1000 deposit karke VIP member bano: {link}")
        ],
        "roman_te": [
            ("job_rt_1", "Work from home job: Daily Rs 4000 salary UPI dwara vasthundi. Simple hotel rating tasks cheyali. WhatsApp cheyandi: +91-99887-76655"),
            ("job_rt_2", "Telegram task job: Prati roju Rs 3500 earning. Ventane group lo join avvandi: {link}")
        ]
    },
    "loan_app_extortion": {
        "en": [
            ("loan_en_1", "URGENT NOTICE: You failed to repay instant loan of {amount}. Recovery agents dispatched to your residential address and your contact list will be shared on social media if not cleared by 2 PM!"),
            ("loan_en_2", "Loan Defaulter Alert: We have access to your phone contacts and gallery. We will send defaming morphed photos to your family unless you transfer {amount} immediately to UPI."),
            ("loan_en_3", "Instant Cash Loan approved! Rs. 50,000 credited in 5 minutes with 0 CIBIL score. Download cash loan APK now: {link}"),
            ("loan_en_4", "Final ultimatum: Pay loan dues of {amount} within 1 hour or we will upload your Aadhaar and contact book to public blacklists.")
        ],
        "hi": [
            ("loan_hi_1", "अंतिम चेतावनी: आपने अपना लोन नहीं चुकाया है। यदि आज दोपहर तक {amount} जमा नहीं किए तो आपकी मॉर्फ की गई तस्वीरें सभी संपर्कों को भेज दी जाएंगी!"),
            ("loan_hi_2", "लोन रिकवरी नोटिस: पुलिस केस दर्ज हो चुका है। गिरफ्तारी से बचने के लिए तुरंत दिए गए यूपीआई पर भुगतान करें।")
        ],
        "te": [
            ("loan_te_1", "అత్యవసర హెచ్చరిక: మీరు తీసుకున్న ఇన్‌స్టాంట్ లోన్ వెంటనే చెల్లించకపోతే మీ కాంటాక్ట్స్ మరియు ఫోటోలను బంధువులకు పంపుతాము! వెంటనే చెల్లించండి: {amount}"),
            ("loan_te_2", "మీపై చట్టపరమైన చర్యలు తీసుకోబడుతున్నాయి. పోలీస్ అరెస్ట్ కాకుండా ఉండాలంటే వెంటనే {amount} చెల్లించండి.")
        ],
        "hinglish": [
            ("loan_hn_1", "Aakhri warning: Loan ka paisa turant wapas karo nahi to tumhare saare contacts ko tumhari photo bhej denge aur police case karenge."),
            ("loan_hn_2", "Turant loan bhugtan kare varna aapke ghar par recovery team aayegi: {link}")
        ],
        "roman_te": [
            ("loan_rt_1", "Mee loan dues ventane kattakapothe mee photo contacts andariki pampinchi badnaam chestam. 2 hours lo UPI transfer cheyandi."),
            ("loan_rt_2", "Loan dabbulu ventane kattandi lekapothe mee family members ki call chesi insult chestamu.")
        ]
    },
    "courier_customs_scam": {
        "en": [
            ("cour_en_1", "{courier} Alert: Your parcel sent from Mumbai to Taiwan intercepted by Customs and NCB. Contains 5 passports and contraband. Digital arrest warrant issued. Contact Cyber Crime officer on Skype."),
            ("cour_en_2", "{courier} Courier Notice: Your package containing international contraband held at Airport Customs. FIR registered. Connect with DCP Crime Branch immediately on video call."),
            ("cour_en_3", "India Post Delivery Alert: Your speed post parcel address is incomplete. Update residential address and pay Rs. 48 redelivery fee: {link}"),
            ("cour_en_4", "DHL Express: Parcel on hold due to unpaid customs clearance duty of {amount}. Pay online within 24 hours at {link} to avoid seizure.")
        ],
        "hi": [
            ("cour_hi_1", "{courier} अलर्ट: आपके नाम पर भेजा गया पार्सल सीमा शुल्क और नारकोटिक्स द्वारा पकड़ा गया है। इसमें नशीली दवाएं हैं। तुरंत पुलिस अधिकारी से वीडियो कॉल पर जुड़ें।"),
            ("cour_hi_2", "भारतीय डाक सूचना: आपका पार्सल पता अधूरा होने के कारण रोक दिया गया है। 48 रुपये का पुनः वितरण शुल्क देकर पता अपडेट करें: {link}")
        ],
        "te": [
            ("cour_te_1", "{courier} హెచ్చరిక: మీ పేరుతో ఉన్న కొరియర్ పార్సెల్ లో డ్రగ్స్ ఉన్నట్లు కస్టమ్స్ అధికారులు గుర్తించారు. మీపై ఎఫ్‌ఐఆర్ నమోదైంది. వెంటనే విచారణ అధికారికి కాల్ చేయండి."),
            ("cour_te_2", "ఇండియా పోస్ట్: మీ పార్సెల్ చిరునామా సరిగ్గా లేనందున నిలిపివేయబడింది. ఈ లింక్‌లో చిరునామా అప్‌డేట్ చేసి రూ. 35 చెల్లించండి: {link}")
        ],
        "hinglish": [
            ("cour_hn_1", "Customs department notice: Aapka courier parcel seize ho gaya hai jisme illegal items mile hain. Arrest se bachne ke liye turant DCP crime branch ko call kare."),
            ("cour_hn_2", "India Post alert: Delivery address galat hai, parcel wapas chala jayega. Address update kare: {link}")
        ],
        "roman_te": [
            ("cour_rt_1", "Mee peru meeda unna parcel lo illegal drugs dorikayi. CBI arrest cheyabothondi. Ventane police officer tho video call lo matladandi."),
            ("cour_rt_2", "Customs duty kattakapothe parcel confiscate chesi case pedataru. Ee link lo duty pay cheyandi: {link}")
        ]
    },
    "marketplace_qr_scam": {
        "en": [
            ("mkt_en_1", "I want to buy your item on OLX. I am sending you a payment QR code. Scan this QR code in Google Pay and enter your UPI PIN to receive {amount} into your account!"),
            ("mkt_en_2", "Buyer on Quikr: I have scanned your item and generated a merchant receiver QR code. Scan it from your gallery and put your UPI PIN to get credited instantly."),
            ("mkt_en_3", "Facebook Marketplace payment: Buyer generated receiving barcode. Scan QR code and authorize payment PIN to claim {amount}."),
            ("mkt_en_4", "Used car token advance: Scan attached dynamic UPI QR code on Paytm and authenticate with your 6-digit PIN to accept deposit.")
        ],
        "hi": [
            ("mkt_hi_1", "मैं आपका सोफा ओएलएक्स पर खरीदना चाहता हूं। मैंने भुगतान के लिए एक क्यूआर कोड भेजा है। इसे फोनपे से स्कैन करें और अपना यूपीआई पिन डालें ताकि {amount} आपके खाते में आ जाएं।"),
            ("mkt_hi_2", "क्यूआर कोड स्कैन करके अपना यूपीआई पिन डालें और {amount} का एडवांस पेमेंट तुरंत अपने खाते में पाएं।")
        ],
        "te": [
            ("mkt_te_1", "నేను మీ వస్తువు కొంటాను. డబ్బులు పంపడానికి QR కోడ్ పంపాను. దీన్ని Google Pay లో స్కాన్ చేసి మీ UPI పిన్ కొడితే డబ్బులు మీ అకౌంట్ లో పడతాయి."),
            ("mkt_te_2", "ఈ క్యూఆర్ కోడ్ స్కాన్ చేసి మీ పిన్ ఎంటర్ చేయండి, వెంటనే {amount} మీ ఖాతాకు జమ అవుతాయి.")
        ],
        "hinglish": [
            ("mkt_hn_1", "OLX par jo saman dala hai uska payment lene ke liye ye QR code scan karo aur PIN enter karo paise turant credit ho jayenge."),
            ("mkt_hn_2", "Bhai QR code scan karke PIN daal do advance payment {amount} turant mil jayega.")
        ],
        "roman_te": [
            ("mkt_rt_1", "Advance payment kosam ee QR code scan chesi UPI PIN kottandi, direct ga bank account lo add aipotundi."),
            ("mkt_rt_2", "Payment recieve cheyadaniki ee QR code scan chesi PIN enter cheyandi.")
        ]
    },
    "accidental_transfer_scam": {
        "en": [
            ("acc_en_1", "Hello sir, by mistake I sent {amount} to your Google Pay number instead of my brother's medical fee. I am a poor student, please please return the money via UPI to my number +91-98765-43210 immediately!"),
            ("acc_en_2", "Sir urgent help! My father accidentally transferred {amount} to your UPI ID via PhonePe. Please reverse it back immediately to rahul@oksbi or my father will have a heart attack!"),
            ("acc_en_3", "Accidental transfer: {amount} sent to wrong UPI handle. Please initiate return transfer to avoid legal freeze on your account."),
            ("acc_en_4", "Sir I sent money by mistake, please check message and transfer back {amount} immediately to my PhonePe.")
        ],
        "hi": [
            ("acc_hi_1", "नमस्ते भाई साहब, गलती से मेरी बहन की कॉलेज फीस के {amount} आपके यूपीआई नंबर पर चले गए हैं। कृपया दया करके इसे तुरंत इस नंबर पर वापस भेज दीजिए।"),
            ("acc_hi_2", "सर गलती से {amount} आपके खाते में चले गए हैं, भगवान के नाम पर तुरंत वापस कर दीजिए वरना पुलिस में शिकायत करनी पड़ेगी।")
        ],
        "te": [
            ("acc_te_1", "నమస్కారం సార్, పొరపాటున నా భార్య హాస్పిటల్ ఖర్చుల కోసం {amount} మీ UPI కి పంపించాను. దయచేసి ఆ డబ్బును వెంటనే తిరిగి నా నంబర్‌కు పంపించండి సార్!"),
            ("acc_te_2", "పొరపాటున ట్రాన్స్‌ఫర్ అయిన {amount} వెంటనే తిరిగి పంపండి, లేకపోతే సైబర్ క్రైమ్ పోలీసులకు ఫిర్యాదు చేస్తాము.")
        ],
        "hinglish": [
            ("acc_hn_1", "Bhai galti se {amount} aapke account me transfer ho gaye hain. Hospital emergency hai, please turant wapas phonepe kar dijiye."),
            ("acc_hn_2", "Mera paisa galti se aapke account me gaya hai, turant wapas bhejo varna account block karwa dunga.")
        ],
        "roman_te": [
            ("acc_rt_1", "Sir mistake ga {amount} mee number ki pampanu. Urgent ga doctor ki kattali, please aa amount na UPI ki return cheyandi."),
            ("acc_rt_2", "Wrong number ki {amount} vachindi mee account ki, ventane return kottandi sir please.")
        ]
    },
    "legitimate": {
        "en": [
            ("leg_en_1", "{bank}: An amount of {amount} is debited from account ending 4821 on 21-Nov-2026 for UPI/Swiggy. Bal: Rs. 24,190.00. NEVER share your OTP or PIN with anyone."),
            ("leg_en_2", "{bank} Security Alert: OTP for login to Internet Banking is 482910. Valid for 10 minutes. Do NOT share OTP or password with anyone, including bank employees."),
            ("leg_en_3", "Dear Consumer, your {board} electricity bill for account 1092837 is {amount}. Due date is 28-Nov-2026. Pay safely at official portal or electricity office."),
            ("leg_en_4", "Your Amazon order #402-9182736 has been shipped and will be delivered by tomorrow. Track your package in the official Amazon app."),
            ("leg_en_5", "{bank}: {amount} credited to your account ending 9102 via UPI from Priya Sharma. Updated balance Rs. 38,400.00."),
            ("leg_en_6", "Dear Customer, your monthly telecom postpaid bill of Rs. 649 is generated. Pay via official MyAirtel / MyJio app before due date."),
            ("leg_en_7", "{bank}: You have requested password reset. Your verification code is 918204. Bank never asks for OTP or CVV over call or SMS."),
            ("leg_en_8", "Transaction successful: {amount} paid to Metro Rail via UPI. Ref No: 492019284719. Save paper, travel smart."),
            ("leg_en_9", "{bank}: Your credit card statement for October is ready. Total due: {amount}. View securely in {bank} Mobile app."),
            ("leg_en_10", "Airtel: Your postpaid bill of {amount} is generated. Pay before due date to avoid late fee on Airtel Thanks app."),
            ("leg_en_11", "Jio Alert: Your monthly recharge of {amount} is successful. Enjoy high-speed data and unlimited calls."),
            ("leg_en_12", "Your delivery for order #402-1928374 is out for delivery. Share OTP ONLY upon physical receipt of package."),
            ("leg_en_13", "Canara Bank: OTP to confirm payment of {amount} is 620194. Do not disclose OTP/CVV to anyone. Bank never asks for confidential details."),
            ("leg_en_14", "Kotak Bank: {amount} debited from a/c **1122 for UPI payment. If not done by you, forward SMS to 9971056767 to block card."),
            ("leg_en_15", "Hey bro, can you Google Pay me Rs 350 for last night dinner?"),
            ("leg_en_16", "I sent {amount} to your UPI id rahul@okhdfcbank, please check and confirm."),
            ("leg_en_17", "Zomato: Your order from Biryani Blues is delivered! Rate your delivery partner Sunil."),
            ("leg_en_18", "EPFO: Your monthly PF contribution of {amount} has been credited for member ID ending 4829.")
        ],
        "hi": [
            ("leg_hi_1", "{bank}: आपके खाते से {amount} की राशि यूपीआई द्वारा काटी गई है। शेष राशि 18,500 रुपये है। अपना ओटीपी या पिन किसी से साझा न करें। बैंक कभी भी ओटीपी नहीं मांगता।"),
            ("leg_hi_2", "{bank}: इंटरनेट बैंकिंग लॉगिन के लिए आपका ओटीपी 394812 है। यह 5 मिनट के लिए वैध है। इसे किसी को न बताएं।"),
            ("leg_hi_3", "प्रिय उपभोक्ता, आपका बिजली बिल {amount} नियत तिथि 25 तारीख तक देय है। आधिकारिक केंद्र पर सुरक्षित भुगतान करें।")
        ],
        "te": [
            ("leg_te_1", "{bank}: మీ ఖాతా నుండి {amount} UPI ద్వారా చెల్లించబడింది. మిగిలిన బ్యాలెన్స్ రూ. 15,300. మీ OTP లేదా PIN ఎవరితోనూ పంచుకోవద్దు. బ్యాంక్ ఎప్పుడూ OTP అడగదు."),
            ("leg_te_2", "{bank}: లాగిన్ కోసం మీ OTP 582910. 10 నిమిషాలు మాత్రమే చెల్లుతుంది. దీనిని ఎవరికీ చెప్పవద్దు."),
            ("leg_te_3", "మీ విద్యుత్ బిల్లు {amount} చెల్లించడానికి ఆఖరి తేదీ 28వ తేదీ. అధికారిక కార్యాలయం లేదా వెబ్‌సైట్ ద్వారా సురక్షితంగా చెల్లించండి.")
        ],
        "hinglish": [
            ("leg_hn_1", "{bank}: {amount} debited from your A/C via UPI. Balance Rs 12,400. Kabhi bhi apna OTP, UPI PIN kisi ko share na kare. Bank never calls for PIN."),
            ("leg_hn_2", "Aapka OTP 849201 hai. Yeh kisi ke saath share na kare, bank staff ke sath bhi nahi.")
        ],
        "roman_te": [
            ("leg_rt_1", "{bank}: {amount} UPI dwara transfer cheyabadindi. Balance Rs 9,800. Mee OTP and PIN eppudu evaritho share cheyavoddu."),
            ("leg_rt_2", "Internet banking login kosam mee OTP 749201. Evariki cheppavaddu. Bank eppudu call chesi PIN adagadu.")
        ]
    }
}

def generate_synthetic_samples(target_per_cat: int = 700) -> List[Dict[str, Any]]:
    samples = []
    
    for cat, lang_dict in RAW_TEMPLATE_DEFS.items():
        all_templates = []
        for lang, t_list in lang_dict.items():
            for t_id, t_text in t_list:
                all_templates.append((t_id, lang, t_text))

        count_generated = 0
        while count_generated < target_per_cat:
            t_id, lang, template = random.choice(all_templates)
            bank = random.choice(BANKS)
            board = random.choice(POWER_BOARDS)
            scheme = random.choice(GOVT_SCHEMES)
            app = random.choice(REMOTE_APPS)
            courier = random.choice(COURIER_BRANDS)
            amount = random.choice(AMOUNTS)
            time_str = random.choice(TIMES)
            link = get_fake_link()

            text = template.format(
                bank=bank,
                board=board,
                scheme=scheme,
                app=app,
                courier=courier,
                amount=amount,
                time=time_str,
                link=link
            )

            # Apply realistic adversarial variations
            text = inject_noise(text)

            samples.append({
                "template_id": t_id,
                "text": text,
                "category": cat,
                "language": "hi" if lang == "hinglish" else ("te" if lang == "roman_te" else lang),
                "script_style": lang,
                "is_scam": 0 if cat == "legitimate" else 1,
                "source": "synthetic_generator"
            })
            count_generated += 1

    return samples

def load_real_uci_sms() -> List[Dict[str, Any]]:
    """Loads real SMS messages from UCI SMS collection as additional grounded data."""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "external", "sms_spam_collection.csv")
    if not os.path.exists(csv_path):
        return []

    try:
        df = pd.read_csv(csv_path)
        real_samples = []
        for idx, row in df.iterrows():
            lbl = str(row["label"]).lower()
            txt = str(row["text"]).strip()
            if not txt or len(txt) < 10:
                continue

            # Ham -> legitimate
            if lbl == "ham":
                real_samples.append({
                    "template_id": f"uci_ham_{idx}",
                    "text": txt,
                    "category": "legitimate",
                    "language": "en",
                    "script_style": "en",
                    "is_scam": 0,
                    "source": "uci_sms_collection"
                })
            elif lbl == "spam":
                # General spam/lottery/prize
                cat = "lottery_prize" if any(w in txt.lower() for w in ["won", "prize", "claim", "cash", "award"]) else "fake_customer_support"
                real_samples.append({
                    "template_id": f"uci_spam_{idx}",
                    "text": txt,
                    "category": cat,
                    "language": "en",
                    "script_style": "en",
                    "is_scam": 1,
                    "source": "uci_sms_collection"
                })
        return real_samples
    except Exception as e:
        print(f"[Warning] Could not load UCI SMS collection: {e}")
        return []

def main():
    random.seed(42)
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "synthetic_scam_dataset.csv")

    print("Generating comprehensive 15-category synthetic dataset (target: 10,500+)...")
    synthetic = generate_synthetic_samples(target_per_cat=720) # 15 * 720 = 10,800
    print(f"Generated {len(synthetic)} synthetic samples.")

    print("Loading real public SMS dataset (UCI SMS Spam)...")
    real_data = load_real_uci_sms()
    # Sample up to 2,000 ham messages from UCI to prevent huge class imbalance while retaining natural diversity
    if real_data:
        ham_samples = [s for s in real_data if s["category"] == "legitimate"]
        spam_samples = [s for s in real_data if s["category"] != "legitimate"]
        sampled_ham = random.sample(ham_samples, min(1500, len(ham_samples)))
        sampled_spam = random.sample(spam_samples, min(500, len(spam_samples)))
        combined_real = sampled_ham + sampled_spam
        print(f"Adding {len(combined_real)} real public SMS samples ({len(sampled_ham)} legitimate, {len(sampled_spam)} spam).")
        all_samples = synthetic + combined_real
    else:
        all_samples = synthetic

    df = pd.DataFrame(all_samples)
    # Shuffle
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    df.to_csv(out_path, index=False, encoding="utf-8")

    print(f"\nSuccessfully created dataset with {len(df)} rows at {out_path}")
    print("\nCategory breakdown:")
    print(df["category"].value_counts())
    print("\nSource breakdown:")
    print(df["source"].value_counts())
    print("\nLanguage breakdown:")
    print(df["script_style"].value_counts())

if __name__ == "__main__":
    main()
