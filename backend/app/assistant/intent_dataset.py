"""
Intent Classification Datasets for Conversational Safety Assistant.
Contains 330+ training samples and 180+ held-out test samples across English,
Hindi, Telugu, and Hinglish with realistic human typos.
"""

INTENT_ANALYZE = "ANALYZE"
INTENT_HELP = "HELP"
INTENT_HOW_TO = INTENT_HELP
INTENT_EMERGENCY = "EMERGENCY"
INTENT_GREETING = "GREETING"
INTENT_SMALL_TALK = INTENT_GREETING
INTENT_OUT_OF_SCOPE = "OUT_OF_SCOPE"
INTENT_UNCLEAR = "UNCLEAR"

ALL_INTENTS = [
    INTENT_ANALYZE,
    INTENT_HELP,
    INTENT_EMERGENCY,
    INTENT_GREETING,
    INTENT_OUT_OF_SCOPE,
    INTENT_UNCLEAR,
]

TRAIN_INTENT_DATA = [
    ["How do I make authentic Hyderabadi chicken biryani at home?", "OUT_OF_SCOPE"],
    ["What is the weather forecast for New Delhi today?", "OUT_OF_SCOPE"],
    ["Who won the ICC Cricket World Cup in 2011?", "OUT_OF_SCOPE"],
    ["Write a python function to reverse a singly linked list.", "OUT_OF_SCOPE"],
    ["Tell me a funny joke about software developers.", "OUT_OF_SCOPE"],
    ["What is the capital city of Australia?", "OUT_OF_SCOPE"],
    ["Can you write an essay about renewable solar energy?", "OUT_OF_SCOPE"],
    ["Solve the quadratic equation 2x^2 + 5x - 3 = 0.", "OUT_OF_SCOPE"],
    ["What movies are releasing this weekend in cinema halls?", "OUT_OF_SCOPE"],
    ["How to play chess for complete beginners?", "OUT_OF_SCOPE"],
    ["What is the average distance between Earth and Mars?", "OUT_OF_SCOPE"],
    ["How to bake a chocolate fudge cake without microwave?", "OUT_OF_SCOPE"],
    ["Who is the current CEO of Google Alphabet?", "OUT_OF_SCOPE"],
    ["Write a short rhyming poem about monsoons and rain.", "OUT_OF_SCOPE"],
    ["Explain offside rule in football.", "OUT_OF_SCOPE"],
    ["How to train for running a half marathon in 12 weeks?", "OUT_OF_SCOPE"],
    ["बिरयानी बनाने की सबसे स्वादिष्ट रेसिपी बताइए", "OUT_OF_SCOPE"],
    ["आज मुंबई का मौसम कैसा रहने वाला है?", "OUT_OF_SCOPE"],
    ["क्रिकेट में सबसे ज्यादा शतक किसने बनाए हैं?", "OUT_OF_SCOPE"],
    ["मुझे एक मजेदार चुटकुला सुनाओ भाई", "OUT_OF_SCOPE"],
    ["ताजमहल किस मुगल बादशाह ने बनवाया था?", "OUT_OF_SCOPE"],
    ["पायथन प्रोग्रामिंग में फॉर लूप कैसे लिखते हैं?", "OUT_OF_SCOPE"],
    ["भारत की राजधानी और राष्ट्रपति कौन हैं?", "OUT_OF_SCOPE"],
    ["घर पर गुलाब जामुन कैसे बनाते हैं?", "OUT_OF_SCOPE"],
    ["హైదరాబాద్ దమ్ బిర్యానీ ఎలా తయారు చేయాలి?", "OUT_OF_SCOPE"],
    ["ఈరోజు విజయవాడలో వర్షం పడుతుందా వాతావరణం ఎలా ఉంది?", "OUT_OF_SCOPE"],
    ["నాకు ఒక మంచి తెలుగు కామెడీ జోక్ చెప్పండి", "OUT_OF_SCOPE"],
    ["పైథాన్ ప్రోగ్రామింగ్ ఎలా నేర్చుకోవాలి?", "OUT_OF_SCOPE"],
    ["బాహుబలి సినిమా డైరెక్టర్ రాజమౌళి ఇతర సినిమాలు ఏవి?", "OUT_OF_SCOPE"],
    ["భారతదేశానికి స్వాతంత్ర్యం ఏ సంవత్సరంలో వచ్చింది?", "OUT_OF_SCOPE"],
    ["మంచి మసాలా టీ ఎలా తయారు చేసుకోవాలి?", "OUT_OF_SCOPE"],
    ["Biryani kaise banate hain step by step recipe batao", "OUT_OF_SCOPE"],
    ["Aaj Bangalore me weather kaisa hai thand hai kya", "OUT_OF_SCOPE"],
    ["Write python code for binary search tree insertion", "OUT_OF_SCOPE"],
    ["Ek mast chutkula sunao hasi aaye", "OUT_OF_SCOPE"],
    ["Kal IPL match kis team ne jeeta tha", "OUT_OF_SCOPE"],
    ["Ee roju weather ela undi Hyderabad lo", "OUT_OF_SCOPE"],
    ["Bookmyshow lo cinema tickets ela book cheyali", "OUT_OF_SCOPE"],

    [
        "URGENT: Your SBI YONO account will be blocked tonight. Click http://sbi-kyc-verify.top to update PAN immediately.",
        "ANALYZE"
    ],
    [
        "Dear customer, your electricity power will be disconnected at 9:30 PM due to unpaid bill. Call officer at 9876543210.",
        "ANALYZE"
    ],
    [
        "Congratulations! You won Rs 25,00,000 in KBC Kaun Banega Crorepati. Contact WhatsApp manager at +919123456789.",
        "ANALYZE"
    ],
    [
        "Part-time work from home: Earn Rs 3000 to Rs 8000 daily by liking YouTube videos. Join telegram channel t.me/fastcashindia",
        "ANALYZE"
    ],
    [
        "Your package from India Post cannot be delivered due to invalid address. Update your address at http://indiapost-update.xyz/track",
        "ANALYZE"
    ],
    [
        "Traffic Police Notice: You have 1 unpaid challan of Rs 1000. Pay immediately at http://echallan-parivahan.info or face court summons.",
        "ANALYZE"
    ],
    [
        "Dear HDFC user, 5420 reward points worth Rs 5420 are expiring today. Redeem cash in your account at http://hdfc-rewards-cash.top",
        "ANALYZE"
    ],
    [
        "FASTag alert: Your FASTag wallet is deactivated. Update KYC immediately at http://fastag-nhai-kyc.online",
        "ANALYZE"
    ],
    [
        "Your loan of Rs 5,00,000 is approved at 2% interest rate. Download app from http://quick-cash-loan.apk to disburse funds.",
        "ANALYZE"
    ],
    [
        "CBI / Mumbai Police Notice: A parcel containing 5 passports and MDMA drugs intercepted in your name. Connect on Skype for verification.",
        "ANALYZE"
    ],
    [
        "Customer sent collect request: 'Approve collect request of Rs 2000 to receive cashback refund from Google Pay'",
        "ANALYZE"
    ],
    [
        "http://192.168.1.10/sbi/login.html",
        "ANALYZE"
    ],
    [
        "https://paytm-kyc-customer-care.xyz/verify",
        "ANALYZE"
    ],
    [
        "payment to refund-desk@okhdfcbank",
        "ANALYZE"
    ],
    [
        "Someone sent me this: 'Dear user your SIM card will be deactivated in 24 hours. Call DoT officer on 9811223344'",
        "ANALYZE"
    ],
    [
        "Is this message genuine? 'Your ICICI Bank credit card is blocked. Download our support tool at http://icici-desk.cc'",
        "ANALYZE"
    ],
    [
        "Look at this SMS: 'Airtel alert: 5G upgrade pending. Send SIM 1234567890 to 121 to continue services'",
        "ANALYZE"
    ],
    [
        "Fwd: Income Tax refund of Rs 15,490 approved. Submit bank account details at http://incometax-efiling-refund.online",
        "ANALYZE"
    ],
    [
        "Check this payment handle for me: merchant-cashback@ybl",
        "ANALYZE"
    ],
    [
        "Is this QR code safe? Scan to receive Rs 1500 prize money from PhonePe rewards",
        "ANALYZE"
    ],
    [
        "Work from home earn 3000 to 5000 daily. Just like videos and get paid: bit.ly/youtube-earn",
        "ANALYZE"
    ],
    [
        "Airtel 5G upgrade pending: Click http://airtel-5g-sim.top to avoid sim suspension.",
        "ANALYZE"
    ],
    [
        "Dear user, your HDFC netbanking password expired. Update now at http://hdfc-pass-reset.site",
        "ANALYZE"
    ],
    [
        "SBI card rewards worth Rs 8500 expired today. Click http://sbi-pointscash.online",
        "ANALYZE"
    ],
    [
        "Customs Department notice: Foreign courier parcel detained at Mumbai Airport. Pay duty Rs 4500.",
        "ANALYZE"
    ],
    [
        "Canara Bank: Your debit card is blocked. Reactivate by calling officer 9811224455.",
        "ANALYZE"
    ],
    [
        "Electricity department: Power disconnection tonight at 9 PM. Call junior engineer on 9876543210.",
        "ANALYZE"
    ],
    [
        "Congratulations you won lottery of Rs 10 Lakhs. WhatsApp +919876543210 to claim prize.",
        "ANALYZE"
    ],
    [
        "Traffic fine pending Rs 2000 on vehicle DL01AB1234. Pay at http://echallan-vahan.xyz",
        "ANALYZE"
    ],
    [
        "Income Tax department approved refund Rs 24,500. Enter details at http://incometax-efiling.top",
        "ANALYZE"
    ],
    [
        "Someone sent this SMS: Punjab National Bank KYC incomplete. Update immediately.",
        "ANALYZE"
    ],
    [
        "Is this UPI ID safe to transfer: customer-care-refund@okhdfcbank",
        "ANALYZE"
    ],
    [
        "Check this payment address: sbi-kyc-desk@ybl",
        "ANALYZE"
    ],
    [
        "Check this QR code received from buyer on OLX for payment of sofa",
        "ANALYZE"
    ],
    [
        "Collect request: Merchant requests Rs 4999 with note Receive Paytm Bonus Cashback",
        "ANALYZE"
    ],
    [
        "Aapka bijli ka bill baki hai, aaj shaam bijli kat jayegi 9876509876 par call karein",
        "ANALYZE"
    ],
    [
        "Badhai ho! Aapko mila hai Pradhan Mantri Yojna ka 50,000 subsidy. Link: http://pm-yojana.top",
        "ANALYZE"
    ],
    [
        "WhatsApp par ye sandesh aaya hai: Ghar baithe paise kamayein daily 4000 t.me/dailyearn",
        "ANALYZE"
    ],
    [
        "Mera SBI account block ka message aaya: http://sbi-yono-update.xyz",
        "ANALYZE"
    ],
    [
        "Ye QR code scan karke 2000 lene ko bol raha hai OLX buyer",
        "ANALYZE"
    ],
    [
        "Customs police parcel arrest warrant notice bheja hai WhatsApp par",
        "ANALYZE"
    ],
    [
        "Credit card reward points cash me badalne ka link: http://rbi-rewards.site",
        "ANALYZE"
    ],
    [
        "Ye message sahi hai kya: Bank of Baroda account suspended tonight call 9876543210",
        "ANALYZE"
    ],
    [
        "Airtel SIM band hone ka SMS mila hai call karo 9811223344",
        "ANALYZE"
    ],
    [
        "PAN card link nahi kiya to account band ho jayega: http://pan-aadhaar-link.top",
        "ANALYZE"
    ],
    [
        "प्रिय ग्राहक, आपके एसबीआई खाते का केवाईसी पूरा नहीं हुआ है। आज रात आपका खाता बंद कर दिया जाएगा: http://sbi-kyc-pan.xyz",
        "ANALYZE"
    ],
    [
        "बिजली विभाग सूचना: आपका पिछला बिजली बिल जमा नहीं हुआ है, आज शाम 8 बजे बिजली काट दी जाएगी। कॉल करें: 9876543210",
        "ANALYZE"
    ],
    [
        "बधाई हो! आपको मिला है 50,000 रुपये का सरकारी युवा लैपटॉप अनुदान। फॉर्म भरें: http://pm-yojna-free-laptop.online",
        "ANALYZE"
    ],
    [
        "घर बैठे पैसे कमाएं: यूट्यूब वीडियो लाइक करके रोजाना 2000-5000 कमाएं। टेलीग्राम लिंक पर क्लिक करें: t.me/dailyincome",
        "ANALYZE"
    ],
    [
        "केबीसी लकी ड्रॉ 25 लाख लॉटरी विजेता। मैनेजर राणा प्रताप सिंह से संपर्क करें 9988776655",
        "ANALYZE"
    ],
    [
        "Mera account block hone ka message aaya hai: 'Your PNB account suspended. Click http://pnb-verify.cc'",
        "ANALYZE"
    ],
    [
        "Mujhe ye SMS mila: 'Aapka bijli cut hone wala hai, turant call kare 9876501234'",
        "ANALYZE"
    ],
    [
        "Ye link check karo: http://sbi-yono-reward.xyz/login",
        "ANALYZE"
    ],
    [
        "Ye message sach hai ya fraud? 'Aapke account me 2500 cashback aaya hai, pin daale'",
        "ANALYZE"
    ],
    [
        "WhatsApp pe ye aaya: 'Courier company customs duty pending Rs 450 pay at link'",
        "ANALYZE"
    ],
    [
        "మీ ఎస్బీఐ ఖాతా కేవైసీ గడువు ముగిసింది. ఖాతా నిలిపివేయబడకుండా వెంటనే http://sbi-kyc-update.xyz లో అప్‌డేట్ చేయండి.",
        "ANALYZE"
    ],
    [
        "విద్యుత్ శాఖ హెచ్చరిక: మీ కరెంట్ బిల్లు చెల్లించనందున ఈ రాత్రి 9:30 గంటలకు విద్యుత్ సరఫరా నిలిపివేయబడుతుంది. వెంటనే ఈ నంబర్‌కు కాల్ చేయండి: 9876543210",
        "ANALYZE"
    ],
    [
        "మీకు ప్రధాని యోజన కింద రూ. 50,000 ఉచిత సబ్సిడీ మంజూరైంది. దరఖాస్తు చేసుకోవడానికి లింక్ క్లిక్ చేయండి: http://pm-subsidy.online",
        "ANALYZE"
    ],
    [
        "నాకు ఈ మెసేజ్ వచ్చింది: 'మీ కొరియర్ పార్సెల్ చిరునామా తప్పుగా ఉంది. రూ. 10 చెల్లించి చిరునామా సరిచేయండి: http://indpost.cc'",
        "ANALYZE"
    ],
    [
        "ఈ యూపీఐ ఐడీ మోసపూరితమైనదా?: sbi-refund@paytm",
        "ANALYZE"
    ],
    [
        "ఫోన్‌పే లో రూ. 5000 క్యాష్‌బ్యాక్ వచ్చిందని కలెక్ట్ రిక్వెస్ట్ పంపారు. పిన్ ఎంటర్ చేయమంటున్నారు.",
        "ANALYZE"
    ],
    [
        "నాకు వచ్చిన మెసేజ్: 'పోలీస్ డిజిటల్ అరెస్ట్ వారెంట్ జారీ చేయబడింది. వెంటనే స్కైప్‌లో కలవండి.'",
        "ANALYZE"
    ],
    [
        "ఈ లింక్ సురక్షితమైనదా? http://phonepe-reward-scratch.top",
        "ANALYZE"
    ],
    [
        "మీ ఎస్బీఐ యోనో ఖాతా నిలిపివేయబడింది. వెంటనే http://sbi-yono.top లో పాన్ కార్డ్ లింక్ చేయండి.",
        "ANALYZE"
    ],
    [
        "మీ కరెంట్ బిల్లు కట్టలేదు, రాత్రి 9:30 కి కరెంట్ తీసేస్తారు, అధికారికి కాల్ చేయండి: 9876543210",
        "ANALYZE"
    ],
    [
        "మీకు రూ. 10 లక్షల లాటరీ తగిలింది. మేనేజర్ కి వాట్సాప్ చేయండి: 9876543210",
        "ANALYZE"
    ],
    [
        "పార్ట్‌టైమ్ జాబ్: రోజుకు రూ. 3000 సంపాదించండి. టెలిగ్రామ్ లింక్: t.me/telugujobs",
        "ANALYZE"
    ],
    [
        "మీ కొరియర్ ఆగిపోయింది. చిరునామా సరిచేయడానికి http://post-courier.xyz లింక్ క్లిక్ చేయండి.",
        "ANALYZE"
    ],
    [
        "ఈ యూపీఐ ఐడీ మోసమా కాదా తనిఖీ చేయండి: gpay-support@paytm",
        "ANALYZE"
    ],
    [
        "నాకు వచ్చిన మెసేజ్: మీ సిమ్ కార్డ్ 24 గంటల్లో బ్లాక్ చేయబడుతుంది. కాల్ 9811223344",
        "ANALYZE"
    ],
    [
        "ట్రాఫిక్ చలాన్ రూ. 1500 కట్టమని లింక్ పంపారు: http://traffic-police.online",
        "ANALYZE"
    ],
    [
        "ఓఎల్ఎక్స్ లో వస్తువు కొంటానని ఈ క్యూఆర్ కోడ్ స్కాన్ చేసి పిన్ కొట్టమంటున్నారు.",
        "ANALYZE"
    ],
    [
        "ఇన్‌కమ్ టాక్స్ రీఫండ్ రూ. 18500 వచ్చిందని ఈ లింక్ పంపారు: http://it-refund.top",
        "ANALYZE"
    ],
    [
        "how to complain to 1930",
        "HELP"
    ],
    [
        "how do I report on cybercrime.gov.in",
        "HELP"
    ],
    [
        "what is the process to file a cyber complaint",
        "HELP"
    ],
    [
        "how to block my UPI ID",
        "HELP"
    ],
    [
        "how do collect requests work in UPI",
        "HELP"
    ],
    [
        "what is digital arrest",
        "HELP"
    ],
    [
        "how to verify if a bank SMS is genuine or fake",
        "HELP"
    ],
    [
        "is UPI safe for online shopping",
        "HELP"
    ],
    [
        "what should I prepare before calling 1930",
        "HELP"
    ],
    [
        "how to recover money from a cyber fraud",
        "HELP"
    ],
    [
        "what is golden hour in cyber crime",
        "HELP"
    ],
    [
        "how do scammers steal money through QR codes",
        "HELP"
    ],
    [
        "can someone debit money if I only give my UPI ID",
        "HELP"
    ],
    [
        "how to check if a website domain is an official bank site",
        "HELP"
    ],
    [
        "what to do if I shared my OTP with someone",
        "HELP"
    ],
    [
        "what steps should I take if I installed AnyDesk app",
        "HELP"
    ],
    [
        "how to freeze my bank account quickly",
        "HELP"
    ],
    [
        "how to report a fraudulent mobile number to Chakshu portal",
        "HELP"
    ],
    [
        "can police arrest someone over WhatsApp video call",
        "HELP"
    ],
    [
        "what is RBI zero liability policy",
        "HELP"
    ],
    [
        "how to change UPI PIN in PhonePe and Google Pay",
        "HELP"
    ],
    [
        "how to file an FIR for online financial fraud",
        "HELP"
    ],
    [
        "how does AnyDesk allow scammers to see my screen",
        "HELP"
    ],
    [
        "how to de-link bank account from Google Pay",
        "HELP"
    ],
    [
        "what is TRAI DLT header on SMS",
        "HELP"
    ],
    [
        "how to check mobile numbers registered on my Aadhaar using TAFCOP",
        "HELP"
    ],
    [
        "how to protect senior citizens from UPI scams",
        "HELP"
    ],
    [
        "is entering UPI PIN required to receive money",
        "HELP"
    ],
    [
        "how to know if customer care number on Google is fake",
        "HELP"
    ],
    [
        "what documents are required for cybercrime complaint",
        "HELP"
    ],
    [
        "how to file a cyber complaint on cybercrime.gov.in",
        "HELP"
    ],
    [
        "what is the official helpline number for online fraud in India",
        "HELP"
    ],
    [
        "how to block upi id in google pay",
        "HELP"
    ],
    [
        "how to block upi id in paytm",
        "HELP"
    ],
    [
        "how to de-link my bank account from upi apps",
        "HELP"
    ],
    [
        "what is digital arrest scam and how does it operate",
        "HELP"
    ],
    [
        "how do collect requests work in upi payments",
        "HELP"
    ],
    [
        "is upi pin required to receive money or cashback",
        "HELP"
    ],
    [
        "how to verify if an SMS is from genuine bank or fraudster",
        "HELP"
    ],
    [
        "what are the TRAI DLT header rules for bank sms",
        "HELP"
    ],
    [
        "what should I prepare before calling 1930 helpline",
        "HELP"
    ],
    [
        "what to do if I installed anydesk on caller advice",
        "HELP"
    ],
    [
        "what to do if I accidentally shared my otp or upi pin",
        "HELP"
    ],
    [
        "how to recover money lost in cyber fraud",
        "HELP"
    ],
    [
        "what is rbi zero liability rule for unauthorized banking transactions",
        "HELP"
    ],
    [
        "how to report suspicious mobile number on Chakshu portal",
        "HELP"
    ],
    [
        "how to check mobile connections registered in my name on Sanchar Saathi",
        "HELP"
    ],
    [
        "how to lock Aadhaar biometrics to prevent AePS fraud",
        "HELP"
    ],
    [
        "how to freeze bank account immediately",
        "HELP"
    ],
    [
        "can cyber police freeze scammer bank account",
        "HELP"
    ],
    [
        "1930 पर साइबर क्राइम शिकायत कैसे दर्ज करें",
        "HELP"
    ],
    [
        "cybercrime.gov.in पोर्टल पर रिपोर्ट कैसे करते हैं",
        "HELP"
    ],
    [
        "अपना यूपीआई आईडी कैसे ब्लॉक करें",
        "HELP"
    ],
    [
        "डिजिटल अरेस्ट क्या होता है",
        "HELP"
    ],
    [
        "क्या पैसे लेने के लिए यूपीआई पिन डालना पड़ता है",
        "HELP"
    ],
    [
        "नकली बैंक मैसेज की पहचान कैसे करें",
        "HELP"
    ],
    [
        "कलेक्ट रिक्वेस्ट कैसे काम करता है",
        "HELP"
    ],
    [
        "अगर किसी को ओटीपी बता दिया तो क्या करना चाहिए",
        "HELP"
    ],
    [
        "एनीडेस्क ऐप डाउनलोड कर लिया तो क्या करें",
        "HELP"
    ],
    [
        "साइबर फ्रॉड होने पर बैंक में शिकायत कैसे करें",
        "HELP"
    ],
    [
        "1930 helpline pe complain kaise kare",
        "HELP"
    ],
    [
        "cybercrime portal me kya documents upload karne hote hain",
        "HELP"
    ],
    [
        "upi id block karne ka tarika batao",
        "HELP"
    ],
    [
        "kya police video call pe arrest kar sakti hai",
        "HELP"
    ],
    [
        "golden hour kya hota hai fraud me",
        "HELP"
    ],
    [
        "fake message kaise pehchane",
        "HELP"
    ],
    [
        "gpay se bank account unlink kaise kare",
        "HELP"
    ],
    [
        "upi pin change kaise karte hain phonepe me",
        "HELP"
    ],
    [
        "1930 helpline par call kaise karein",
        "HELP"
    ],
    [
        "cybercrime portal par online report kaise darj karein",
        "HELP"
    ],
    [
        "gpay me upi id block kaise karein",
        "HELP"
    ],
    [
        "phonepe me upi id delete kaise karein",
        "HELP"
    ],
    [
        "kya paise lene ke liye kabhi bhi pin dalna padta hai",
        "HELP"
    ],
    [
        "digital arrest kya hai aur kya police video call pe arrest kar sakti hai",
        "HELP"
    ],
    [
        "fake bank sms ko kaise pehchane",
        "HELP"
    ],
    [
        "agar kisi ko otp de diya to turant kya karna chahiye",
        "HELP"
    ],
    [
        "anydesk app download karne ke baad phone safe kaise karein",
        "HELP"
    ],
    [
        "bank account ko freeze kaise karwaye",
        "HELP"
    ],
    [
        "chakshu portal par fraud number report kaise karein",
        "HELP"
    ],
    [
        "1930 par complaint karne ke liye kya jankari chahiye",
        "HELP"
    ],
    [
        "cyber fraud hone par paise wapas aane ka kya process hai",
        "HELP"
    ],
    [
        "sanchar saathi portal par sim check kaise karein",
        "HELP"
    ],
    [
        "aadhaar biometric lock kaise karte hain",
        "HELP"
    ],
    [
        "1930 హెల్ప్‌లైన్‌కు సైబర్ మోసం గురించి ఎలా ఫిర్యాదు చేయాలి",
        "HELP"
    ],
    [
        "cybercrime.gov.in పోర్టల్‌లో ఆన్‌లైన్ ఫిర్యాదు ఎలా నమోదు చేయాలి",
        "HELP"
    ],
    [
        "నా యూపీఐ ఐడీని ఎలా బ్లాక్ చేసుకోవాలి",
        "HELP"
    ],
    [
        "డిజిటల్ అరెస్ట్ అంటే ఏమిటి మరియు ఇది నిజమా",
        "HELP"
    ],
    [
        "యూపీఐ కలెక్ట్ రిక్వెస్ట్ ఎలా పనిచేస్తుంది",
        "HELP"
    ],
    [
        "బ్యాంక్ నుంచి వచ్చిన మెసేజ్ అసలైనదో కాదో ఎలా తెలుసుకోవాలి",
        "HELP"
    ],
    [
        "డబ్బులు తీసుకోవడానికి యూపీఐ పిన్ నమోదు చేయాలా",
        "HELP"
    ],
    [
        "ఒకవేళ పొరపాటున ఎవరికైనా ఓటీపీ చెబితే ఏం చేయాలి",
        "HELP"
    ],
    [
        "ఎనీడెస్క్ యాప్ ఇన్‌స్టాల్ చేసుకుంటే ఫోన్ సేఫ్‌గా ఉంచడానికి ఏం చేయాలి",
        "HELP"
    ],
    [
        "సైబర్ క్రైమ్ ఫిర్యాదు కోసం ఏఏ ఆధారాలు సిద్ధం చేసుకోవాలి",
        "HELP"
    ],
    [
        "1930 lo complain ela ivvali",
        "HELP"
    ],
    [
        "cybercrime portal lo report cheyadam ela",
        "HELP"
    ],
    [
        "upi id block cheyatam ela",
        "HELP"
    ],
    [
        "digital arrest ante ento cheppandi",
        "HELP"
    ],
    [
        "bank account freeze ela cheyali",
        "HELP"
    ],
    [
        "1930 హెల్ప్‌లైన్‌కు సైబర్ మోసం ఫిర్యాదు ఎలా చేయాలి",
        "HELP"
    ],
    [
        "cybercrime.gov.in లో ఆన్‌లైన్ ఎఫ్‌ఐఆర్ ఎలా నమోదు చేయాలి",
        "HELP"
    ],
    [
        "గూగుల్ పే లో నా యూపీఐ ఐడీని ఎలా డిలీట్ చేయాలి",
        "HELP"
    ],
    [
        "ఫోన్‌పే లో యూపీఐ ఐడీ బ్లాక్ చేయడం ఎలా",
        "HELP"
    ],
    [
        "డబ్బులు స్వీకరించడానికి యూపీఐ పిన్ అవసరమా",
        "HELP"
    ],
    [
        "డిజిటల్ అరెస్ట్ అంటే ఏమిటి మరియు చట్టపరంగా ఇది చెల్లుతుందా",
        "HELP"
    ],
    [
        "నకిలీ బ్యాంక్ మెసేజ్‌లను ఎలా గుర్తించాలి",
        "HELP"
    ],
    [
        "ఓటీపీ చెబితే వెంటనే ఏం చేయాలి",
        "HELP"
    ],
    [
        "ఎనీడెస్క్ యాప్ ఇన్‌స్టాల్ చేస్తే సైబర్ మోసం ఎలా ఆపాలి",
        "HELP"
    ],
    [
        "బ్యాంక్ ఖాతాను వెంటనే ఫ్రీజ్ చేయడం ఎలా",
        "HELP"
    ],
    [
        "చక్షు పోర్టల్‌లో ఫేక్ నంబర్‌ను ఎలా రిపోర్ట్ చేయాలి",
        "HELP"
    ],
    [
        "1930 కి కాల్ చేసే ముందు ఏఏ వివరాలు సిద్ధం చేసుకోవాలి",
        "HELP"
    ],
    [
        "ఆధార్ బయోమెట్రిక్ లాక్ ఎలా చేసుకోవాలి",
        "HELP"
    ],
    [
        "సైబర్ మోసంలో పోయిన డబ్బును ఎలా రికవర్ చేయాలి",
        "HELP"
    ],
    [
        "కలెక్ట్ రిక్వెస్ట్ ఆమోదిస్తే డబ్బులు కట్ అవుతాయా",
        "HELP"
    ],
    [
        "I lost 5000 rupees to a scammer just now",
        "EMERGENCY"
    ],
    [
        "Money was debited from my bank account without my permission",
        "EMERGENCY"
    ],
    [
        "Scammer withdrew 25000 from my SBI account",
        "EMERGENCY"
    ],
    [
        "I just entered my UPI PIN on a phishing link and money got deducted",
        "EMERGENCY"
    ],
    [
        "Help me please! 10000 rupees gone from Google Pay",
        "EMERGENCY"
    ],
    [
        "I installed AnyDesk and now money is deducting automatically",
        "EMERGENCY"
    ],
    [
        "A fake officer made me transfer 50000 rupees for digital arrest",
        "EMERGENCY"
    ],
    [
        "My account was debited Rs 12500 by an unknown merchant",
        "EMERGENCY"
    ],
    [
        "I shared my OTP and entire bank balance was transferred",
        "EMERGENCY"
    ],
    [
        "Fraud happened 10 minutes ago, please help me recover funds",
        "EMERGENCY"
    ],
    [
        "Someone debited Rs 50000 through unauthorized collect request",
        "EMERGENCY"
    ],
    [
        "I have been cheated of 1 lakh rupees in a fake loan scam",
        "EMERGENCY"
    ],
    [
        "Money stolen from my account right now, what should I do",
        "EMERGENCY"
    ],
    [
        "Emergency! Unauthorized withdrawal of Rs 30,000 from my HDFC card",
        "EMERGENCY"
    ],
    [
        "I lost 15000 rupees to a cyber scammer just now",
        "EMERGENCY"
    ],
    [
        "Someone withdrew 50000 from my savings account without my knowledge",
        "EMERGENCY"
    ],
    [
        "Emergency help needed! Money debited from my account right now",
        "EMERGENCY"
    ],
    [
        "I installed AnyDesk and Rs 35000 was deducted immediately",
        "EMERGENCY"
    ],
    [
        "I gave my OTP to a caller and my account balance is now zero",
        "EMERGENCY"
    ],
    [
        "Fraud just happened! 12000 rupees transferred to a fraudster",
        "EMERGENCY"
    ],
    [
        "A fake police officer made me transfer 75000 for digital arrest",
        "EMERGENCY"
    ],
    [
        "Someone accepted a collect request on my phone and 8000 debited",
        "EMERGENCY"
    ],
    [
        "Unauthorized transaction of Rs 20000 on my credit card",
        "EMERGENCY"
    ],
    [
        "Help please, all my money stolen by a fake customer care caller",
        "EMERGENCY"
    ],
    [
        "मेरे खाते से अभी 5000 रुपये कट गए हैं, मदद करें",
        "EMERGENCY"
    ],
    [
        "धोखेबाज ने मेरे बैंक से 20000 रुपये निकाल लिए",
        "EMERGENCY"
    ],
    [
        "मैंने ओटीपी बता दिया और खाते से सारे पैसे उड़ गए",
        "EMERGENCY"
    ],
    [
        "एनीडेस्क डाउनलोड करवाया और 15000 डेबिट हो गए",
        "EMERGENCY"
    ],
    [
        "तुरंत मदद चाहिए! मेरे एसबीआई अकाउंट से अनधिकृत ट्रांसफर हुआ है",
        "EMERGENCY"
    ],
    [
        "Mera 10000 rupees cut gaya scam me abhi",
        "EMERGENCY"
    ],
    [
        "Account se paise debit ho gaye fraud me turant help karo",
        "EMERGENCY"
    ],
    [
        "Scammer ne 50000 rupaye nikal liye bank se",
        "EMERGENCY"
    ],
    [
        "Maine pin daala aur paise chale gaye",
        "EMERGENCY"
    ],
    [
        "Paisa kat gaya account se fraud ho gaya",
        "EMERGENCY"
    ],
    [
        "Mere account se abhi 15000 rupaye cut gaye hain",
        "EMERGENCY"
    ],
    [
        "Kisi ne mere bank se 50000 nikal liye fraud me",
        "EMERGENCY"
    ],
    [
        "Turant madad karein! Account se unauthorized debit hua hai",
        "EMERGENCY"
    ],
    [
        "Maine AnyDesk install kiya aur 30000 nikal gaye",
        "EMERGENCY"
    ],
    [
        "Caller ko OTP bata diya aur account khali ho gaya",
        "EMERGENCY"
    ],
    [
        "Digital arrest ke dar se maine 50000 transfer kar diye",
        "EMERGENCY"
    ],
    [
        "Abhi 10 minute pehle fraud hua hai 25000 rupaye chale gaye",
        "EMERGENCY"
    ],
    [
        "Fake customer care ne mere 18000 rupaye nikal liye",
        "EMERGENCY"
    ],
    [
        "Mere Google Pay se 10000 rupaye debit ho gaye fraud me",
        "EMERGENCY"
    ],
    [
        "Paisa kat gaya account se turant bank ko kaise rokein",
        "EMERGENCY"
    ],
    [
        "నా బ్యాంక్ ఖాతా నుండి ఇప్పుడే రూ. 5000 కట్ అయ్యాయి, సహాయం చేయండి",
        "EMERGENCY"
    ],
    [
        "మోసగాడు నా ఖాతా నుండి 25000 రూపాయలు దొంగిలించాడు",
        "EMERGENCY"
    ],
    [
        "నేను పొరపాటున ఓటీపీ చెప్పాను, మొత్తం బ్యాలెన్స్ ఖాళీ అయిపోయింది",
        "EMERGENCY"
    ],
    [
        "ఎనీడెస్క్ డౌన్‌లోడ్ చేయించి ఖాతాలోని డబ్బులు డెబిట్ చేశారు",
        "EMERGENCY"
    ],
    [
        "నా గూగుల్ పే నుండి అనధికారికంగా రూ. 12000 పోయాయి",
        "EMERGENCY"
    ],
    [
        "Account nundi dabbu cut aipoyindi ippude",
        "EMERGENCY"
    ],
    [
        "Dabbu poyindi scam jarigindi help please",
        "EMERGENCY"
    ],
    [
        "Na bank nundi 20000 withdraw chesesaru",
        "EMERGENCY"
    ],
    [
        "నా ఖాతా నుండి ఇప్పుడే రూ. 15000 కట్ అయ్యాయి సహాయం చేయండి",
        "EMERGENCY"
    ],
    [
        "మోసగాడు నా బ్యాంక్ నుండి రూ. 50000 దొంగిలించాడు",
        "EMERGENCY"
    ],
    [
        "తక్షణ సహాయం కావాలి! నా గూగుల్ పే నుండి రూ. 20000 డెబిట్ అయ్యాయి",
        "EMERGENCY"
    ],
    [
        "ఎనీడెస్క్ ఇన్‌స్టాల్ చేసుకున్న వెంటనే రూ. 35000 పోయాయి",
        "EMERGENCY"
    ],
    [
        "ఓటీపీ చెప్పాను ఖాతాలోని బ్యాలెన్స్ మొత్తం ఖాళీ అయిపోయింది",
        "EMERGENCY"
    ],
    [
        "డిజిటల్ అరెస్ట్ అని బెదిరించి నా దగ్గర నుండి రూ. 60000 ట్రాన్స్‌ఫర్ చేయించుకున్నారు",
        "EMERGENCY"
    ],
    [
        "ఇప్పుడే నా అకౌంట్ నుండి రూ. 10000 అనధికారికంగా కట్ అయ్యాయి",
        "EMERGENCY"
    ],
    [
        "ఫేక్ కస్టమర్ కేర్ కాల్‌లో నన్ను మోసం చేసి రూ. 25000 తీసేశారు",
        "EMERGENCY"
    ],
    [
        "నా ఫోన్‌పే నుండి రూ. 8000 దొంగిలించారు",
        "EMERGENCY"
    ],
    [
        "మోసం జరిగింది నా డబ్బులు ఎలా కాపాడుకోవాలి",
        "EMERGENCY"
    ],
    [
        "hi",
        "GREETING"
    ],
    [
        "hello",
        "GREETING"
    ],
    [
        "hey",
        "GREETING"
    ],
    [
        "good morning",
        "GREETING"
    ],
    [
        "good evening",
        "GREETING"
    ],
    [
        "hello there",
        "GREETING"
    ],
    [
        "who are you",
        "GREETING"
    ],
    [
        "what is UPI Rakshak",
        "GREETING"
    ],
    [
        "what can you do for me",
        "GREETING"
    ],
    [
        "how can you help me",
        "GREETING"
    ],
    [
        "thank you so much",
        "GREETING"
    ],
    [
        "thanks a lot",
        "GREETING"
    ],
    [
        "thanks for the help",
        "GREETING"
    ],
    [
        "you are very helpful",
        "GREETING"
    ],
    [
        "bye",
        "GREETING"
    ],
    [
        "ok bye",
        "GREETING"
    ],
    [
        "hello there safety assistant",
        "GREETING"
    ],
    [
        "good day",
        "GREETING"
    ],
    [
        "hi upi rakshak",
        "GREETING"
    ],
    [
        "are you a chatbot",
        "GREETING"
    ],
    [
        "what is your purpose",
        "GREETING"
    ],
    [
        "what features do you have",
        "GREETING"
    ],
    [
        "how do you work",
        "GREETING"
    ],
    [
        "many thanks for the guidance",
        "GREETING"
    ],
    [
        "thank you very much",
        "GREETING"
    ],
    [
        "have a wonderful day",
        "GREETING"
    ],
    [
        "नमस्ते",
        "GREETING"
    ],
    [
        "नमस्कार",
        "GREETING"
    ],
    [
        "आप कौन हैं",
        "GREETING"
    ],
    [
        "आप क्या कर सकते हैं",
        "GREETING"
    ],
    [
        "बहुत बहुत धन्यवाद",
        "GREETING"
    ],
    [
        "शुक्रिया आपकी मदद के लिए",
        "GREETING"
    ],
    [
        "namaste",
        "GREETING"
    ],
    [
        "kya haal hai",
        "GREETING"
    ],
    [
        "aap kya karte ho",
        "GREETING"
    ],
    [
        "dhanyawad",
        "GREETING"
    ],
    [
        "shukriya",
        "GREETING"
    ],
    [
        "namaste rakshak",
        "GREETING"
    ],
    [
        "shubh prabhat",
        "GREETING"
    ],
    [
        "aapka swagat hai",
        "GREETING"
    ],
    [
        "aap kaun se scams check kar sakte ho",
        "GREETING"
    ],
    [
        "dhanyawad aapki jankari ke liye",
        "GREETING"
    ],
    [
        "shukriya dost",
        "GREETING"
    ],
    [
        "నమస్కారం",
        "GREETING"
    ],
    [
        "హలో",
        "GREETING"
    ],
    [
        "మీరు ఎవరు",
        "GREETING"
    ],
    [
        "మీరు నాకు ఎలా సహాయపడగలరు",
        "GREETING"
    ],
    [
        "చాలా ధన్యవాదాలు",
        "GREETING"
    ],
    [
        "మీ సహాయానికి ధన్యవాదాలు",
        "GREETING"
    ],
    [
        "namaskaram",
        "GREETING"
    ],
    [
        "dhanyavadalu",
        "GREETING"
    ],
    [
        "namaskaram andi ela unnaru",
        "GREETING"
    ],
    [
        "subhodayam",
        "GREETING"
    ],
    [
        "meeru em chestharu",
        "GREETING"
    ],
    [
        "meeru ae bhashalo matladagalaru",
        "GREETING"
    ],
    [
        "chala thanks andi mee sahayaniki",
        "GREETING"
    ],
    [
        "dhanyavadalu rakshak",
        "GREETING"
    ],
    [
        "help",
        "UNCLEAR"
    ],
    [
        "scam",
        "UNCLEAR"
    ],
    [
        "fraud",
        "UNCLEAR"
    ],
    [
        "bank",
        "UNCLEAR"
    ],
    [
        "check this",
        "UNCLEAR"
    ],
    [
        "check",
        "UNCLEAR"
    ],
    [
        "verify",
        "UNCLEAR"
    ],
    [
        "tell me",
        "UNCLEAR"
    ],
    [
        "doubt",
        "UNCLEAR"
    ],
    [
        "problem",
        "UNCLEAR"
    ],
    [
        "kuch batao",
        "UNCLEAR"
    ],
    [
        "kya karein",
        "UNCLEAR"
    ],
    [
        "sahayam",
        "UNCLEAR"
    ],
    [
        "cheppu",
        "UNCLEAR"
    ],
    [
        "em cheyali",
        "UNCLEAR"
    ],
    [
        "urgent",
        "UNCLEAR"
    ],
    [
        "please",
        "UNCLEAR"
    ],
    [
        "plz help",
        "UNCLEAR"
    ],
    [
        "what to do",
        "UNCLEAR"
    ],
    [
        "please help me",
        "UNCLEAR"
    ],
    [
        "confused",
        "UNCLEAR"
    ],
    [
        "is this ok",
        "UNCLEAR"
    ],
    [
        "need advice",
        "UNCLEAR"
    ],
    [
        "kya karu batao",
        "UNCLEAR"
    ],
    [
        "kuch samajh nahi aa raha",
        "UNCLEAR"
    ],
    [
        "madad chahiye",
        "UNCLEAR"
    ],
    [
        "samasya hai",
        "UNCLEAR"
    ],
    [
        "em cheyali cheppandi",
        "UNCLEAR"
    ],
    [
        "ardham kavatledu",
        "UNCLEAR"
    ],
    [
        "sandheham undi",
        "UNCLEAR"
    ],
    [
        "sahayam cheyandi",
        "UNCLEAR"
    ],
    [
        "chudandi",
        "UNCLEAR"
    ],
    [
        "batao na",
        "UNCLEAR"
    ]
]

