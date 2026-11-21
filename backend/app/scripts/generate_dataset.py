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
        pos = random.randint(5, max(6, len(text) - 5))
        text = text[:pos] + "\u200B" + text[pos:]
    return text

def get_fake_link():
    if random.random() < 0.4:
        return f"http://{random.choice(SHORTENERS)}"
    return f"http://{random.choice(FAKE_DOMAINS)}/auth?ref={random.randint(1000, 9999)}"

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
            ("kyc_te_2", "హెచ్చరిక: మీ బ్యాంక్ ఖాతా సేవలు నిలిపివేయబడ్డాయి. పాన్ కార్డు లింక్ చేయడానికి వెంటనే ఈ లింక్ క్లిక్ చేయండి: {link}"),
            ("kyc_te_3", "మీ నెట్ బ్యాంకింగ్ పాస్‌వర్డ్ గడువు ముగిసింది. ఖాతా శాశ్వతంగా మూసివేయబడకుండా ఉండటానికి ఇప్పుడే కేవైసీ చేయండి: {link}")
        ],
        "hinglish": [
            ("kyc_hn_1", "Dear customer, aapka {bank} account {time} block kar diya jayega pending KYC ke karan. Turant update kare: {link}"),
            ("kyc_hn_2", "Aapke bank a/c me PAN update nahi hai. Branch jane ki jarurat nahi, is link par video kyc kare: {link}")
        ],
        "roman_te": [
            ("kyc_rt_1", "Mee {bank} account KYC pending undi. Ee roju night lo block aipotundi. Ventane ee link open chesi Aadhaar update cheyandi: {link}"),
            ("kyc_rt_2", "Mee debit card temporary freeze aindi. Unfreeze cheyadaniki link click chesi details fill cheyandi: {link}")
        ]
    },
    "electricity_disconnection": {
        "en": [
            ("elec_en_1", "Dear Consumer, your electricity power will be DISCONNECTED {time} from sub-station because your previous month bill was not updated. Contact electricity officer immediately at +91-98765-43210 or pay: {link}"),
            ("elec_en_2", "{board} Alert: Bill payment of {amount} is overdue. Physical disconnection order is issued for {time}. Call Power Executive at +91-91234-56789 or settle bill: {link}"),
            ("elec_en_3", "POWER CUT NOTICE: Your electricity connection CA-890214 will be severed {time}. Immediately verify receipt at {link} to stop field linesman."),
            ("elec_en_4", "Urgent notice from {board} office: Your electric meter is scheduled for removal {time}. Contact junior engineer immediately or pay online: {link}")
        ],
        "hi": [
            ("elec_hi_1", "प्रिय उपभोक्ता, आपके बिजली का बिल अपडेट नहीं होने के कारण {time} बिजली काट दी जाएगी। तुरंत हमारे बिजली अधिकारी से संपर्क करें: +91-98765-11223 या भुगतान करें: {link}"),
            ("elec_hi_2", "बिजली विभाग सूचना: आपका कनेक्शन {time} काट दिया जाएगा। लाइनमैन को रोकने के लिए तुरंत इस लिंक पर बिल भरें: {link}")
        ],
        "te": [
            ("elec_te_1", "ప్రియమైన వినియోగదారుడా, మీ విద్యుత్ బిల్లు అప్‌డేట్ కానందున {time} కరెంట్ కట్ చేయబడుతుంది. లైన్‌మ్యాన్ ఆపడానికి వెంటనే కాల్ చేయండి: +91-98765-99887 లేదా చెల్లించండి: {link}"),
            ("elec_te_2", "కరెంట్ బిల్లు చెల్లించలేదని మీ విద్యుత్ సరఫరా నిలిపివేయబడుతుంది. వెంటనే ఈ లింక్ ద్వారా బిల్లు చెల్లించండి: {link}")
        ],
        "hinglish": [
            ("elec_hn_1", "Dear consumer, aapka bijli bill update nahi hua hai isliye {time} bijli cut jayegi. Lineman rokne ke liye turant call kare: +91-98123-45678 ya link par pay kare: {link}"),
            ("elec_hn_2", "Bijli vibhag notice: Meter disconnect order pass ho gaya hai. Turant contact kare officer se: {link}")
        ],
        "roman_te": [
            ("elec_rt_1", "Mee current bill kattaledu kabatti {time} current cut chestharu. Ventane ee number ki call cheyandi: +91-99887-76655 lekapothe link lo pay cheyandi: {link}"),
            ("elec_rt_2", "Current meter remove chestam ani notice vachindi. Officer tho matladi bill settle cheyandi: {link}")
        ]
    },
    "fake_upi_refund_cashback": {
        "en": [
            ("ref_en_1", "Congratulations! You have won an unclaimed scratch card reward of {amount} on PhonePe. Click here to credit to your bank account: {link}"),
            ("ref_en_2", "Google Pay Reward Alert: Your cashback of {amount} is waiting in your rewards bucket. Claim directly to your primary bank: {link}"),
            ("ref_en_3", "Refund Approved: Your failed transaction refund of {amount} has been processed by NPCI. Click {link} to receive money in your UPI wallet."),
            ("ref_en_4", "You have a pending cashback of {amount} from Paytm festival bonanza. Click link to transfer instantly: {link}")
        ],
        "hi": [
            ("ref_hi_1", "बधाई हो! आपको फोनपे पर {amount} का कैशबैक रिवॉर्ड मिला है। सीधे अपने बैंक खाते में प्राप्त करने के लिए यहां क्लिक करें: {link}"),
            ("ref_hi_2", "गूगल पे कैशबैक: आपका {amount} का रिफंड तैयार है। अभी क्लेम करें और अपने खाते में पाएं: {link}")
        ],
        "te": [
            ("ref_te_1", "అభినందనలు! మీకు PhonePe లో {amount} క్యాష్‌బ్యాక్ బహుమతి లభించింది. మీ బ్యాంక్ ఖాతాకు జమ చేసుకోవడానికి ఇక్కడ క్లిక్ చేయండి: {link}"),
            ("ref_te_2", "గూగుల్ పే ఆఫర్: మీ {amount} రీఫండ్ సిద్ధంగా ఉంది. క్లెయిమ్ చేసుకోవడానికి వెంటనే లింక్ ఓపెన్ చేయండి: {link}")
        ],
        "hinglish": [
            ("ref_hn_1", "Badhai ho! Aapko Google Pay par {amount} ka reward mila hai. Apne bank account me transfer karne ke liye link par jaye: {link}"),
            ("ref_hn_2", "Aapka pending UPI cashback {amount} release ho gaya hai. Abhi claim kare: {link}")
        ],
        "roman_te": [
            ("ref_rt_1", "Meeku PhonePe lo {amount} scratch card reward vachindi. Direct ga bank account lo credit chesukondi: {link}"),
            ("ref_rt_2", "Cashback claim cheyadaniki ee link open chesi UPI details confirm cheyandi: {link}")
        ]
    },
    "collect_request_fraud": {
        "en": [
            ("col_en_1", "I have initiated payment of {amount} to your Google Pay. Please open your UPI app, click 'Pay' on the collect request and enter your secret UPI PIN to receive money!"),
            ("col_en_2", "PhonePe Collect Notice: You received a collect request for {amount} from buyer. Accept and enter your 6-digit MPIN to deposit amount into your savings account."),
            ("col_en_3", "To receive your advance payment of {amount}, authorize the pending collect request on BHIM app by entering your UPI PIN."),
            ("col_en_4", "Payment Credit Trick: Enter your secret UPI PIN to receive {amount} refund directly to your debit card.")
        ],
        "hi": [
            ("col_hi_1", "मैंने आपको {amount} भेज दिए हैं। अपना फोनपे खोलें, कलेक्ट रिक्वेस्ट पर क्लिक करें और पैसे प्राप्त करने के लिए अपना यूपीआई पिन डालें!"),
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
            ("lot_en_4", "Prize Notification: You are selected for iPhone 16 Pro Giveaway. Click {link} and pay Rs. 99 shipping fee to confirm delivery."),
            ("lot_en_5", "Dubai Gold Souk Mega Raffle: 100g Gold Bar winner is your mobile number. Pay customs duty tax Rs 8,500 to dispatch gold bar: {link}"),
            ("lot_en_6", "Amazon Festive Bonanza: You won Tata Safari Car in Diwali lucky draw. Contact WhatsApp manager +91-9820194821 to pay RTO registration fee.")
        ],
        "hi": [
            ("lot_hi_1", "केबीसी जियो लकी ड्रॉ: बधाई हो! आपके मोबाइल नंबर ने 25 लाख रुपये की लॉटरी जीती है। अपने इनाम का दावा करने के लिए तुरंत कॉल करें: +91-98765-88776"),
            ("lot_hi_2", "बधाई! आपके नाम पर 15 लाख का इनाम निकला है। फाइल चार्ज {amount} जमा करके अपनी लॉटरी राशि प्राप्त करें: {link}"),
            ("lot_hi_3", "अमेज़न लकी ड्रॉ में आपको महिंद्रा थार गाड़ी मिली है। आरटीओ टैक्स और इंश्योरेंस फीस 14,500 जमा करें: {link}")
        ],
        "te": [
            ("lot_te_1", "కేబీసీ లక్కీ డ్రా: అభినందనలు! మీ నంబర్‌కు 25 లక్షల రూపాయల బహుమతి వచ్చింది. మేనేజర్‌ను సంప్రదించండి: +91-98765-44332"),
            ("lot_te_2", "మీరు 10 లక్షల రూపాయల కార్ లక్కీ డ్రా గెలుచుకున్నారు! రిజిస్ట్రేషన్ ఫీజు చెల్లించి బహుమతి పొందండి: {link}"),
            ("lot_te_3", "రిలయన్స్ జియో బంపర్ లక్కీ డ్రా లో మీకు రూ. 15 లక్షల నగదు బహుమతి వచ్చింది. టాక్స్ ఫీజు చెల్లించి క్లెయిమ్ చేసుకోండి: {link}")
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
            ("cs_en_4", "Google Pay Support: Refund disputed. Call toll-free officer at +91-98765-11223 within 30 minutes to reverse funds."),
            ("cs_en_5", "PhonePe Nodal Helpdesk: If your Rs 5,000 transfer failed, contact our helpline 08920194821 to generate instant reversal ticket."),
            ("cs_en_6", "Paytm Wallet Customer Care: Wallet suspended. Call support executive on +91-9012938472 to verify debit card and unblock.")
        ],
        "hi": [
            ("cs_hi_1", "कस्टमर सपोर्ट: कटे हुए पैसे वापस पाने के लिए तुरंत हमारे हेल्पलाइन नंबर +91-98765-01234 पर कॉल करें।"),
            ("cs_hi_2", "बैंक हेल्पडेस्क: अपने खाते से कटी राशि वापस पाने के लिए तुरंत सहायता केंद्र से संपर्क करें: +91-9820194821"),
            ("cs_hi_3", "फोनपे सहायता केंद्र: ट्रांजैक्शन फेल होने पर तुरंत रिफंड पाने के लिए कस्टमर केयर अधिकारी 09128374821 पर कॉल करें।")
        ],
        "te": [
            ("cs_te_1", "సహాయ కేంద్రం: మీ ఖాతా నుండి కట్ అయిన డబ్బును తిరిగి పొందడానికి వెంటనే మా అధికారిక నంబర్‌కు కాల్ చేయండి: +91-98765-11223"),
            ("cs_te_2", "కస్టమర్ కేర్ హెచ్చరిక: మీ లావాదేవీ సమస్యను పరిష్కరించడానికి మా హెల్ప్‌లైన్ సంప్రదించండి: 8920194821"),
            ("cs_te_3", "పేటీఎం కస్టమర్ సపోర్ట్: మీ ఫెయిల్ అయిన ట్రాన్సాక్షన్ రిఫండ్ కోసం వెంటనే ఎగ్జిక్యూటివ్ నెంబర్ 9849201920 కు కాల్ చేయండి.")
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
            ("rem_en_4", "Technical Verification: Install {app} and keep screen open to rectify your disputed UPI debit of {amount}."),
            ("rem_en_5", "Electricity bill update error: Install {app} on your phone to allow power department engineer to inspect transaction logs.")
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
            ("otp_en_4", "Verification needed: Please tell the 6-digit one-time password (OTP) received on your phone to cancel pending debit order of {amount}."),
            ("otp_en_5", "Reward point redemption: Tell OTP to executive to credit Rs 9,500 cash into your bank account.")
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
            ("loan_en_2", "Loan Defaulter Alert: We have access to your phone contacts and gallery. We will send defaming morphed photos to your family unless you transfer {amount} immediately to UPI: recovery@ybl"),
            ("loan_en_3", "Instant Cash Loan approved! Rs. 50,000 credited in 5 minutes with 0 CIBIL score. Download cash loan APK now: {link}"),
            ("loan_en_4", "Final ultimatum: Pay loan dues of {amount} within 1 hour or we will upload your Aadhaar and contact book to public blacklists and call your relatives."),
            ("loan_en_5", "Legal police summons: Non payment of loan #LN90184. Pay settlement amount of {amount} now at {link} to stop warrant execution.")
        ],
        "hi": [
            ("loan_hi_1", "अंतिम चेतावनी: आपने अपना लोन नहीं चुकाया है। यदि आज दोपहर तक {amount} जमा नहीं किए तो आपकी मॉर्फ की गई तस्वीरें सभी संपर्कों को भेज दी जाएंगी!"),
            ("loan_hi_2", "लोन रिकवरी नोटिस: पुलिस केस दर्ज हो चुका है। गिरफ्तारी से बचने के लिए तुरंत दिए गए यूपीआई पर भुगतान करें।"),
            ("loan_hi_3", "तेरे सारे कांटेक्ट नंबर हमारे पास हैं। तुरंत {amount} यूपीआई पर डाल वरना तेरी बहन को कॉल करके बदनाम करेंगे।")
        ],
        "te": [
            ("loan_te_1", "అత్యవసర హెచ్చరిక: మీరు తీసుకున్న ఇన్‌స్టాంట్ లోన్ వెంటనే చెల్లించకపోతే మీ కాంటాక్ట్స్ మరియు ఫోటోలను బంధువులకు పంపుతాము! వెంటనే చెల్లించండి: {amount}"),
            ("loan_te_2", "మీపై చట్టపరమైన చర్యలు తీసుకోబడుతున్నాయి. పోలీస్ అరెస్ట్ కాకుండా ఉండాలంటే వెంటనే {amount} చెల్లించండి."),
            ("loan_te_3", "మీ కాంటాక్ట్ లిస్ట్ లో ఉన్న అందరికీ మీ ఫోటోలు ఎడిట్ చేసి పంపిస్తాము. 1 గంటలో ఈ లింక్ లో లోన్ క్లియర్ చేయండి: {link}")
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
            ("cour_en_4", "DHL Express: Parcel on hold due to unpaid customs clearance duty of {amount}. Pay online within 24 hours at {link} to avoid seizure."),
            ("cour_en_5", "Narcotics Control Bureau Mumbai: Seized parcel booked under your Aadhaar. Supreme Court digital arrest order initiated. Settle security deposit of {amount} to prevent raid."),
            ("cour_en_6", "Delhi Customs Directorate: Package detained containing undeclared foreign currency and luxury items. Pay penalty tax {amount} via UPI immediately: {link}")
        ],
        "hi": [
            ("cour_hi_1", "{courier} अलर्ट: आपके नाम पर भेजा गया पार्सल सीमा शुल्क और नारकोटिक्स द्वारा पकड़ा गया है। इसमें नशीली दवाएं हैं। तुरंत पुलिस अधिकारी से वीडियो कॉल पर जुड़ें।"),
            ("cour_hi_2", "भारतीय डाक सूचना: आपका पार्सल पता अधूरा होने के कारण रोक दिया गया है। 48 रुपये का पुनः वितरण शुल्क देकर पता अपडेट करें: {link}"),
            ("cour_hi_3", "मुंबई क्राइम ब्रांच नोटिस: आपके पार्सल में ड्रग्स मिले हैं। सुप्रीम कोर्ट के डिजिटल अरेस्ट ऑर्डर से बचने के लिए तुरंत पुलिस वेरिफिकेशन फीस जमा करें।")
        ],
        "te": [
            ("cour_te_1", "{courier} హెచ్చరిక: మీ పేరుతో ఉన్న కొరియర్ పార్సెల్ లో డ్రగ్స్ ఉన్నట్లు కస్టమ్స్ అధికారులు గుర్తించారు. మీపై ఎఫ్‌ఐఆర్ నమోదైంది. వెంటనే విచారణ అధికారికి కాల్ చేయండి."),
            ("cour_te_2", "ఇండియా పోస్ట్: మీ పార్సెల్ చిరునామా సరిగ్గా లేనందున నిలిపివేయబడింది. ఈ లింక్‌లో చిరునామా అప్‌డేట్ చేసి రూ. 35 చెల్లించండి: {link}"),
            ("cour_te_3", "హైదరాబాద్ సైబర్ క్రైమ్: మీ ఆధార్ కార్డ్ తో డ్రగ్స్ కొరియర్ పంపినట్లు రికార్డు అయింది. డిజిటల్ అరెస్ట్ వారెంట్ జారీ చేయబడింది.")
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
            ("mkt_en_1", "I want to buy your item on OLX. I am sending you an official payment QR code. Scan this QR code in Google Pay and enter your UPI PIN to receive {amount} into your account!"),
            ("mkt_en_2", "Buyer on Quikr: I have generated a merchant receiver barcode. Scan it from your gallery and put your UPI PIN to get credited with {amount} instantly."),
            ("mkt_en_3", "Facebook Marketplace payment: Buyer generated receiving barcode. Scan QR code and authorize payment PIN to claim and accept {amount}."),
            ("mkt_en_4", "Used car token advance: Scan attached dynamic UPI QR code on Paytm and authenticate with your 6-digit PIN to receive deposit into your bank."),
            ("mkt_en_5", "Army officer buyer: I am purchasing your furniture on OLX. Scan this military canteen QR code and type your secret UPI PIN to receive money."),
            ("mkt_en_6", "OLX Escrow Secure Pay: Scan reverse QR code and enter MPIN to release buyer advance fund of {amount} to your savings a/c.")
        ],
        "hi": [
            ("mkt_hi_1", "मैं आपका सोफा ओएलएक्स पर खरीदना चाहता हूं। मैंने भुगतान के लिए एक क्यूआर कोड भेजा है। इसे फोनपे से स्कैन करें और अपना यूपीआई पिन डालें ताकि {amount} आपके खाते में आ जाएं।"),
            ("mkt_hi_2", "क्यूआर कोड स्कैन करके अपना यूपीआई पिन डालें और {amount} का एडवांस पेमेंट तुरंत अपने खाते में प्राप्त करें।"),
            ("mkt_hi_3", "आर्मी कैंटीन पेमेंट: सामान का एडवांस लेने के लिए यह बारकोड स्कैन करके अपना पिन डालें, पैसे तुरंत आपके बैंक खाते में क्रेडिट होंगे।")
        ],
        "te": [
            ("mkt_te_1", "నేను మీ వస్తువు కొంటాను. డబ్బులు పంపడానికి QR కోడ్ పంపాను. దీన్ని Google Pay లో స్కాన్ చేసి మీ UPI పిన్ కొడితే డబ్బులు మీ అకౌంట్ లో పడతాయి."),
            ("mkt_te_2", "ఈ క్యూఆర్ కోడ్ స్కాన్ చేసి మీ పిన్ ఎంటర్ చేయండి, వెంటనే {amount} మీ ఖాతాకు జమ అవుతాయి."),
            ("mkt_te_3", "ఆర్మీ ఆఫీసర్ కస్టమర్: మీ ఫర్నిచర్ అడ్వాన్స్ తీసుకోవడానికి ఈ రివర్స్ బార్‌కోడ్ స్కాన్ చేసి మీ ఎంపిన్ కొట్టండి.")
        ],
        "hinglish": [
            ("mkt_hn_1", "OLX par jo saman dala hai uska payment receive karne ke liye ye QR code scan karo aur PIN enter karo paise turant credit ho jayenge."),
            ("mkt_hn_2", "Bhai QR code scan karke PIN daal do advance payment {amount} receive ho jayega.")
        ],
        "roman_te": [
            ("mkt_rt_1", "Advance payment receive cheyadam kosam ee QR code scan chesi UPI PIN kottandi, direct ga bank account lo add aipotundi."),
            ("mkt_rt_2", "Payment receive cheyadaniki ee barcode scan chesi PIN enter cheyandi.")
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
            ("leg_en_18", "EPFO: Your monthly PF contribution of {amount} has been credited for member ID ending 4829."),
            ("leg_en_chat_1", "Bhai kal ke match ke ticket ke 500 rupaye phonepe kar de jab free ho."),
            ("leg_en_chat_2", "I sent 1000 rupees via GPay please check once brother."),
            ("leg_en_chat_3", "Mom called, she said grocery bill was paid using credit card at Reliance."),
            ("leg_en_chat_4", "IRCTC Booking: PNR 4829102847 confirmed. Train 12728 Godavari Exp. Coach B2 Berth 31."),
            ("leg_en_chat_5", "IndiGo flight 6E-204 web check-in is now open. Complete your boarding pass at goindigo.in."),
            ("leg_en_chat_6", "Can you send Rs 300 on Google Pay for dinner contribution?"),
            ("leg_en_chat_7", "Tata Power-DDL: Bill for CA 60012938491 for Nov-26 is Rs 2,340. Due date 02-Dec-2026. Pay safely at https://www.tatapower-ddl.com."),
            # --- Dedicated Genuine Merchant QR & Marketplace Hard Negatives ---
            ("leg_en_qr_1", "Paid {amount} to Sharma Groceries by scanning PhonePe merchant QR code. Transaction successful. UPI Ref 4920194821."),
            ("leg_en_qr_2", "Google Pay: You paid {amount} to Apollo Pharmacy via QR code scan at counter. Avail Bal: Rs 24,190.00."),
            ("leg_en_qr_3", "Paytm Merchant Receipt: {amount} paid successfully to Chai Point using BharatQR. Save paper, go digital."),
            ("leg_en_qr_4", "You scanned verified merchant QR at Reliance Smart Bazaar. Amount {amount} debited from your HDFC bank a/c."),
            ("leg_en_qr_5", "Scan the official BharatQR on your BESCOM electricity bill to make direct secure payment at bescom.karnataka.gov.in."),
            ("leg_en_qr_6", "OLX buyer chat: Yes the wooden study table is available. You can visit my house tomorrow evening to inspect in person."),
            ("leg_en_qr_7", "Quikr deal: I will buy your cycle for Rs 2,500. I can pay cash or scan your Google Pay QR code when I pick it up."),
            ("leg_en_qr_8", "Merchant settlement: Your shop QR code received Rs 150 from customer UPI transfer. Credited to current account."),
            ("leg_en_qr_9", "Payment of {amount} to Indian Oil Petrol Pump via GPay QR code successful. Reward scratch card unlocked."),
            ("leg_en_qr_10", "D-Mart Store: {amount} paid using UPI QR scanner. Cashier ID 402. Thank you for shopping with us!"),
            ("leg_en_qr_11", "Swiggy UPI: Paid {amount} for order #940192 via UPI. Food is being prepared by restaurant."),
            ("leg_en_qr_12", "Ola Cabs: Ride fare of Rs 240 paid via Paytm UPI auto-debit. Invoice emailed to your registered address."),
            ("leg_en_qr_13", "IRCTC Tatkal booking confirmed: PNR 4920194820. Rs 1,890 debited from SBI account. Happy Journey!"),
            ("leg_en_qr_14", "BBD Sale: Flipkart order dispatched via Ekart Logistics. Tracking ID FMPC492019482. Delivery by Friday."),
            ("leg_en_qr_15", "ICICI Bank Alert: Salary of {amount} credited to your salary account from WIPRO ENTERPRISES LTD.")
        ],
        "hi": [
            ("leg_hi_1", "{bank}: आपके खाते से {amount} की राशि यूपीआई द्वारा काटी गई है। शेष राशि 18,500 रुपये है। अपना ओटीपी या पिन किसी से साझा न करें। बैंक कभी भी ओटीपी नहीं मांगता।"),
            ("leg_hi_2", "{bank}: इंटरनेट बैंकिंग लॉगिन के लिए आपका ओटीपी 394812 है। यह 5 मिनट के लिए वैध है। इसे किसी को न बताएं।"),
            ("leg_hi_3", "प्रिय उपभोक्ता, आपका बिजली बिल {amount} नियत तिथि 25 तारीख तक देय है। आधिकारिक केंद्र पर सुरक्षित भुगतान करें।"),
            ("leg_hi_qr_1", "दुकानदार के क्यूआर कोड को स्कैन करके {amount} का भुगतान सफल रहा। यूटीआर नंबर 4920194821।"),
            ("leg_hi_qr_2", "फोनपे: शर्मा किराना स्टोर पर क्यूआर कोड से {amount} का भुगतान सफलतापूर्वक पूरा हुआ।"),
            ("leg_hi_qr_3", "ओएलएक्स चैट: जी टेबल अभी उपलब्ध है। आप कल शाम आकर देख सकते हैं और पसंद आए तो ले जा सकते हैं।"),
            ("leg_hi_qr_4", "पेट्रोल पंप पर यूपीआई बारकोड स्कैन करके {amount} का भुगतान किया गया। रसीद नंबर 940192।")
        ],
        "te": [
            ("leg_te_1", "{bank}: మీ ఖాతా నుండి {amount} UPI ద్వారా చెల్లించబడింది. మిగిలిన బ్యాలెన్స్ రూ. 15,300. మీ OTP లేదా PIN ఎవరితోనూ పంచుకోవద్దు. బ్యాంక్ ఎప్పుడూ OTP అడగదు."),
            ("leg_te_2", "{bank}: లాగిన్ కోసం మీ OTP 582910. 10 నిమిషాలు మాత్రమే చెల్లుతుంది. దీనిని ఎవరికీ చెప్పవద్దు."),
            ("leg_te_3", "మీ విద్యుత్ బిల్లు {amount} చెల్లించడానికి ఆఖరి తేదీ 28వ తేదీ. అధికారిక కార్యాలయం లేదా వెబ్‌సైట్ ద్వారా సురక్షితంగా చెల్లించండి."),
            ("leg_te_qr_1", "సూపర్ మార్కెట్ లో QR కోడ్ స్కాన్ చేసి {amount} విజయవంతంగా చెల్లించబడింది. మీ ఎస్బీఐ నిల్వ రూ. 18,400."),
            ("leg_te_qr_2", "గూగుల్ పే: మెడికల్ షాప్ లో క్యూఆర్ బార్‌కోడ్ ద్వారా {amount} చెల్లింపు విజయవంతమైంది."),
            ("leg_te_qr_3", "ఓఎల్ఎక్స్ డీల్: సోఫా అందుబాటులో ఉంది. రేపు ఉదయం వచ్చి చూసి నచ్చితే పేమెంట్ చేయవచ్చు.")
        ],
        "hinglish": [
            ("leg_hn_1", "{bank}: {amount} debited from your A/C via UPI. Balance Rs 12,400. Kabhi bhi apna OTP, UPI PIN kisi ko share na kare. Bank never calls for PIN."),
            ("leg_hn_2", "Aapka OTP 849201 hai. Yeh kisi ke saath share na kare, bank staff ke sath bhi nahi."),
            ("leg_hn_chat_1", "Bhai kal ke match ke ticket ke 500 rupaye phonepe kar de jab time mile."),
            ("leg_hn_chat_2", "Maine 1000 rupees GPay kar diye hain dekh le account me aa gaye honge."),
            ("leg_hn_chat_3", "Mummy ne bola tha dukan ka saman ka bill pay kar diya Paytm se."),
            ("leg_hn_chat_4", "Room rent ke 8000 rupaye transfer kar diye hain uncle, check kar lijiye."),
            ("leg_hn_chat_5", "Airtel ka 299 wala recharge ho gaya hai successful."),
            ("leg_hn_qr_1", "Bhai maine dukaan wale ke board par QR scan karke {amount} de diye the, receipt dekh lo."),
            ("leg_hn_qr_2", "OLX pe sofa available hai, aap physically aake check kar lo fir cash ya GPay kar dena.")
        ],
        "roman_te": [
            ("leg_rt_1", "{bank}: {amount} UPI dwara transfer cheyabadindi. Balance Rs 9,800. Mee OTP and PIN eppudu evaritho share cheyavoddu."),
            ("leg_rt_2", "Internet banking login kosam mee OTP 749201. Evariki cheppavaddu. Bank eppudu call chesi PIN adagadu."),
            ("leg_rt_chat_1", "Nenu neeku 1000 rupees GPay chesanu chusuko okasari account balance."),
            ("leg_rt_chat_2", "Anna PhonePe lo Rs 1500 pampanu, screenshot WhatsApp chesa chusuko."),
            ("leg_rt_chat_3", "Current bill BESCOM app lo pay chesanu receipt vachindi."),
            ("leg_rt_chat_4", "Dinner ki 400 Google Pay cheyava urgent ga petrol kottali."),
            ("leg_rt_qr_1", "Shop lo PhonePe QR code scan chesi {amount} pay chesanu, bill payment success aindi."),
            ("leg_rt_qr_2", "Quikr lo item undi, direct ga vachi chusukondi, nachithe UPI cheyandi.")
        ]
    }
}

