import os
import json

# 165 Hand-crafted, natural, messy, human-style gold benchmark samples
# Covering English, Hindi, Telugu, Hinglish, and Romanized Telugu
# Across all 15 fraud categories + legitimate hard negatives
GOLD_V2_SAMPLES = [
    # --- LEGITIMATE HARD NEGATIVES (35 samples) ---
    {
        "id": "gold_v2_legit_001",
        "text": "SBI: Rs 3,200.00 debited from A/c XX8921 on 21/11/26 via UPI to Zomato. UPI Ref 632190123456. Available Bal: Rs 18,430.50. If not done by you, forward SMS to 9223008333 or call 1800111109 immediately.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "bank_debit_alert"
    },
    {
        "id": "gold_v2_legit_002",
        "text": "Dear Customer, 592014 is your One Time Password (OTP) for verifying your mobile number on Amazon India. Valid for 15 mins. NEVER disclose your OTP to anyone over call or SMS.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "otp_alert"
    },
    {
        "id": "gold_v2_legit_003",
        "text": "Canara Bank Alert: Your a/c *5541 has been credited with Rs 45,000.00 on 21-Nov-2026 by NEFT salary credit from INFOSYS LTD. Total Avail Bal Rs 62,310.00.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "salary_credit"
    },
    {
        "id": "gold_v2_legit_004",
        "text": "Tata Power-DDL: Bill for CA 60012938491 for Nov-26 is Rs 2,340. Due date 02-Dec-2026. Avail 1.2% rebate by paying digitally at https://www.tatapower-ddl.com before due date.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "utility_bill"
    },
    {
        "id": "gold_v2_legit_005",
        "text": "Hi Rahul, sharing the QR code for our chai stall. You can scan to pay Rs 40 via PhonePe or GPay. Thank you bhaiya!",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "genuine_merchant_qr"
    },
    {
        "id": "gold_v2_legit_006",
        "text": "Paid Rs 350 to Sharma General Store via UPI. Transaction successful. UPI Ref No 432198765432. Date: 21 Nov 2026, 14:32 IST.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "upi_receipt"
    },
    {
        "id": "gold_v2_legit_007",
        "text": "HDFC Bank NetBanking Security Tip: Always verify that the address bar displays https://netbanking.hdfcbank.com before typing credentials. We never ask for PIN or passwords.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "security_advisory"
    },
    {
        "id": "gold_v2_legit_008",
        "text": "Flipkart: Your package with order ID OD3920194012 containing Wireless Earbuds has been dispatched via Ekart Logistics. Track at https://www.flipkart.com",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "courier_notice"
    },
    {
        "id": "gold_v2_legit_009",
        "text": "Axis Bank: Rs. 1500 debited from card ending 4019 at D-Mart Bangalore. If this transaction was not authorized by you, block your card instantly via Axis Mobile app.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "card_alert"
    },
    {
        "id": "gold_v2_legit_010",
        "text": "Airtel Thanks: Your recharge of Rs 839 (84 Days, 2GB/day) is successful. Pack validity until 13-Feb-2027. Manage your account on Airtel Thanks app.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "telecom_recharge"
    },
    {
        "id": "gold_v2_legit_011",
        "text": "प्रिय ग्राहक, आपके बैंक खाते से ₹1,200 का भुगतान UPI के माध्यम से सफल रहा। शेष राशि: ₹14,250। किसी भी व्यक्ति के साथ अपना UPI पिन या OTP साझा न करें।",
        "category": "legitimate",
        "language": "hi",
        "is_hard_negative": True,
        "style": "hindi_bank_alert"
    },
    {
        "id": "gold_v2_legit_012",
        "text": "दक्षिण हरियाणा बिजली वितरण निगम (DHBVN): खाता संख्या 10928374 के लिए आपका बिजली बिल ₹1,850 है। देय तिथि 29-Nov-2026। आधिकारिक पोर्टल dhbvn.org.in पर भुगतान करें।",
        "category": "legitimate",
        "language": "hi",
        "is_hard_negative": True,
        "style": "hindi_utility_bill"
    },
    {
        "id": "gold_v2_legit_013",
        "text": "स्टेट बैंक ऑफ इंडिया: आपका नेटबैंकिंग लॉगिन OTP 492018 है। यह 5 मिनट के लिए वैध है। बैंक कभी भी आपका पासवर्ड या ओटीपी नहीं मांगता।",
        "category": "legitimate",
        "language": "hi",
        "is_hard_negative": True,
        "style": "hindi_otp"
    },
    {
        "id": "gold_v2_legit_014",
        "text": "ప్రియమైన ఎస్బీఐ కస్టమర్, మీ ఖాతా నెంబర్ XX4019 నుండి స్విగ్గీకి రూ. 450 యుపిఐ ద్వారా చెల్లించబడింది. మీ నిల్వ: రూ. 8,920. ఓటీపీ ఎవరికీ చెప్పవద్దు.",
        "category": "legitimate",
        "language": "te",
        "is_hard_negative": True,
        "style": "telugu_bank_alert"
    },
    {
        "id": "gold_v2_legit_015",
        "text": "టీఎస్ఎస్పీడీసీఎల్ (TSSPDCL): మీ విద్యుత్ బిల్లు సర్వీస్ నెం 102938 కు రూ. 950. గడువు తేదీ: 27-Nov-2026. అధికారిక యాప్ tssouthernpower.com లో చెల్లించండి.",
        "category": "legitimate",
        "language": "te",
        "is_hard_negative": True,
        "style": "telugu_utility"
    },
    {
        "id": "gold_v2_legit_016",
        "text": "Bhai maine sham ko party ke 400 rupaye GPay kar diye the, dekh lo balance update hua kya.",
        "category": "legitimate",
        "language": "hi",
        "is_hard_negative": False,
        "style": "hinglish_chat"
    },
    {
        "id": "gold_v2_legit_017",
        "text": "Anna nenu neeku Google Pay lo Rs 1500 pampanu, account check chesko receipt screenshot kooda WhatsApp chesa.",
        "category": "legitimate",
        "language": "te",
        "is_hard_negative": False,
        "style": "roman_telugu_chat"
    },
    {
        "id": "gold_v2_legit_018",
        "text": "IRCTC: PNR 4820194821 Booking Confirmed. Train 12723 Telangana Exp, 23-Nov-2026. Coach B3 Berth 24 (MB). Happy Journey!",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "railway_booking"
    },
    {
        "id": "gold_v2_legit_019",
        "text": "Swiggy order #910294 delivered. Rate your delivery partner Ramesh on the Swiggy app. Hope you enjoyed the meal!",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "delivery_notice"
    },
    {
        "id": "gold_v2_legit_020",
        "text": "Uber trip receipt: You rode with Suresh for Rs 240.50 on 21-Nov. Paid via Paytm UPI. Invoice sent to your registered email.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "cab_receipt"
    },
    {
        "id": "gold_v2_legit_021",
        "text": "Dear customer, your request for Cheque Book dispatch for a/c ending 1029 has been processed. Dispatch tracking via India Post: EM492019201IN.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "bank_service_notice"
    },
    {
        "id": "gold_v2_legit_022",
        "text": "Your CIBIL Score has been refreshed for November 2026: 785 (Excellent). Log in to your bank portal to view your free annual report.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "credit_score"
    },
    {
        "id": "gold_v2_legit_023",
        "text": "Kotak Mahindra Bank: Rs 5,000 withdrawn from ATM at MG Road Bangalore on 21-Nov-26 18:20. Avail Bal: Rs 42,100. Call 18602662666 if not you.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "atm_withdrawal"
    },
    {
        "id": "gold_v2_legit_024",
        "text": "Amazon Delivery: Package will be delivered today by Manoj. Share delivery secret OTP 3841 with delivery agent only upon physical inspection.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "delivery_pin"
    },
    {
        "id": "gold_v2_legit_025",
        "text": "Indane Gas: Booking confirmation for Refill order 90129482. Subsidy will be directly credited to your Aadhaar linked bank a/c.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "gas_booking"
    },
    {
        "id": "gold_v2_legit_026",
        "text": "LIC of India: Premium of Rs 14,200 for policy 684920192 is due on 05-Dec-2026. Pay safely through licindia.in customer portal.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "insurance_notice"
    },
    {
        "id": "gold_v2_legit_027",
        "text": "Zerodha: Rs 20,000 transferred from HDFC bank to your trading account. Fund margin available for equity trades.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "brokerage_credit"
    },
    {
        "id": "gold_v2_legit_028",
        "text": "Apollo Pharmacy: Thank you for shopping with us! Bill Amount: Rs 640. Paid via GPay. Medicines will be delivered in 2 hrs.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "store_receipt"
    },
    {
        "id": "gold_v2_legit_029",
        "text": "BSNL Landline/Fiber bill for tele 040-23456789 is Rs 943. Pay before 01-Dec to avoid late fees. Portal: portal.bsnl.in.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "broadband_bill"
    },
    {
        "id": "gold_v2_legit_030",
        "text": "EPFO: Your monthly PF contribution of Rs 3,600 has been credited to UAN 100928374821 by employer for month Oct-2026.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "epfo_notice"
    },
    {
        "id": "gold_v2_legit_031",
        "text": "BigBasket: Order BB-849201 dispatched. Total invoice Rs 1,890. Paid online via UPI. Contact customer care in app for assistance.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "grocery_order"
    },
    {
        "id": "gold_v2_legit_032",
        "text": "PNB SMS: OTP for Net Banking registration is 921402. Never share with anybody. PNB official helpline 1800-180-2222.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "pnb_otp"
    },
    {
        "id": "gold_v2_legit_033",
        "text": "Post Office Savings Bank: Interest of Rs 480 credited to account 8920194 for Q3 FY26. Visit indiapost.gov.in for passbook update.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "post_office"
    },
    {
        "id": "gold_v2_legit_034",
        "text": "BookMyShow: Booking confirmed! 2 Tickets for Kalki at PVR Forum Hyderabad on 22 Nov 7:30 PM. Screen 4, Seats F12-F13. Enjoy the show!",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": False,
        "style": "ticket_booking"
    },
    {
        "id": "gold_v2_legit_035",
        "text": "UPI Alert: Automatic mandate of Rs 299 for Netflix Entertainment set for 25th of every month. Cancel anytime in your UPI app.",
        "category": "legitimate",
        "language": "en",
        "is_hard_negative": True,
        "style": "mandate_alert"
    },

    # --- MARKETPLACE / OLX FAKE QR SCAMS (15 samples) ---
    {
        "id": "gold_v2_mkt_001",
        "text": "Sir I want to purchase your second hand refrigerator on OLX. I am Army officer posted in cantonment. Sending you official Army payment QR code. Scan it and enter UPI PIN to get Rs 12000 advance.",
        "category": "marketplace_qr_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "army_buyer_qr"
    },
    {
        "id": "gold_v2_mkt_002",
        "text": "Bhai OLX pe aapka dining table final hai. Mai abhi advance 8000 rupaye bhej raha hu. Ye lo barcode scan karo aur apna 4 digit UPI pin daalo, turant account me credit hoga.",
        "category": "marketplace_qr_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "olx_hinglish_qr"
    },
    {
        "id": "gold_v2_mkt_003",
        "text": "Mee Quikr washing machine nenu kontanu sir. Nenu advance ga Rs 6000 QR code pampanu. Meeru PhonePe lo scan chesi PIN kodithe meeku payment release avthundi.",
        "category": "marketplace_qr_scam",
        "language": "te",
        "is_hard_negative": False,
        "style": "quikr_telugu_qr"
    },
    {
        "id": "gold_v2_mkt_004",
        "text": "Hello, saw your sofa ad on Facebook Marketplace. Will pay full Rs 15000 right now. I have sent merchant collect QR code. Scan QR code to accept and receive amount into your bank.",
        "category": "marketplace_qr_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "fb_marketplace_qr"
    },
    {
        "id": "gold_v2_mkt_005",
        "text": "Sir army quota purchase department se bol raha hu. Aapke bike ka deal pakka. Ye receiving QR code hai, isko scan karke PIN enter kijiye payment receive karne ke liye.",
        "category": "marketplace_qr_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "army_quota_qr"
    },
    {
        "id": "gold_v2_mkt_006",
        "text": "I am sending a verified merchant QR code for OLX buyer protection. Open GPay -> scan image -> enter UPI PIN -> Rs 20000 will be credited directly to your savings account.",
        "category": "marketplace_qr_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "merchant_protection_qr"
    },
    {
        "id": "gold_v2_mkt_007",
        "text": "Bhaiya maine galti se Rs 50 ka test payment kiya tha na wo aa gaya. Ab baki 14000 lene ke liye ye bada QR scan karke apna PIN daaliye receive ho jayega.",
        "category": "marketplace_qr_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "two_step_qr_trap"
    },
    {
        "id": "gold_v2_mkt_008",
        "text": "OLX Customer Safe Trade: You have an incoming escrow payment of Rs 18500. Scan the transaction QR code and input security UPI PIN to claim escrow fund to your bank.",
        "category": "marketplace_qr_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "escrow_fake_qr"
    },
    {
        "id": "gold_v2_mkt_009",
        "text": "Nenu CISF security officer ni sir, mee laptop deal confirm. Nenu military canteen QR code pampisthunna, scan chesi UPI PIN enter chesi Rs 25000 collect chesukondi.",
        "category": "marketplace_qr_scam",
        "language": "te",
        "is_hard_negative": False,
        "style": "cisf_canteen_qr"
    },
    {
        "id": "gold_v2_mkt_010",
        "text": "Buyer transferred Rs 7500 for your old mobile on Cashify. To accept incoming money, open scanner, scan this barcode and type secret UPI PIN.",
        "category": "marketplace_qr_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "cashify_buyer_qr"
    },
    {
        "id": "gold_v2_mkt_011",
        "text": "Sir aap payment receive karne se dar kyu rahe ho? Scan karke PIN dalna compulsory hota hai govt server se receive karne ke liye. Jaldi scan karo warna order cancel.",
        "category": "marketplace_qr_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "coercive_qr_chat"
    },
    {
        "id": "gold_v2_mkt_012",
        "text": "Dear Seller, scan the OLX Verified Pay QR to receive your payment of ₹9,000 for Bedroom Wardrobe. You must authorise with PIN to receive money.",
        "category": "marketplace_qr_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "olx_verified_qr"
    },
    {
        "id": "gold_v2_mkt_013",
        "text": "Mee car tyre set nenu theesukuntanu. Nenu QR code WhatsApp chesa. Scan chesi PIN enter chesthe account lo credit paduthundi chudandi.",
        "category": "marketplace_qr_scam",
        "language": "te",
        "is_hard_negative": False,
        "style": "car_parts_qr"
    },
    {
        "id": "gold_v2_mkt_014",
        "text": "PhonePe Reverse Collect Payment: Someone wants to pay you Rs 5500. Scan QR code attached or approve collect request by typing your 6-digit MPIN.",
        "category": "marketplace_qr_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "reverse_collect_qr"
    },
    {
        "id": "gold_v2_mkt_015",
        "text": "Google Pay Merchant Settlement: Buyer scanned your shop board. To accept Rs 11,200 into current a/c, scan refund bar code and authenticate with UPI PIN.",
        "category": "marketplace_qr_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "merchant_settle_qr"
    },

    # --- COURIER / CUSTOMS / DIGITAL ARREST SCAMS (10 samples) ---
    {
        "id": "gold_v2_courier_001",
        "text": "FEDEX NARCOTICS CELL: A parcel booked under your Aadhaar number containing 16 MDMA passports and contraband was intercepted at Mumbai International Airport. CBI arrest warrant issued. Contact Narcotics Inspector Sharma on Skype immediately to clear charges or pay security deposit: http://customs-narcotics-clearance.top",
        "category": "courier_customs_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "digital_arrest_fedex"
    },
    {
        "id": "gold_v2_courier_002",
        "text": "DHL Alert: Your overseas parcel from UK with tracking #DHL849201 is detained at Delhi Customs due to undeclared foreign currency and gold jewelry. Pay customs tax Rs 48,500 immediately to RBI nodal a/c via UPI to prevent police FIR: http://delhi-customs-duty.xyz",
        "category": "courier_customs_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "customs_duty_gold"
    },
    {
        "id": "gold_v2_courier_003",
        "text": "Mumbai Crime Branch: Aapke naam se Taiwan parcel me 5 fake passports aur drugs mile hain. Supreme Court ne digital arrest order pass kiya hai. Turant police verification fee 35,000 UPI karein warna ghar pe raid hogi.",
        "category": "courier_customs_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "crime_branch_digital_arrest"
    },
    {
        "id": "gold_v2_courier_004",
        "text": "హైదరాబాద్ సైబర్ క్రైమ్ పోలీస్ నోటీస్: మీ ఆధార్ కార్డ్ ఉపయోగించి మలేషియా నుండి డ్రగ్స్ పార్సెల్ వచ్చింది. మీ పై నాన్ బెయిలబుల్ వారెంట్ జారీ చేయబడింది. అరెస్ట్ తప్పించుకోవడానికి వెంటనే రూ. 50,000 సెక్యూరిటీ డిపాజిట్ చేయండి: http://cybercrime-police-clearance.top",
        "category": "courier_customs_scam",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_digital_arrest"
    },
    {
        "id": "gold_v2_courier_005",
        "text": "India Post Urgent: Your Speed Post parcel is held at central hub due to invalid house number and pending customs clearance of Rs 149. Click link to update address and pay duty: http://indiapost-parcel-delivery.online",
        "category": "courier_customs_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "india_post_smishing"
    },
    {
        "id": "gold_v2_courier_006",
        "text": "BlueDart Express: Consignment #BD901284 detained by Enforcement Directorate (ED) for money laundering audit. Join video call for verification or transfer clearance fee to reserve officer VPA ed-clearance@ybl.",
        "category": "courier_customs_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "ed_money_laundering"
    },
    {
        "id": "gold_v2_courier_007",
        "text": "CBI Cyber Wing: Your phone number is linked to illegal money laundering courier dispatch in Cambodia. Connect to Skype room CBI_INVESTIGATION_04 immediately for virtual interrogation and bail fee transfer.",
        "category": "courier_customs_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "cbi_skype_interrogation"
    },
    {
        "id": "gold_v2_courier_008",
        "text": "Aapka FedEx parcel hold par hai kyunki usme 500 gram banned chemical paya gaya hai. Police complaint darj ho chuki hai. Case close karne ke liye investigation officer ko 25000 UPI karein.",
        "category": "courier_customs_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "banned_chemical_parcel"
    },
    {
        "id": "gold_v2_courier_009",
        "text": "Customs Commissionerate Bangalore: Luxury watch gift parcel arrived from Dubai for your name. Clearance duty of Rs 28,400 must be remitted within 4 hours or parcel confiscated and tax evasion charges pressed.",
        "category": "courier_customs_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "dubai_gift_parcel"
    },
    {
        "id": "gold_v2_courier_010",
        "text": "Delhi Police Narcotics Department: Digital arrest initiated for 48 hours. Do not disconnect phone call. Transfer complete bank funds to Supreme Court holding account for forensic audit: http://court-escrow-audit.online",
        "category": "courier_customs_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "digital_arrest_escrow"
    },

    # --- LOAN APP EXTORTION / HARASSMENT (10 samples) ---
    {
        "id": "gold_v2_loan_001",
        "text": "FINAL WARNING! You took loan of Rs 5000 from RupeeFast app. Now you owe Rs 28,000 with penalty. If you do not pay within 30 minutes, we will send your morphed nude photos and contact list to your mother, sister, and WhatsApp groups: http://rupeefast-clear-loan.xyz",
        "category": "loan_app_extortion",
        "language": "en",
        "is_hard_negative": False,
        "style": "morphed_photo_blackmail"
    },
    {
        "id": "gold_v2_loan_002",
        "text": "Tu 15000 rupaye turant is UPI id pe bhej nahi toh tere phone ki puri contact list par message dalenge ki tu 420 chor fraud hai aur teri behan ki photo viral karenge: recovery-loan@paytm",
        "category": "loan_app_extortion",
        "language": "hi",
        "is_hard_negative": False,
        "style": "hindi_loan_threat"
    },
    {
        "id": "gold_v2_loan_003",
        "text": "Mee instant loan overdue aipoindi. 1 hour lo Rs 18,000 kattakapothe mee contacts lo unna andariki mee photos edit chesi WhatsApp lo pampisthamu. Police case kooda pedathamu: http://fast-cash-loan-repay.online",
        "category": "loan_app_extortion",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_loan_harass"
    },
    {
        "id": "gold_v2_loan_004",
        "text": "Legal Notice from SpeedyCredit: Recovery recovery agents have reached your residential address. Pay overdue loan Rs 12,500 immediately to avoid public humiliation in front of neighbors: http://speedycredit-legal.top",
        "category": "loan_app_extortion",
        "language": "en",
        "is_hard_negative": False,
        "style": "agent_home_threat"
    },
    {
        "id": "gold_v2_loan_005",
        "text": "Aapka 7-day loan default hua hai. Hamare paas aapki gallery aur call logs ka pura backup hai. Agar 20 min me settlement nahi hua toh office me HR ko call karke defame karenge.",
        "category": "loan_app_extortion",
        "language": "hi",
        "is_hard_negative": False,
        "style": "office_hr_call_threat"
    },
    {
        "id": "gold_v2_loan_006",
        "text": "URGENT: RupeeLoan fraud clearance! Your Aadhaar and PAN are being blacklisted with CIBIL and police warrant issued. Clear fine Rs 9,400 via UPI to close criminal case: loanclose@okhdfcbank",
        "category": "loan_app_extortion",
        "language": "en",
        "is_hard_negative": False,
        "style": "cibil_blacklist_threat"
    },
    {
        "id": "gold_v2_loan_007",
        "text": "Mee phone contacts lo unna mee relatives list motham download chesamu. Rs 14,000 repay cheyyakapothe andariki mee gurinchi cheppi insult chesthamu: http://quick-repay-loan.xyz",
        "category": "loan_app_extortion",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_contacts_threat"
    },
    {
        "id": "gold_v2_loan_008",
        "text": "KreditBee recovery department: You failed to pay EMI. Your CIBIL score is ruined and court summons dispatching. Pay minimum settlement Rs 6,800 on link now: http://kreditbee-settlement.online",
        "category": "loan_app_extortion",
        "language": "en",
        "is_hard_negative": False,
        "style": "court_summons_fake"
    },
    {
        "id": "gold_v2_loan_009",
        "text": "Tere baap ko phone lagaye ya chup chap 8000 UPI karega? Hamare recovery boys tere area me khade hain, address confirm hai. Phone mat kaatna.",
        "category": "loan_app_extortion",
        "language": "hi",
        "is_hard_negative": False,
        "style": "thug_call_threat"
    },
    {
        "id": "gold_v2_loan_010",
        "text": "Final pre-litigation settlement: PocketCash loan account defaulting. Pay Rs 4,999 to avoid attachment of salary and bank account freeze by recovery magistrate.",
        "category": "loan_app_extortion",
        "language": "en",
        "is_hard_negative": False,
        "style": "salary_attachment_scam"
    },

    # --- LOTTERY & PRIZE SCAMS (10 samples) ---
    {
        "id": "gold_v2_lottery_001",
        "text": "CONGRATULATIONS! Your mobile number won 1st Prize of Rs 25,00,000 (25 Lakhs) in KBC Kaun Banega Crorepati WhatsApp Lucky Draw! Contact KBC Manager Rana Pratap on WhatsApp +91-9876543210 to pay processing tax Rs 12,500 and claim your cheque.",
        "category": "lottery_prize",
        "language": "en",
        "is_hard_negative": False,
        "style": "kbc_whatsapp_lottery"
    },
    {
        "id": "gold_v2_lottery_002",
        "text": "बधाई हो! आपके जिओ नंबर पर 25 लाख की केबीसी लॉटरी लगी है। चेक आपके पते पर भेजने के लिए 18,500 रुपये जीएसटी शुल्क इस खाते में जमा करें: http://kbc-lucky-winner.xyz",
        "category": "lottery_prize",
        "language": "hi",
        "is_hard_negative": False,
        "style": "hindi_kbc_lottery"
    },
    {
        "id": "gold_v2_lottery_003",
        "text": "అభినందనలు! రిలయన్స్ జియో 10వ వార్షికోత్సవం లక్కీ డ్రా లో మీకు టాటా సఫారి కారు లేదా రూ. 15 లక్షల నగదు బహుమతి వచ్చింది. రిజిస్ట్రేషన్ ఫీజు రూ. 8,500 చెల్లించి బహుమతి పొందండి: http://jio-bumper-lottery.top",
        "category": "lottery_prize",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_jio_lottery"
    },
    {
        "id": "gold_v2_lottery_004",
        "text": "Amazon Mega Festive Bonanza: You have won a brand new iPhone 16 Pro Max! Pay shipping and courier insurance charge of Rs 999 only via UPI to confirm dispatch: http://amazon-festive-winner.online",
        "category": "lottery_prize",
        "language": "en",
        "is_hard_negative": False,
        "style": "iphone_gift_scam"
    },
    {
        "id": "gold_v2_lottery_005",
        "text": "Aapka mobile number Maruti Swift car lucky winner chuna gaya hai. Car deliver karne ke liye RTO road tax aur insurance charges 14,200 UPI karein: rto-lottery@ybl",
        "category": "lottery_prize",
        "language": "hi",
        "is_hard_negative": False,
        "style": "maruti_car_draw"
    },
    {
        "id": "gold_v2_lottery_006",
        "text": "State Bank of India 75th Year Celebration Draw: Selected account holders get cash reward of Rs 75,000 directly credited. Pay government stamp duty Rs 2,499 to release fund: http://sbi-anniversary-prize.top",
        "category": "lottery_prize",
        "language": "en",
        "is_hard_negative": False,
        "style": "bank_anniversary_prize"
    },
    {
        "id": "gold_v2_lottery_007",
        "text": "Mee number ku Dubai Gold Souk lottery lo 100 grams gold bar vachindi. Customs clearance charge Rs 11,500 kattandi gold mee intiki post chestharu: http://dubai-gold-lottery.xyz",
        "category": "lottery_prize",
        "language": "te",
        "is_hard_negative": False,
        "style": "dubai_gold_lottery"
    },
    {
        "id": "gold_v2_lottery_008",
        "text": "ICC T20 World Cup Fan Contest: You won Rs 5,00,000 cash! Claim code #WC2026. Deposit refundable verification deposit Rs 5,000 to authorize bank wire transfer.",
        "category": "lottery_prize",
        "language": "en",
        "is_hard_negative": False,
        "style": "sports_contest_prize"
    },
    {
        "id": "gold_v2_lottery_009",
        "text": "Kaun Banega Crorepati official customer lottery ticket #KB8492! Amitabh Bachchan handed cheque to your mobile number. WhatsApp 8920194012 for bank account details.",
        "category": "lottery_prize",
        "language": "en",
        "is_hard_negative": False,
        "style": "amitabh_cheque_scam"
    },
    {
        "id": "gold_v2_lottery_010",
        "text": "Aapko Flipkart Spin & Win me 10 Gram Sona mila hai. Ghar par delivery ke liye GST fee 799 rupaye turant pay karein link par: http://flipkart-spin-gold.online",
        "category": "lottery_prize",
        "language": "hi",
        "is_hard_negative": False,
        "style": "spin_and_win_gold"
    },

    # --- FAKE CUSTOMER SUPPORT (10 samples) ---
    {
        "id": "gold_v2_support_001",
        "text": "Google Pay 24x7 Customer Support Desk: Did your UPI transaction of Rs 8,500 fail or get stuck? Call our senior nodal officer on 08920194821 immediately for instant refund within 2 minutes.",
        "category": "fake_customer_support",
        "language": "en",
        "is_hard_negative": False,
        "style": "gpay_fake_helpline"
    },
    {
        "id": "gold_v2_support_002",
        "text": "PhonePe Sahayata Kendra: Agar aapka transaction fas gaya hai ya cashback nahi mila toh hamare toll free helpline number 09128374821 par sampark karein aur refund form bharein.",
        "category": "fake_customer_support",
        "language": "hi",
        "is_hard_negative": False,
        "style": "phonepe_hindi_support"
    },
    {
        "id": "gold_v2_support_003",
        "text": "పేటీఎం కస్టమర్ సపోర్ట్: మీ వాలెట్ లాక్ చేయబడింది లేదా పేమెంట్ ఆగిపోయిందా? సహాయం కోసం మా కస్టమర్ కేర్ ఎగ్జిక్యూటివ్ 8920194821 కు కాల్ చేయండి.",
        "category": "fake_customer_support",
        "language": "te",
        "is_hard_negative": False,
        "style": "paytm_telugu_support"
    },
    {
        "id": "gold_v2_support_004",
        "text": "SBI YONO Helpdesk: If your mobile banking login shows technical error 901, dial our instant resolution specialist at 9849201920 to reset password and unlock account.",
        "category": "fake_customer_support",
        "language": "en",
        "is_hard_negative": False,
        "style": "sbi_fake_helpdesk"
    },
    {
        "id": "gold_v2_support_005",
        "text": "Zomato / Swiggy refund department: Your refund of Rs 480 is pending due to bank server failure. Contact refund officer on WhatsApp 7820194820 to claim payment via UPI collect link.",
        "category": "fake_customer_support",
        "language": "en",
        "is_hard_negative": False,
        "style": "food_delivery_refund_help"
    },
    {
        "id": "gold_v2_support_006",
        "text": "Airtel DTH Customer Care: Recharge failed but money deducted? Call 09820194821 to register complaint and get instant refund into your Google Pay.",
        "category": "fake_customer_support",
        "language": "en",
        "is_hard_negative": False,
        "style": "dth_care_scam"
    },
    {
        "id": "gold_v2_support_007",
        "text": "IRCTC Tatkal Refund Support: Train cancellation refund of Rs 2,450 failed. Call nodal officer 8920194820 to generate reverse refund QR code.",
        "category": "fake_customer_support",
        "language": "en",
        "is_hard_negative": False,
        "style": "irctc_refund_support"
    },
    {
        "id": "gold_v2_support_008",
        "text": "Amazon Pay Customer Redressal: Account suspended for suspicious activity. Reach out to verified customer associate on 9012938472 to verify debit card details and unblock.",
        "category": "fake_customer_support",
        "language": "en",
        "is_hard_negative": False,
        "style": "amazon_pay_support"
    },
    {
        "id": "gold_v2_support_009",
        "text": "Electricity Bill Complaint Cell: Did you pay bill but receipt not generated? Call power department supervisor at 9820194821 for immediate receipt clearance.",
        "category": "fake_customer_support",
        "language": "en",
        "is_hard_negative": False,
        "style": "bijli_complaint_desk"
    },
    {
        "id": "gold_v2_support_010",
        "text": "HDFC Credit Card Fraud Department: Transaction blocked for security reasons. Call our senior risk manager at 8920194821 immediately to authenticate transaction.",
        "category": "fake_customer_support",
        "language": "en",
        "is_hard_negative": False,
        "style": "credit_card_fraud_desk"
    },

    # --- JOB & INVESTMENT / CRYPTO / TASK SCAMS (10 samples) ---
    {
        "id": "gold_v2_job_001",
        "text": "Earn Rs 3,000 - 8,000 daily from home! Part-time YouTube video liking and Google Maps rating job. Daily salary paid via UPI. No experience required. Join official Telegram HR manager: t.me/youtube_daily_earn_2026",
        "category": "job_investment_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "youtube_task_scam"
    },
    {
        "id": "gold_v2_job_002",
        "text": "Ghar baithe kamayein ₹50,000 mahina! Simple Amazon product review aur Telegram task job. Pehle task me ₹150 invest karo aur ₹300 wapas pao. WhatsApp par contact karein: +91-9820194821",
        "category": "job_investment_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "hindi_task_investment"
    },
    {
        "id": "gold_v2_job_003",
        "text": "వర్క్ ఫ్రమ్ హోమ్ పార్ట్ టైమ్ జాబ్! హోటల్ రివ్యూలు రాయడం ద్వారా రోజుకు రూ. 4000 సంపాదించండి. ఎలాంటి రిజిస్ట్రేషన్ ఫీజు లేదు. టెలిగ్రామ్ గ్రూప్ లో చేరండి: t.me/hotel_rating_jobs",
        "category": "job_investment_scam",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_job_scam"
    },
    {
        "id": "gold_v2_job_004",
        "text": "VIP Crypto Trading Signals by Binance VIP Trader: Invest Rs 10,000 and get guaranteed 250% return in 24 hours. Zero risk, 100% automated trading bot. Send funds to UPI id: cryptoking@ybl",
        "category": "job_investment_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "crypto_doubling"
    },
    {
        "id": "gold_v2_job_005",
        "text": "Flipkart Merchant Partner: Earn commissions by buying product inventory. Deposit Rs 25,000 to unlock Tier-3 tasks and withdraw Rs 45,000 immediately: http://flipkart-partner-task.xyz",
        "category": "job_investment_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "merchant_prepaid_task"
    },
    {
        "id": "gold_v2_job_006",
        "text": "Stock market tips by SEBI registered advisor! 100% sure-shot intraday call for tomorrow. Join premium VIP group by transferring membership fee of Rs 4,999 to stock-guru@paytm.",
        "category": "job_investment_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "fake_sebi_advisor"
    },
    {
        "id": "gold_v2_job_007",
        "text": "Data Entry Work From Home: Typing simple books. Salary Rs 28,000/month. Refundable security deposit of Rs 1,500 required for software activation. Pay at http://dataentry-jobs-india.top",
        "category": "job_investment_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "data_entry_deposit"
    },
    {
        "id": "gold_v2_job_008",
        "text": "Bhai maine ye Telegram channel join kiya tha, pehle 500 dale toh 800 mile, ab 20000 dale toh bol rahe hain aur 50000 dalo tabhi withdrawal milega. Ye scam hai kya?",
        "category": "job_investment_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "task_withdrawal_trap"
    },
    {
        "id": "gold_v2_job_009",
        "text": "Congratulations! Your resume has been shortlisted for HR Executive at Deloitte / Infosys. Pay interview processing and uniform security fee of Rs 3,250 to confirm schedule: http://deloitte-campus-drive.online",
        "category": "job_investment_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "mnc_recruitment_fee"
    },
    {
        "id": "gold_v2_job_010",
        "text": "AI Prompt Engineer trainee needed. No degree required. Training stipend Rs 45,000. Laptop security deposit Rs 6,000 refundable after 1st month. Apply now: http://ai-career-portal.xyz",
        "category": "job_investment_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "ai_job_deposit"
    },

    # --- COLLECT REQUEST / PIN FRAUD (10 samples) ---
    {
        "id": "gold_v2_collect_001",
        "text": "GPay Reward: You have received a collect request of Rs 4,500 for Diwali Cashback. Accept collect request and enter your UPI PIN to receive money directly into your account.",
        "category": "collect_request_fraud",
        "language": "en",
        "is_hard_negative": False,
        "style": "cashback_collect_pin"
    },
    {
        "id": "gold_v2_collect_002",
        "text": "Aapke PhonePe par 3000 rupaye ka refund request aaya hai. Turant accept karke apna UPI PIN dalein taaki paise aapke khate me transfer ho sakein.",
        "category": "collect_request_fraud",
        "language": "hi",
        "is_hard_negative": False,
        "style": "hindi_collect_pin"
    },
    {
        "id": "gold_v2_collect_003",
        "text": "Mee PhonePe lo Rs 5,000 బోనస్ వచ్చింది. Collect request approve chesi, mee 6 digit UPI PIN enter chesi dabbu account lo collect chesukondi.",
        "category": "collect_request_fraud",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_collect_pin"
    },
    {
        "id": "gold_v2_collect_004",
        "text": "Paytm Collect Request Alert: User Priya Sharma requested Rs 2,500 from you. Note: Approving this request and typing your PIN will credit money to you.",
        "category": "collect_request_fraud",
        "language": "en",
        "is_hard_negative": False,
        "style": "fake_note_collect"
    },
    {
        "id": "gold_v2_collect_005",
        "text": "Bhai maine galati se collect request bhej di, tu bus accept dabake PIN daal de, tere account me mere paise aa jayenge refund ke tor pe.",
        "category": "collect_request_fraud",
        "language": "hi",
        "is_hard_negative": False,
        "style": "accidental_collect_chat"
    },
    {
        "id": "gold_v2_collect_006",
        "text": "Government Subsidy Claim: Collect request of Rs 6,000 sent from PM Kisan Samman Nidhi. Authorize with your secret UPI PIN to receive direct benefit transfer.",
        "category": "collect_request_fraud",
        "language": "en",
        "is_hard_negative": False,
        "style": "pm_kisan_collect"
    },
    {
        "id": "gold_v2_collect_007",
        "text": "Flipkart Cancellation Refund: We have raised a collect request for Rs 1,890. Kindly click Pay on PhonePe and enter your secret MPIN to receive instant credit.",
        "category": "collect_request_fraud",
        "language": "en",
        "is_hard_negative": False,
        "style": "ecommerce_refund_collect"
    },
    {
        "id": "gold_v2_collect_008",
        "text": "Mee salary advance collect request approve cheyyandi. PhonePe lo PIN kodithe mee account lo Rs 20,000 credit paduthundi.",
        "category": "collect_request_fraud",
        "language": "te",
        "is_hard_negative": False,
        "style": "salary_advance_collect"
    },
    {
        "id": "gold_v2_collect_009",
        "text": "Ola Cabs: Excess ride fare refund of Rs 180 sent via UPI collect. Accept and authorize with UPI PIN on BHIM app to claim money.",
        "category": "collect_request_fraud",
        "language": "en",
        "is_hard_negative": False,
        "style": "cab_refund_collect"
    },
    {
        "id": "gold_v2_collect_010",
        "text": "Google Pay: Ramesh sent you a payment collect of Rs 8,000 for Old Furniture. Press Pay and enter UPI secret code to accept cash into your bank.",
        "category": "collect_request_fraud",
        "language": "en",
        "is_hard_negative": False,
        "style": "furniture_collect_scam"
    },

    # --- REMOTE ACCESS APP SCAMS (10 samples) ---
    {
        "id": "gold_v2_remote_001",
        "text": "Dear customer, your bank KYC verification requires remote biometric screening. Install AnyDesk or TeamViewer QuickSupport app from Play Store and share the 9-digit remote access code with our agent to prevent account block.",
        "category": "remote_access_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "anydesk_kyc_screening"
    },
    {
        "id": "gold_v2_remote_002",
        "text": "Aapka 5G SIM upgrade karne ke liye AnyDesk app download karein aur 9 digit number hamare officer ko batayein warna aapka SIM 2 ghante me band ho jayega.",
        "category": "remote_access_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "sim_upgrade_anydesk"
    },
    {
        "id": "gold_v2_remote_003",
        "text": "బ్యాంక్ కేవైసీ కోసం Play Store నుండి TeamViewer QuickSupport యాప్ ఇన్స్టాల్ చేయండి. స్క్రీన్ పైన వచ్చే 9 అంకెల కోడ్ మా బ్యాంక్ ఎగ్జిక్యూటివ్ కి చెప్పండి.",
        "category": "remote_access_scam",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_quicksupport"
    },
    {
        "id": "gold_v2_remote_004",
        "text": "Electricity Board technical verification: To clear your pending bill error, install RustDesk or AnyDesk software on your phone so our technical engineer can inspect your payment gateway.",
        "category": "remote_access_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "rustdesk_utility_scam"
    },
    {
        "id": "gold_v2_remote_005",
        "text": "PhonePe customer support: Sir refund process karne ke liye hamare live screen share tool AnyDesk ko install kijiye aur code allow kijiye, hum screen par dekh ke guide karenge.",
        "category": "remote_access_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "screenshare_refund_trap"
    },
    {
        "id": "gold_v2_remote_006",
        "text": "Urgent: Your HDFC Netbanking is temporarily restricted due to unauthorized login. Download AirDroid or TeamViewer to allow security audit by banking cyber team.",
        "category": "remote_access_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "netbanking_airdroid"
    },
    {
        "id": "gold_v2_remote_007",
        "text": "PF withdrawal settlement error: Install QuickSupport remote assistance app so EPFO helpdesk officer can verify your Aadhaar OTP and approve your claim.",
        "category": "remote_access_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "epfo_remote_support"
    },
    {
        "id": "gold_v2_remote_008",
        "text": "Meeru AnyDesk app open chesi permission allow chesthe memu mee mobile lo refund form fill chesi mee account lo Rs 12000 transfer chesthamu.",
        "category": "remote_access_scam",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_anydesk_form"
    },
    {
        "id": "gold_v2_remote_009",
        "text": "Google Pay Security Patch update: Download UltraViewer from Play Store. Grant accessibility permission so our team can protect your device against malware attacks.",
        "category": "remote_access_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "ultraviewer_patch"
    },
    {
        "id": "gold_v2_remote_010",
        "text": "Sir aap mobile screen share kijiye aur apna SBI Yono app open kijiye, hum check karenge kyu transaction fail ho raha hai. Code batayein.",
        "category": "remote_access_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "screen_share_yono"
    },

    # --- ACCIDENTAL TRANSFER / "WRONG NUMBER SENT MONEY" SCAMS (8 samples) ---
    {
        "id": "gold_v2_acc_001",
        "text": "Hello bhaiya, maine galti se aapke phone number pe Google Pay se Rs 25,000 bhej diye hain hospital emergency ke liye the. Please check karke turant is dusre number pe refund kar dijiye: +91-9820194821",
        "category": "accidental_transfer_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "hospital_accidental_refund"
    },
    {
        "id": "gold_v2_acc_002",
        "text": "Sir by mistake I transferred Rs 18,000 to your UPI ID instead of my brother's account. I am a poor student, please refund my money back immediately to this VPA: student-help@okhdfcbank",
        "category": "accidental_transfer_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "student_transfer_trap"
    },
    {
        "id": "gold_v2_acc_003",
        "text": "అన్నయ్య, పొరపాటున మీ ఫోన్ నెంబర్ కి రూ. 30,000 ఫోన్ పే ద్వారా పంపించాను. మా అమ్మ ఆసుపత్రి బిల్లు కోసం ఉంచిన డబ్బులు. దయచేసి వెంటనే నా గూగుల్ పే నెంబర్ 9849201920 కి తిరిగి పంపించండి.",
        "category": "accidental_transfer_scam",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_mother_hospital"
    },
    {
        "id": "gold_v2_acc_004",
        "text": "Bhaiya aapke a/c me fake SMS bheja gaya hai ki 15000 credit hua. Par sach me maine send kiya hai, aap return kijiye warna police me cyber cell FIR karunga.",
        "category": "accidental_transfer_scam",
        "language": "hi",
        "is_hard_negative": False,
        "style": "fir_threat_accidental"
    },
    {
        "id": "gold_v2_acc_005",
        "text": "Urgent: Mistakenly sent Rs 45,000 to your account for rent payment. Kindly re-transfer immediately. You can verify the spoofed credit notification on your SMS.",
        "category": "accidental_transfer_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "rent_mistake_transfer"
    },
    {
        "id": "gold_v2_acc_006",
        "text": "Sir, my small daughter pressed transfer button on PhonePe and sent Rs 12,000 to your mobile number. Please have humanity and return it to my UPI id.",
        "category": "accidental_transfer_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "daughter_transfer_plea"
    },
    {
        "id": "gold_v2_acc_007",
        "text": "Sir nenu shop payment chesthu mee number type chesa, Rs 8500 mee account ki vellipoyindi. Please help chesi na VPA ku pampandi.",
        "category": "accidental_transfer_scam",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_shop_payment_error"
    },
    {
        "id": "gold_v2_acc_008",
        "text": "I mistakenly sent Rs 50,000 from company corporate card to your UPI. Return immediately or legal audit committee will freeze your PAN card and savings account.",
        "category": "accidental_transfer_scam",
        "language": "en",
        "is_hard_negative": False,
        "style": "corporate_transfer_threat"
    },

    # --- FAKE BANK KYC / BLOCKED ACCOUNT (10 samples) ---
    {
        "id": "gold_v2_kyc_001",
        "text": "Dear SBI customer, your YONO NetBanking account will be PERMANENTLY BLOCKED tonight at 11:59 PM due to pending Aadhaar PAN link. Update immediately here: http://sbi-pan-kyc-update.xyz/login",
        "category": "fake_bank_kyc",
        "language": "en",
        "is_hard_negative": False,
        "style": "sbi_kyc_block_link"
    },
    {
        "id": "gold_v2_kyc_002",
        "text": "प्रिय पीएनबी ग्राहक, आपका खाता आज रात 10 बजे निष्क्रिय (Deactivated) कर दिया जाएगा क्योंकि आपकी ई-केवाईसी अधूरी है। तुरंत पेन कार्ड लिंक करें: http://pnb-ekyc-portal.online",
        "category": "fake_bank_kyc",
        "language": "hi",
        "is_hard_negative": False,
        "style": "hindi_pnb_kyc"
    },
    {
        "id": "gold_v2_kyc_003",
        "text": "హెచ్‌డిఎఫ్‌సి బ్యాంక్: మీ డెబిట్ కార్డ్ మరియు నెట్‌బ్యాంకింగ్ కేవైసీ అప్‌డేట్ కాకపోవడం వల్ల బ్లాక్ చేయబడింది. వెంటనే పునరుద్ధరించడానికి లింక్ క్లిక్ చేయండి: http://hdfc-card-reverify.top",
        "category": "fake_bank_kyc",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_hdfc_kyc"
    },
    {
        "id": "gold_v2_kyc_004",
        "text": "ICICI iMobile Security Warning: Your mobile banking access is suspended for unverified PAN documentation. Avoid permanent de-activation by updating within 24 hours: http://icici-pan-link.xyz",
        "category": "fake_bank_kyc",
        "language": "en",
        "is_hard_negative": False,
        "style": "icici_imobile_pan"
    },
    {
        "id": "gold_v2_kyc_005",
        "text": "Bank of Baroda: Your a/c ending 4012 will be closed and funds confiscated to RBI reserve if physical KYC verification is not confirmed online at http://bob-kyc-verify.online",
        "category": "fake_bank_kyc",
        "language": "en",
        "is_hard_negative": False,
        "style": "bob_fund_confiscation"
    },
    {
        "id": "gold_v2_kyc_006",
        "text": "Aapka Kotak 811 account freeze ho gaya hai. Dobara chalu karne ke liye yaha apna ATM card number aur PIN enter karein: http://kotak811-unfreeze.top",
        "category": "fake_bank_kyc",
        "language": "hi",
        "is_hard_negative": False,
        "style": "kotak_unfreeze_pin"
    },
    {
        "id": "gold_v2_kyc_007",
        "text": "Axis Bank Alert: Your UPI transaction facility has been disabled due to non-submission of Form 60. Enable immediately by visiting: http://axis-form60-verify.xyz",
        "category": "fake_bank_kyc",
        "language": "en",
        "is_hard_negative": False,
        "style": "axis_form60_scam"
    },
    {
        "id": "gold_v2_kyc_008",
        "text": "Mee Canara Bank account lo KYC expire aindi. Eeroju rathri lopala update cheyyakapothe ATM card pani cheyadhu: http://canara-kyc-renewal.online",
        "category": "fake_bank_kyc",
        "language": "te",
        "is_hard_negative": False,
        "style": "canara_telugu_kyc"
    },
    {
        "id": "gold_v2_kyc_009",
        "text": "URGENT: RBI mandates all savings accounts to complete Biometric KYC verification by today. Click here to prevent account closure: http://rbi-central-kyc.top",
        "category": "fake_bank_kyc",
        "language": "en",
        "is_hard_negative": False,
        "style": "fake_rbi_central_kyc"
    },
    {
        "id": "gold_v2_kyc_010",
        "text": "Union Bank Customer: Your Internet banking profile has been locked due to 3 wrong password attempts. Unlock profile instantly at: http://unionbank-profile-unlock.xyz",
        "category": "fake_bank_kyc",
        "language": "en",
        "is_hard_negative": False,
        "style": "unionbank_profile_lock"
    },

    # --- ELECTRICITY DISCONNECTION SCAMS (10 samples) ---
    {
        "id": "gold_v2_elec_001",
        "text": "Dear Consumer, your electricity power will be DISCONNECTED tonight at 9:30 PM from the sub-station because your previous month bill was not updated. Immediately contact power officer Mr. Verma at 9820194821 or pay here: http://bijli-bill-disconnect.xyz",
        "category": "electricity_disconnection",
        "language": "en",
        "is_hard_negative": False,
        "style": "bijli_officer_call"
    },
    {
        "id": "gold_v2_elec_002",
        "text": "बिजली विभाग सूचना: आज रात 9:30 बजे आपके घर की बिजली काट दी जाएगी क्योंकि पिछला बिल अपडेट नहीं हुआ है। तुरंत बिजली अधिकारी 8920194820 पर कॉल करें और बिल का भुगतान करें।",
        "category": "electricity_disconnection",
        "language": "hi",
        "is_hard_negative": False,
        "style": "hindi_bijli_disconnection"
    },
    {
        "id": "gold_v2_elec_003",
        "text": "ప్రియమైన వినియోగదారుడా, మీ విద్యుత్ బిల్లు అప్‌డేట్ కానందున ఈ రాత్రి 9:30 గంటలకు పవర్ కట్ చేయబడుతుంది. లైన్ మెన్ ఆఫీసర్ 9849201920 కి కాల్ చేసి వెంటనే బిల్లు చెల్లించండి: http://apspdcl-power-bill.top",
        "category": "electricity_disconnection",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_power_disconnect"
    },
    {
        "id": "gold_v2_elec_004",
        "text": "BSES Rajdhani Alert: Connection CA 10293849 scheduled for physical meter disconnection at 8:00 PM. Avoid penalty fee of Rs 2,500 by clearing pending dues instantly: http://bses-bill-clearance.online",
        "category": "electricity_disconnection",
        "language": "en",
        "is_hard_negative": False,
        "style": "bses_penalty_scam"
    },
    {
        "id": "gold_v2_elec_005",
        "text": "MahaVitaran (MSEDCL): Notice of electricity supply termination for consumer #02910394. To stop power outage at your premises, contact electric superintendent immediately on WhatsApp 7820194820.",
        "category": "electricity_disconnection",
        "language": "en",
        "is_hard_negative": False,
        "style": "msedcl_whatsapp_threat"
    },
    {
        "id": "gold_v2_elec_006",
        "text": "UPPCL Bijli alert: Consumer 10293849, bijli supply cut off order approved by Junior Engineer. Pay 100 rupees update fee on link immediately: http://uppcl-bill-update.xyz",
        "category": "electricity_disconnection",
        "language": "hi",
        "is_hard_negative": False,
        "style": "uppcl_update_fee"
    },
    {
        "id": "gold_v2_elec_007",
        "text": "TSSPDCL Warning: Line disconnection crew dispatched to your colony. Settle pending power charges immediately or face meter removal: http://tsspdcl-quick-pay.online",
        "category": "electricity_disconnection",
        "language": "en",
        "is_hard_negative": False,
        "style": "tsspdcl_meter_removal"
    },
    {
        "id": "gold_v2_elec_008",
        "text": "WBSEDCL West Bengal: Meter disconnected due to unpaid charges. Transfer payment to state electricity officer UPI VPA wbsedcl-officer@ybl to restore electricity tonight.",
        "category": "electricity_disconnection",
        "language": "en",
        "is_hard_negative": False,
        "style": "wbsedcl_officer_vpa"
    },
    {
        "id": "gold_v2_elec_009",
        "text": "Mee current meter bill update kaledu. 10 minutes lo current cut chestharu. Office officer number 9012938472 ku call cheyandi.",
        "category": "electricity_disconnection",
        "language": "te",
        "is_hard_negative": False,
        "style": "roman_telugu_current_cut"
    },
    {
        "id": "gold_v2_elec_010",
        "text": "Torrent Power: Electricity disconnection order issued for tonight. Clear outstanding balance of Rs 1,890 instantly to prevent disconnection at midnight: http://torrentpower-bill-pay.xyz",
        "category": "electricity_disconnection",
        "language": "en",
        "is_hard_negative": False,
        "style": "torrent_power_midnight"
    },

    # --- OTP / PIN THEFT (10 samples) ---
    {
        "id": "gold_v2_otp_001",
        "text": "Dear customer, your credit card loyalty reward points of Rs 9,850 are expiring today! To redeem into your bank account, share the 6-digit verification OTP received on your mobile with our reward executive.",
        "category": "otp_pin_theft",
        "language": "en",
        "is_hard_negative": False,
        "style": "reward_points_otp"
    },
    {
        "id": "gold_v2_otp_002",
        "text": "Bank Manager bol raha hu: Aapka ATM card band ho raha hai, abhi aapke phone par 6 digit ka OTP aayega wo turant batayein taaki card re-activate kar sakein.",
        "category": "otp_pin_theft",
        "language": "hi",
        "is_hard_negative": False,
        "style": "bank_manager_atm_otp"
    },
    {
        "id": "gold_v2_otp_003",
        "text": "మీ ఫోన్ కి వచ్చిన 6 అంకెల OTP కోడ్ మా బ్యాంక్ సర్వర్‌కి చెబితే మీ ఖాతా బ్లాక్ అవ్వకుండా ఉంటుంది. వెంటనే ఓటీపీ చెప్పండి.",
        "category": "otp_pin_theft",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_otp_demand"
    },
    {
        "id": "gold_v2_otp_004",
        "text": "SBI Alert: A transaction of Rs 48,000 is requested on your card. To CANCEL this fraud transaction, provide the one-time password (OTP) sent to your registered mobile number: http://sbi-cancel-fraud.xyz",
        "category": "otp_pin_theft",
        "language": "en",
        "is_hard_negative": False,
        "style": "cancel_fraud_otp_trap"
    },
    {
        "id": "gold_v2_otp_005",
        "text": "Enter your 4-digit or 6-digit ATM PIN and CVV number to claim free annual subscription bonus of Rs 5,000 on your RuPay debit card: http://rupay-annual-bonus.online",
        "category": "otp_pin_theft",
        "language": "en",
        "is_hard_negative": False,
        "style": "cvv_pin_bonus"
    },
    {
        "id": "gold_v2_otp_006",
        "text": "Sir aapke a/c me 25000 cashback credit karne ke liye bank ko aapka secret UPI PIN confirm karna padega. Yaha enter karein: http://upi-pin-confirm.xyz",
        "category": "otp_pin_theft",
        "language": "hi",
        "is_hard_negative": False,
        "style": "cashback_pin_confirm"
    },
    {
        "id": "gold_v2_otp_007",
        "text": "WhatsApp Security Update: Do not close this session. Enter your 6-digit WhatsApp registration SMS code to protect your account from hacking.",
        "category": "otp_pin_theft",
        "language": "en",
        "is_hard_negative": False,
        "style": "whatsapp_code_theft"
    },
    {
        "id": "gold_v2_otp_008",
        "text": "Aadhaar authentication service: Provide the Aadhaar UIDAI OTP to link with your telecom SIM card to avoid mobile number disconnection within 4 hours.",
        "category": "otp_pin_theft",
        "language": "en",
        "is_hard_negative": False,
        "style": "aadhaar_otp_telecom"
    },
    {
        "id": "gold_v2_otp_009",
        "text": "Meeru lottery amount claim cheyyali ante mee debit card meeda unna 16 digit number, expiry date mariyu 3 digit CVV enter cheyyandi.",
        "category": "otp_pin_theft",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_cvv_theft"
    },
    {
        "id": "gold_v2_otp_010",
        "text": "Telecom tower installation bonus: Send OTP received on your phone to complete agreement verification and receive advance lease payment of Rs 1,50,000.",
        "category": "otp_pin_theft",
        "language": "en",
        "is_hard_negative": False,
        "style": "tower_lease_otp"
    },

    # --- FAKE UPI REFUND / CASHBACK (8 samples) ---
    {
        "id": "gold_v2_refund_001",
        "text": "You have received an unclaimed scratch card reward of Rs 1,489 on PhonePe! Scratch now and claim directly to your bank account: http://phonepe-scratch-win.xyz",
        "category": "fake_upi_refund_cashback",
        "language": "en",
        "is_hard_negative": False,
        "style": "scratch_card_refund"
    },
    {
        "id": "gold_v2_refund_002",
        "text": "Google Pay: Aapko Diwali cashback reward mila hai ₹2,999 ka. Abhi link par click karke apne bank khate me transfer karein: http://gpay-festive-cashback.online",
        "category": "fake_upi_refund_cashback",
        "language": "hi",
        "is_hard_negative": False,
        "style": "gpay_hindi_cashback"
    },
    {
        "id": "gold_v2_refund_003",
        "text": "పేటీఎం క్యాష్‌బ్యాక్ ఆఫర్: మీకు రూ. 3,500 లక్కీ క్యాష్‌బ్యాక్ వచ్చింది. మీ బ్యాంక్ అకౌంట్ కి బదిలీ చేసుకోవడానికి ఇప్పుడే క్లిక్ చేయండి: http://paytm-reward-claim.top",
        "category": "fake_upi_refund_cashback",
        "language": "te",
        "is_hard_negative": False,
        "style": "paytm_telugu_cashback"
    },
    {
        "id": "gold_v2_refund_004",
        "text": "IRCTC Ticket Cancellation Refund of Rs 3,820 is ready for settlement. Click link to choose refund payment mode and verify your UPI ID: http://irctc-refund-settlement.xyz",
        "category": "fake_upi_refund_cashback",
        "language": "en",
        "is_hard_negative": False,
        "style": "irctc_ticket_refund"
    },
    {
        "id": "gold_v2_refund_005",
        "text": "PhonePe Merchant Cashback: Rs 5,500 credited to your merchant balance. Click to redeem to primary savings account: http://phonepe-merchant-settle.top",
        "category": "fake_upi_refund_cashback",
        "language": "en",
        "is_hard_negative": False,
        "style": "merchant_cashback_fake"
    },
    {
        "id": "gold_v2_refund_006",
        "text": "Amazon Pay Cashback: Congratulations! You unlocked Rs 850 cash reward on your last recharge. Claim before midnight: http://amazon-cashback-claim.online",
        "category": "fake_upi_refund_cashback",
        "language": "en",
        "is_hard_negative": False,
        "style": "amazon_cashback_scam"
    },
    {
        "id": "gold_v2_refund_007",
        "text": "Mee Google Pay account lo Rs 4,200 pending refund unnadhi. Redeem chesukodaniki ventane link open cheyandi: http://gpay-refund-center.xyz",
        "category": "fake_upi_refund_cashback",
        "language": "te",
        "is_hard_negative": False,
        "style": "gpay_telugu_refund"
    },
    {
        "id": "gold_v2_refund_008",
        "text": "Cred UPI Cashback: You won Rs 1,250 jackpot cashback on your credit card bill payment. Click here to transfer to bank: http://cred-jackpot-reward.top",
        "category": "fake_upi_refund_cashback",
        "language": "en",
        "is_hard_negative": False,
        "style": "cred_jackpot_cashback"
    },

    # --- FAKE GOVERNMENT SCHEMES (7 samples) ---
    {
        "id": "gold_v2_govt_001",
        "text": "Pradhan Mantri Berojgari Bhatta Yojana 2026: All unemployed youth will get Rs 4,500 every month directly in bank account. Registration is free for today only. Apply here: http://pm-berojgari-yojana.xyz",
        "category": "fake_govt_scheme",
        "language": "en",
        "is_hard_negative": False,
        "style": "pm_unemployment_allowance"
    },
    {
        "id": "gold_v2_govt_002",
        "text": "प्रधानमंत्री कन्या धन योजना 2026: सभी बेटियों को पढ़ाई के लिए ₹50,000 की आर्थिक सहायता सीधे बैंक खाते में दी जा रही है। अपना फॉर्म आज ही भरें: http://pm-kanya-dhan.online",
        "category": "fake_govt_scheme",
        "language": "hi",
        "is_hard_negative": False,
        "style": "hindi_kanya_dhan"
    },
    {
        "id": "gold_v2_govt_003",
        "text": "పీఎం ఆవాస్ యోజన: ఉచిత పక్కా ఇల్లు మరియు రూ. 2,50,000 సబ్సిడీ కోసం మీ ఆధార్ నెంబర్ తో నమోదు చేసుకోండి. నమోదు రుసుము రూ. 499 మాత్రమే: http://pm-awas-subsidy.top",
        "category": "fake_govt_scheme",
        "language": "te",
        "is_hard_negative": False,
        "style": "telugu_pm_awas"
    },
    {
        "id": "gold_v2_govt_004",
        "text": "PM Free Solar Panel Scheme 2026: Government is giving 100% free rooftop solar subsidy. Pay application documentation fee of Rs 999 to receive installation in 7 days: http://pm-solar-subsidy.xyz",
        "category": "fake_govt_scheme",
        "language": "en",
        "is_hard_negative": False,
        "style": "solar_panel_fee"
    },
    {
        "id": "gold_v2_govt_005",
        "text": "Mukhyamantri Ladli Behna Yojana: Rs 3,000 monthly allowance transfer failed due to inactive DBT bank link. Update your bank details immediately at: http://ladli-behna-dbt.online",
        "category": "fake_govt_scheme",
        "language": "en",
        "is_hard_negative": False,
        "style": "ladli_behna_scam"
    },
    {
        "id": "gold_v2_govt_006",
        "text": "Ministry of Finance Relief Package: Claim COVID / Economic revival stimulus grant of Rs 10,000 directly to your Jan Dhan account. Enter details at: http://mof-relief-grant.top",
        "category": "fake_govt_scheme",
        "language": "en",
        "is_hard_negative": False,
        "style": "stimulus_grant_scam"
    },
    {
        "id": "gold_v2_govt_007",
        "text": "Rythu Bandhu Financial Assistance: Farmer support installment of Rs 7,500 waiting for bank approval. Pay verification stamp charge Rs 250 here: http://rythu-bandhu-claim.xyz",
        "category": "fake_govt_scheme",
        "language": "te",
        "is_hard_negative": False,
        "style": "rythu_bandhu_scam"
    }
]

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    v2_path = os.path.join(data_dir, "gold_v2.json")
    with open(v2_path, "w", encoding="utf-8") as f:
        json.dump(GOLD_V2_SAMPLES, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated gold_v2 benchmark dataset at {v2_path}")
    print(f"Total samples in gold_v2: {len(GOLD_V2_SAMPLES)}")

if __name__ == "__main__":
    main()