TEST_INTENT_DATA = [
    ["How to cook paneer butter masala restaurant style?", "OUT_OF_SCOPE"],
    ["What is the current score of today's cricket match?", "OUT_OF_SCOPE"],
    ["Write a JavaScript script to compute factorial of a number.", "OUT_OF_SCOPE"],
    ["Tell me a creative bedtime story about an astronaut.", "OUT_OF_SCOPE"],
    ["दिल्ली में आज का तापमान कितना डिग्री है?", "OUT_OF_SCOPE"],
    ["मुझे कोई नया मजेदार चुटकुला बताइए", "OUT_OF_SCOPE"],
    ["గులాబ్ జామున్ ఎలా తయారు చేయాలి రెసిపీ చెప్పండి", "OUT_OF_SCOPE"],
    ["ఈరోజు ఇండియా మ్యాచ్ స్కోర్ ఎంత?", "OUT_OF_SCOPE"],
    ["Weather kaisa hai Delhi me aaj", "OUT_OF_SCOPE"],
    ["Who won the FIFA world cup in 2022?", "OUT_OF_SCOPE"],
    ["What is the capital of France?", "OUT_OF_SCOPE"],
    ["Write a short poem on mountains and rivers", "OUT_OF_SCOPE"],
    ["How to grow tomato plants in balcony pot?", "OUT_OF_SCOPE"],
    ["Who invented the telephone?", "OUT_OF_SCOPE"],
    ["चाय की अच्छी रेसिपी बताइए", "OUT_OF_SCOPE"],
    ["సినిమా రివ్యూ ఎలా ఉంది?", "OUT_OF_SCOPE"],
    ["Tell me lyrics of national anthem", "OUT_OF_SCOPE"],
    ["Who is prime minister of Japan?", "OUT_OF_SCOPE"],

    [
        "SBI Alert: Your YONO account blocked. Click http://sbi-kyc-fix.top to reactivate.",
        "ANALYZE"
    ],
    [
        "Dear consumer, electricity bill unpaid. Power cut at 8pm. Call JE 9988771122.",
        "ANALYZE"
    ],
    [
        "You won 10,00,000 cash prize in Dream11 lucky contest. Claim at http://dream11-prize.cc",
        "ANALYZE"
    ],
    [
        "Work 2 hrs daily from mobile, earn Rs 5000. Join t.me/telegram_job_scam",
        "ANALYZE"
    ],
    [
        "Speed post delivery failed. Update address and pay Rs 25: http://speedpost-customs.online",
        "ANALYZE"
    ],
    [
        "Collect request received: 'Accept request to receive cashback Rs 1999 from GooglePay'",
        "ANALYZE"
    ],
    [
        "Someone sent me this link: http://sbi-rewards.xyz/redeem",
        "ANALYZE"
    ],
    [
        "Please verify this UPI handle: secure-refund@okaxis",
        "ANALYZE"
    ],
    [
        "Fwd: Delhi Police cyber cell digital arrest notice issued for money laundering.",
        "ANALYZE"
    ],
    [
        "Is this genuine? 'Dear customer your SIM will be suspended tonight call 9811220099'",
        "ANALYZE"
    ],
    [
        "Aapka electricity bill baki hai, raat ko bijli kat jayegi call kare 9812345678",
        "ANALYZE"
    ],
    [
        "Mera SBI block hone ka sms aaya hai link: http://sbi-yono.top",
        "ANALYZE"
    ],
    [
        "WhatsApp pe task job ka offer mila: 3000 daily earn karo t.me/dailycash",
        "ANALYZE"
    ],
    [
        "Ye link check kariye: http://paytm-pan-kyc.site",
        "ANALYZE"
    ],
    [
        "KBC ka lottery letter bheja hai kisi ne 25 lakh ka",
        "ANALYZE"
    ],
    [
        "మీ ఎస్బీఐ ఖాతా నిలిపివేయబడింది. ఈ లింక్ క్లిక్ చేయండి: http://sbi-bank-kyc.top",
        "ANALYZE"
    ],
    [
        "విద్యుత్ సరఫరా నిలిపివేత మెసేజ్ వచ్చింది: 9876501234 కి కాల్ చేయమన్నారు",
        "ANALYZE"
    ],
    [
        "ఈ యూపీఐ ఐడీ తనిఖీ చేయండి: refund-support@ybl",
        "ANALYZE"
    ],
    [
        "ఫోన్‌పే లో రూ. 3000 క్యాష్‌బ్యాక్ కోసం పిన్ కొట్టమంటున్నారు",
        "ANALYZE"
    ],
    [
        "కొరియర్ డెలివరీ ఫెయిల్ అయిందని ఈ లింక్ వచ్చింది: http://india-courier.xyz",
        "ANALYZE"
    ],
    [
        "http://192.168.0.1/sbi/verify.php",
        "ANALYZE"
    ],
    [
        "https://axis-reward-points.online/claim",
        "ANALYZE"
    ],
    [
        "check this QR: payment to unknown merchant qr image",
        "ANALYZE"
    ],
    [
        "SMS says: 'Dear user your account debited with Rs 49999 to Flipkart if not you call 9876543210'",
        "ANALYZE"
    ],
    [
        "Fake customer care handle refund@paytm",
        "ANALYZE"
    ],
    [
        "Dear customer your PNB account will expire today. Update KYC: http://pnb-yono.top",
        "ANALYZE"
    ],
    [
        "DHVBN electricity bill unpaid. Power disconnected tonight. Call officer on 9811223344.",
        "ANALYZE"
    ],
    [
        "You have won Rs 5,00,000 cash prize in Jio anniversary contest. Claim at bit.ly/jio-win",
        "ANALYZE"
    ],
    [
        "Work from home: 2000 daily for telegram reviews. Join t.me/job_fast_cash",
        "ANALYZE"
    ],
    [
        "India Post parcel detained due to incomplete address. Pay Rs 25 at http://indiapost-parcel.site",
        "ANALYZE"
    ],
    [
        "SBI Collect Request received for Rs 3499 cashback reward refund.",
        "ANALYZE"
    ],
    [
        "Please scan this QR code to receive Rs 2500 refund from PhonePe support",
        "ANALYZE"
    ],
    [
        "Verify this UPI handle: sbi-helpdesk@okhdfcbank",
        "ANALYZE"
    ],
    [
        "Cyber cell warrant issued against you for narcotics parcel. Contact on WhatsApp video.",
        "ANALYZE"
    ],
    [
        "Bank SMS says: VK-HDFCBK: Your card locked due to suspicious activity. Call 9876543210.",
        "ANALYZE"
    ],
    [
        "Bijli vibhag: Bill jama karein warna light kat jayegi 9876501234 pe call karo",
        "ANALYZE"
    ],
    [
        "KBC lottery ka message mila hai 25 lakh wala: http://kbc-draw.top",
        "ANALYZE"
    ],
    [
        "Aapka SBI account suspend hone wala hai kyc karein http://sbi-pan-kyc.cc",
        "ANALYZE"
    ],
    [
        "OLX pe buyer ne kaha ye QR scan karo paise lene ke liye",
        "ANALYZE"
    ],
    [
        "Courier tracking SMS: http://dhl-customs.online pe 50 rs pay karo",
        "ANALYZE"
    ],
    [
        "ఎస్బీఐ ఖాతా బ్లాక్ చేయబడుతుంది. వెంటనే ఈ లింక్ ఓపెన్ చేయండి: http://sbi-secure.xyz",
        "ANALYZE"
    ],
    [
        "కరెంట్ బిల్లు చెల్లించనందున విద్యుత్ సరఫరా ఆగిపోతుంది 9876543210 కి కాల్ చేయండి",
        "ANALYZE"
    ],
    [
        "లాటరీలో రూ. 5 లక్షలు గెలుచుకున్నారు క్లెయిమ్ లింక్: http://lottery-win.top",
        "ANALYZE"
    ],
    [
        "ఈ యూపీఐ నంబర్ కి డబ్బులు పంపమని మెసేజ్ వచ్చింది: 9876543210@paytm",
        "ANALYZE"
    ],
    [
        "కొరియర్ పార్సెల్ చిరునామా సరిచేయడానికి రూ. 20 కట్టమని లింక్ వచ్చింది: http://post.site",
        "ANALYZE"
    ],
    [
        "how to compliant to 1930",
        "HELP"
    ],
    [
        "how to complain to 1930",
        "HELP"
    ],
    [
        "how do I report on cybercrime.gov.in",
        "HELP"
    ],
    [
        "how to bloack my upi id",
        "HELP"
    ],
    [
        "how to block upi id in phonepe",
        "HELP"
    ],
    [
        "what is digital arrest",
        "HELP"
    ],
    [
        "how do collect requests work",
        "HELP"
    ],
    [
        "how to verify if bank sms is real",
        "HELP"
    ],
    [
        "is entering upi pin required to receive money",
        "HELP"
    ],
    [
        "what should I prepare before calling 1930 helplne",
        "HELP"
    ],
    [
        "how to report scam on cybercrime portal",
        "HELP"
    ],
    [
        "what is golden hour protocol in cyber crime",
        "HELP"
    ],
    [
        "how to protect my bank account from fraud",
        "HELP"
    ],
    [
        "how to report fake WhatsApp caller to Chakshu",
        "HELP"
    ],
    [
        "can CBI arrest through video call",
        "HELP"
    ],
    [
        "what is rbi zero liability rule",
        "HELP"
    ],
    [
        "how to change my upi pin in gpay",
        "HELP"
    ],
    [
        "how to check if sms header is genuine",
        "HELP"
    ],
    [
        "how to recover scammed money from bank",
        "HELP"
    ],
    [
        "what to do if I installed anydesk app",
        "HELP"
    ],
    [
        "1930 pe shikayat kaise kare",
        "HELP"
    ],
    [
        "cybercrime portal pe report kaise karte hain",
        "HELP"
    ],
    [
        "upi id block kaise karein",
        "HELP"
    ],
    [
        "kya paise lene ke liye pin dalna padta h",
        "HELP"
    ],
    [
        "digital arrest ka kya matlab hota hai",
        "HELP"
    ],
    [
        "fake customer care number kaise pehchane",
        "HELP"
    ],
    [
        "anydesk install ho gaya to kya kare",
        "HELP"
    ],
    [
        "1930 helpline pe kya documents lagte hain",
        "HELP"
    ],
    [
        "1930 lo complaint ela ivvali",
        "HELP"
    ],
    [
        "cybercrime.gov.in lo report ela cheyyali",
        "HELP"
    ],
    [
        "upi id block cheyadam ela",
        "HELP"
    ],
    [
        "digital arrest ante ento cheppandi",
        "HELP"
    ],
    [
        "collect request ante enti",
        "HELP"
    ],
    [
        "dabbu teesukovadaniki upi pin kottala",
        "HELP"
    ],
    [
        "fake bank sms ni ela gurtinchali",
        "HELP"
    ],
    [
        "1930 ki call chese mundu em ready chesukovali",
        "HELP"
    ],
    [
        "anydesk app delete cheste saripotunda",
        "HELP"
    ],
    [
        "bank nundi dabbu recovery cheyadam ela",
        "HELP"
    ],
    [
        "how to compliant to 1930 helplne",
        "HELP"
    ],
    [
        "how do i report on cybercrime.gov.in portal",
        "HELP"
    ],
    [
        "how to bloack my upi id in phonepe",
        "HELP"
    ],
    [
        "how to block upi id in gpay and paytm",
        "HELP"
    ],
    [
        "what is digital arrest scam in india",
        "HELP"
    ],
    [
        "how do collect requests work in upi",
        "HELP"
    ],
    [
        "do i need to enter upi pin to receive money",
        "HELP"
    ],
    [
        "how to verify if bank sms is genuine or fake",
        "HELP"
    ],
    [
        "what should i prepare before calling 1930 helpline",
        "HELP"
    ],
    [
        "what to do if i installed anydesck screen share app",
        "HELP"
    ],
    [
        "what to do if i accidentally shared my otp with fraudster",
        "HELP"
    ],
    [
        "how to freeze bank account immediately after scam",
        "HELP"
    ],
    [
        "what is golden hour recovery protocol",
        "HELP"
    ],
    [
        "how to report fraud caller on Chakshu portal",
        "HELP"
    ],
    [
        "is upi payment safe for online buyers",
        "HELP"
    ],
    [
        "1930 pe complaint kaise karein",
        "HELP"
    ],
    [
        "cybercrime portal pe report darj karne ka tarika",
        "HELP"
    ],
    [
        "upi id block kaise karte hain",
        "HELP"
    ],
    [
        "kya paise lene ke liye upi pin dalna padta hai",
        "HELP"
    ],
    [
        "digital arrest kya sach me hota hai",
        "HELP"
    ],
    [
        "fake bank sms ko pehchanne ka tarika",
        "HELP"
    ],
    [
        "agar otp de diya to turant kya karein",
        "HELP"
    ],
    [
        "anydesk install ho jaye to phone safe kaise kare",
        "HELP"
    ],
    [
        "1930 par call karne se pehle kya ready rakhein",
        "HELP"
    ],
    [
        "bank account ko freeze kaise karwaye",
        "HELP"
    ],
    [
        "1930 lo complain ela ivvali",
        "HELP"
    ],
    [
        "cybercrime portal lo case ela file cheyyali",
        "HELP"
    ],
    [
        "upi id ni ela block cheyali",
        "HELP"
    ],
    [
        "డబ్బులు స్వీకరించడానికి యూపీఐ పిన్ కొట్టాలా",
        "HELP"
    ],
    [
        "డిజిటల్ అరెస్ట్ అంటే ఏమిటి నిజమైన పోలీసులా",
        "HELP"
    ],
    [
        "నకిలీ బ్యాంక్ మెసేజ్‌లను ఎలా ధృవీకరించాలి",
        "HELP"
    ],
    [
        "ఎవరికైనా ఓటీపీ చెబితే తక్షణమే ఏం చేయాలి",
        "HELP"
    ],
    [
        "ఎనీడెస్క్ యాప్ ఇన్‌స్టాల్ చేసుకుంటే దాన్ని ఎలా తొలగించాలి",
        "HELP"
    ],
    [
        "1930 కాల్ చేసే ముందు ఏ వివరాలు కావాలి",
        "HELP"
    ],
    [
        "బ్యాంక్ ఖాతాను వెంటనే ఫ్రీజ్ చేయడం ఎలా",
        "HELP"
    ],
    [
        "I lost 5000 rupees",
        "EMERGENCY"
    ],
    [
        "I lost 10000 rupees to a fraudster",
        "EMERGENCY"
    ],
    [
        "Money debited without my consent from account",
        "EMERGENCY"
    ],
    [
        "Scammer stole 15000 from my GPay",
        "EMERGENCY"
    ],
    [
        "I shared OTP and 20000 debited immediately",
        "EMERGENCY"
    ],
    [
        "I installed AnyDesk and my entire bank balance was deducted",
        "EMERGENCY"
    ],
    [
        "Fraud happened just now, 50000 taken from my SBI account",
        "EMERGENCY"
    ],
    [
        "Emergency! 8000 rupees debited from my card",
        "EMERGENCY"
    ],
    [
        "Someone approved a fake collect request of Rs 12000 on my phone",
        "EMERGENCY"
    ],
    [
        "A digital arrest caller forced me to transfer 1 lakh rupees",
        "EMERGENCY"
    ],
    [
        "Mere account se 5000 rupaye cut gaye fraud me",
        "EMERGENCY"
    ],
    [
        "Paisa kat gaya account se turant madad karo",
        "EMERGENCY"
    ],
    [
        "Scammer ne 20000 nikal liye mere bank se",
        "EMERGENCY"
    ],
    [
        "Maine otp de diya aur 15000 debit ho gaya",
        "EMERGENCY"
    ],
    [
        "AnyDesk daal diya aur paise gayab ho gaye",
        "EMERGENCY"
    ],
    [
        "Na bank nundi 5000 cut aipoyayi",
        "EMERGENCY"
    ],
    [
        "Dabbu poyindi scam lo 10000 deduct chesaru",
        "EMERGENCY"
    ],
    [
        "Ippude na account nundi 25000 withdraw ayyayi",
        "EMERGENCY"
    ],
    [
        "Nenu otp cheppanu dabbu mottam poyindi",
        "EMERGENCY"
    ],
    [
        "Help me scammed 30000 rupees right now",
        "EMERGENCY"
    ],
    [
        "I lost 12000 rupees to a scammer 15 minutes ago",
        "EMERGENCY"
    ],
    [
        "Someone debited 45000 from my bank account without permission",
        "EMERGENCY"
    ],
    [
        "Emergency! My bank balance was emptied by fake customer care",
        "EMERGENCY"
    ],
    [
        "I gave my OTP on phishing site and 25000 was deducted immediately",
        "EMERGENCY"
    ],
    [
        "I installed AnyDesk on my phone and 40000 rupees was transferred out",
        "EMERGENCY"
    ],
    [
        "Scammer forced me to pay 50000 for digital arrest threat",
        "EMERGENCY"
    ],
    [
        "Money was debited from my HDFC account right now help me",
        "EMERGENCY"
    ],
    [
        "Mere account se 12000 rupaye cut gaye fraud me",
        "EMERGENCY"
    ],
    [
        "Kisi ne mere 45000 nikal liye bank se turant roko",
        "EMERGENCY"
    ],
    [
        "Maine caller ko OTP diya aur saare paise chale gaye",
        "EMERGENCY"
    ],
    [
        "AnyDesk install kiya aur 35000 rupaye gayab ho gaye",
        "EMERGENCY"
    ],
    [
        "Digital arrest ke naam par 50000 le liye scammer ne",
        "EMERGENCY"
    ],
    [
        "నా బ్యాంక్ నుండి రూ. 12000 ఇప్పుడే కట్ అయ్యాయి సహాయం చేయండి",
        "EMERGENCY"
    ],
    [
        "మోసగాడు నా ఖాతా నుండి రూ. 45000 తీసేశాడు",
        "EMERGENCY"
    ],
    [
        "నేను పొరపాటున ఓటీపీ చెప్పాను రూ. 20000 పోయాయి",
        "EMERGENCY"
    ],
    [
        "ఎనీడెస్క్ ద్వారా నా ఫోన్ నుండి రూ. 30000 దొంగిలించారు",
        "EMERGENCY"
    ],
    [
        "డిజిటల్ అరెస్ట్ భయంతో రూ. 50000 పంపేశాను సహాయం కావాలి",
        "EMERGENCY"
    ],
    [
        "hi there",
        "GREETING"
    ],
    [
        "hello assistant",
        "GREETING"
    ],
    [
        "hey buddy",
        "GREETING"
    ],
    [
        "good morning assistant",
        "GREETING"
    ],
    [
        "who built you",
        "GREETING"
    ],
    [
        "what is your name",
        "GREETING"
    ],
    [
        "what are your capabilities",
        "GREETING"
    ],
    [
        "thanks a lot for this info",
        "GREETING"
    ],
    [
        "thank you assistant",
        "GREETING"
    ],
    [
        "namaste ji",
        "GREETING"
    ],
    [
        "namaskaram andi",
        "GREETING"
    ],
    [
        "aapka naam kya hai",
        "GREETING"
    ],
    [
        "bahut dhanyawad",
        "GREETING"
    ],
    [
        "meeru evaru",
        "GREETING"
    ],
    [
        "chala thanks andi",
        "GREETING"
    ],
    [
        "bye bye",
        "GREETING"
    ],
    [
        "hello assistant can you help me",
        "GREETING"
    ],
    [
        "good afternoon upi rakshak",
        "GREETING"
    ],
    [
        "what are you capable of doing",
        "GREETING"
    ],
    [
        "thank you for your prompt response",
        "GREETING"
    ],
    [
        "thanks a lot buddy",
        "GREETING"
    ],
    [
        "namaste kaise ho aap",
        "GREETING"
    ],
    [
        "bahut bahut shukriya aapka",
        "GREETING"
    ],
    [
        "aap kya kya check kar sakte ho",
        "GREETING"
    ],
    [
        "namaskaram meeru ela unnaru",
        "GREETING"
    ],
    [
        "chala thanks andi mee sahayaniki",
        "GREETING"
    ],
    [
        "meeru ememi check chestaru",
        "GREETING"
    ],
    [
        "help me",
        "UNCLEAR"
    ],
    [
        "check please",
        "UNCLEAR"
    ],
    [
        "doubt",
        "UNCLEAR"
    ],
    [
        "scam?",
        "UNCLEAR"
    ],
    [
        "fraud?",
        "UNCLEAR"
    ],
    [
        "bank alert",
        "UNCLEAR"
    ],
    [
        "what to do",
        "UNCLEAR"
    ],
    [
        "kuch samjh nahi aaya",
        "UNCLEAR"
    ],
    [
        "kya karu",
        "UNCLEAR"
    ],
    [
        "em cheyalo cheppu",
        "UNCLEAR"
    ],
    [
        "sahayam kavali",
        "UNCLEAR"
    ],
    [
        "urgent help",
        "UNCLEAR"
    ],
    [
        "confused",
        "UNCLEAR"
    ],
    [
        "query",
        "UNCLEAR"
    ],
    [
        "help needed",
        "UNCLEAR"
    ],
    [
        "doubt regarding bank",
        "UNCLEAR"
    ],
    [
        "fraud alert check",
        "UNCLEAR"
    ],
    [
        "not sure what to do",
        "UNCLEAR"
    ],
    [
        "plz help",
        "UNCLEAR"
    ],
    [
        "kuch madad chahiye",
        "UNCLEAR"
    ],
    [
        "samajh nahi aa raha",
        "UNCLEAR"
    ],
    [
        "sahayam kavali andi",
        "UNCLEAR"
    ],
    [
        "em cheyali",
        "UNCLEAR"
    ]
]