def generate_synthetic_samples(target_per_cat: int = 750) -> List[Dict[str, Any]]:
    samples = []
    
    for cat, lang_dict in RAW_TEMPLATE_DEFS.items():
        all_templates = []
        for lang, tpls in lang_dict.items():
            for tpl_id, tpl_text in tpls:
                all_templates.append((tpl_id, lang, tpl_text))
        
        # Balance samples per category; for legitimate, increase volume to provide hard negatives
        cat_target = target_per_cat if cat != "legitimate" else target_per_cat * 2
        
        for i in range(cat_target):
            tpl_id, lang, tpl_str = random.choice(all_templates)
            text = tpl_str.format(
                bank=random.choice(BANKS),
                board=random.choice(POWER_BOARDS),
                scheme=random.choice(GOVT_SCHEMES),
                app=random.choice(REMOTE_APPS),
                courier=random.choice(COURIER_BRANDS),
                amount=random.choice(AMOUNTS),
                time=random.choice(TIMES),
                link=get_fake_link()
            )
            # Add slight adversarial noise or variation
            text = inject_noise(text)
            
            samples.append({
                "template_id": tpl_id,
                "category": cat,
                "language": lang,
                "text": text
            })
            
    return samples

def main():
    print("=" * 65)
    print("  UPI RAKSHAK AI — DATASET GENERATOR (ENHANCED QUALITY)")
    print("=" * 65)
    random.seed(42)
    samples = generate_synthetic_samples(target_per_cat=800)
    df = pd.DataFrame(samples)
    
    print(f"Total samples synthesized: {len(df)}")
    print("Class distribution:")
    print(df["category"].value_counts())
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "synthetic_scam_dataset.csv")
    df.to_csv(out_file, index=False, encoding="utf-8")
    print(f"\nSaved synthetic dataset to: {out_file}")

if __name__ == "__main__":
    main()
