import os
import random
import pandas as pd

def generate_callback_scam_samples():
    random.seed(42)
    samples = []

    amounts = ["49,999", "50,000", "25,000", "99,999", "1,00,000", "75,000", "30,000", "20,000", "40,000", "80,000", "15,000", "10,000", "35,500", "65,000", "48,500", "85,000"]
    mobiles = [
        "+91-9876543210", "+91 9876543210", "9876543210", "09876543210",
        "+91-8765432109", "8765432109", "+91 7654321098", "7654321098",
        "+91-6543210987", "6543210987", "+91-9123456780", "9123456780",
        "+91-8123456789", "8123456789", "+91 9988776655", "9988776655"
    ]
    placeholders = [
        "+91-XXXXXXXXXX", "XXXXXXXXXX", "+91 XXXXXXXXXX", "98765XXXXX",
        "+91-98765XXXXX", "98765*****", "XXXXX XXXXX", "98765 XXXXX"
    ]
    spaced_numbers = [
        "9 8 7 6 5 4 3 2 1 0", "+91 9 8 7 6 5 4 3 2 1 0", "8 7 6 5 4 3 2 1 0 9",
        "7 6 5 4 3 2 1 0 9 8", "9 1 2 3 4 5 6 7 8 0"
    ]
    word_numbers = [
        "nine eight seven six five four three two one zero",
        "eight seven six five four three two one zero nine",
        "nine one two three four five six seven eight zero"
    ]
    all_numbers = mobiles + placeholders + spaced_numbers + word_numbers

    # --- ENGLISH SCAMS (105 samples) ---
    en_templates = [
        "Alert: ₹{amt} debited from your account. If not done by you, call {num} immediately to reverse.",
        "URGENT: Rs {amt} has been deducted from your bank account. To dispute this transaction or cancel, contact customer care at {num} now.",
        "Notice: Transaction of INR {amt} processed on your account. If unauthorized, dial {num} within 24 hours.",
        "Bank Alert: Payment of Rs {amt} charged. If not you? Call fraud desk at {num} immediately.",
        "Your account debited by ₹{amt}. Dispute this transaction immediately by calling {num}.",
        "Transaction Alert: ₹{amt} debited from your bank account. Not you? Contact security helpline {num} immediately.",
        "Dear Customer, ₹{amt} was withdrawn from your account. To stop this transaction, reach us at {num} immediately.",
        "Alert: Rs {amt} debited. If not done by you, msg/call on this number {num} immediately.",
        "Hello, I am from bank fraud team. ₹{amt} debited from your account. If not done by you, call this number {num} immediately.",
        "URGENT DISPUTE ALERT: ₹{amt} deducted from your account. Call officer on {num} to claim refund and freeze transfer.",
        "Important notification: An amount of Rs {amt} is debited from your account. If not initiated by you, dial {num} at once.",
        "Alert: Debit of Rs {amt} successful. If not you, call {num} immediately to block card and reverse funds.",
        "Security warning: Your account has been charged ₹{amt}. To reverse unauthorized debit, contact customer care {num}.",
        "Bank Notification: Rs {amt} debited. Call {num} immediately if this was not done by you.",
        "Txn alert: Rs {amt} debited from your account. If not you call {num} now to cancel."
    ]

    for t_idx, tpl in enumerate(en_templates):
        for i in range(7):
            amt = random.choice(amounts)
            num = random.choice(all_numbers)
            text = tpl.format(amt=amt, num=num)
            # Add minor typo or SMS shorthand occasionally
            if i % 3 == 0:
                text = text.replace("account", "a/c").replace("Transaction", "Txn").replace("immediately", "urgently")
            samples.append({
                "template_id": f"cb_scam_en_{t_idx + 1}",
                "category": "fake_debit_alert_callback",
                "language": "en",
                "text": text,
                "label": "scam"
            })

    # --- HINDI SCAMS (85 samples) ---
    hi_numbers = [
        "+91-9876543210", "9876543210", "09876543210", "+91-XXXXXXXXXX",
        "XXXXXXXXXX", "98765XXXXX", "9 8 7 6 5 4 3 2 1 0",
        "नौ आठ सात छह पांच चार तीन दो एक शून्य"
    ]
    hi_templates = [
        "अलर्ट: आपके बैंक खाते से ₹{amt} डेबिट हो गए हैं। यदि आपने यह ट्रांजेक्शन नहीं किया, तो तुरंत {num} पर कॉल करें।",
        "सूचना: आपके खाते से ₹{amt} की राशि निकाल ली गई है। इस ट्रांजेक्शन को रद्द करने के लिए तुरंत {num} पर संपर्क करें।",
        "बैंक अलर्ट: आपके खाते से ₹{amt} काटे गए हैं। यदि आपने नहीं किया तो तुरंत कस्टमर केयर नंबर {num} पर कॉल करें।",
        "चेतावनी: खाते से ₹{amt} का लेनदेन हुआ है। अनधिकृत लेनदेन रोकने हेतु तुरंत इस नंबर {num} पर कॉल करें।",
        "ज़रूरी सूचना: आपके बैंक अकाउंट से ₹{amt} निकल गए हैं। इस ट्रांजेक्शन को रोकने के लिए अभी कॉल करें: {num}",
        "अलर्ट: ₹{amt} खाते से डेबिट। अगर आपने नहीं किया तो तुरंत {num} पर कॉल या मैसेज करें।",
        "नमस्ते, मैं बैंक फ्रॉड प्रिवेंशन टीम से हूँ। आपके खाते से ₹{amt} डेबिट हुए हैं। यदि आपने नहीं किया, तो तुरंत {num} पर डायल करें।",
        "बैंक सुरक्षा चेतावनी: आपके खाते से ₹{amt} कटे हैं। पैसे वापस पाने के लिए तुरंत अधिकारी से {num} पर संपर्क करें।",
        "अलर्ट: ₹{amt} आपके बैंक खाते से ट्रांसफर हुए। अगर यह आपने नहीं किया तो तुरंत {num} पर शिकायत दर्ज करें।",
        "अति आवश्यक: ₹{amt} कट गए हैं। ट्रांजेक्शन रद्द करवाने हेतु तुरंत {num} पर फोन करें।"
    ]

    for t_idx, tpl in enumerate(hi_templates):
        for i in range(8 if t_idx < 5 else 9):
            amt = random.choice(amounts)
            num = random.choice(hi_numbers)
            text = tpl.format(amt=amt, num=num)
            samples.append({
                "template_id": f"cb_scam_hi_{t_idx + 1}",
                "category": "fake_debit_alert_callback",
                "language": "hi",
                "text": text,
                "label": "scam"
            })

    # --- TELUGU SCAMS (85 samples) ---
    te_numbers = [
        "+91-9876543210", "9876543210", "+91-XXXXXXXXXX", "XXXXXXXXXX",
        "98765XXXXX", "9 8 7 6 5 4 3 2 1 0",
        "తొమ్మిది ఎనిమిది ఏడు ఆరు ఐదు నాలుగు మూడు రెండు ఒకటి సున్నా"
    ]
    te_templates = [
        "హెచ్చరిక: మీ బ్యాంక్ ఖాతా నుండి ₹{amt} డెబిట్ చేయబడింది. ఈ లావాదేవీ మీరు చేయకపోతే, వెంటనే {num} నంబర్‌కు కాల్ చేయండి.",
        "ముఖ్య గమనిక: మీ ఖాతా నుండి ₹{amt} నగదు విత్‌డ్రా చేయబడింది. లావాదేవీని రద్దు చేయడానికి వెంటనే {num} ను సంప్రదించండి.",
        "బ్యాంక్ అలర్ట్: మీ అకౌంట్ నుండి ₹{amt} కట్ అయ్యాయి. మీరు చేయకపోతే వెంటనే కస్టమర్ కేర్ {num} కు కాల్ చేయండి.",
        "అత్యవసరం: మీ ఖాతా నుండి ₹{amt} డెబిట్ అయింది. ఈ లావాదేవీని ఆపడానికి వెంటనే {num} కు డయల్ చేయండి.",
        "భద్రతా హెచ్చరిక: ₹{amt} మీ అకౌంట్ నుండి బదిలీ చేయబడింది. రీఫండ్ పొందడానికి వెంటనే ఈ నంబర్ {num} కు కాల్ చేయండి.",
        "అలర్ట్: ఖాతా నుండి ₹{amt} డెబిట్. మీరు చేయకపోతే వెంటనే {num} కు వాట్సాప్ లేదా కాల్ చేయండి.",
        "నమస్కారం, నేను బ్యాంక్ ఫ్రాడ్ విభాగం నుండి మాట్లాడుతున్నాను. మీ ఖాతా నుండి ₹{amt} కట్ అయ్యాయి. ఆపడానికి వెంటనే {num} కు కాల్ చేయండి.",
        "ముఖ్యమైన సమాచారం: ₹{amt} మీ ఖాతా నుండి తీసివేయబడింది. వెంటనే నిలిపివేయడానికి {num} సంప్రదించండి.",
        "బ్యాంక్ నోటీస్: మీ ఖాతా నుండి ₹{amt} డెబిట్ జరిగింది. మీరు కాకపోతే వెంటనే {num} కు ఫోన్ చేయండి.",
        "హెచ్చరిక: ₹{amt} లావాదేవీ జరిగింది. రద్దు చేయడానికి వెంటనే {num} నంబర్‌కు కాల్ చేయండి."
    ]

    for t_idx, tpl in enumerate(te_templates):
        for i in range(8 if t_idx < 5 else 9):
            amt = random.choice(amounts)
            num = random.choice(te_numbers)
            text = tpl.format(amt=amt, num=num)
            samples.append({
                "template_id": f"cb_scam_te_{t_idx + 1}",
                "category": "fake_debit_alert_callback",
                "language": "te",
                "text": text,
                "label": "scam"
            })

    # --- HINGLISH & CODE-MIXED SCAMS (60 samples) ---
    hinglish_templates = [
        "Alert: Aapke account se Rs {amt} debit ho gaya hai. Agar aapne nahi kiya toh turant {num} par call kare.",
        "URGENT: Khate se Rs {amt} cut gaye hai. Cancel karne ke liye abhi customer care number {num} par contact kare.",
        "Bank Alert: Rs {amt} debited from your bank account. Agar ye aapne nahi kiya toh turant {num} pe call karo.",
        "Notice: Account se Rs {amt} nikal gaye hai. Transaction reverse karne ke liye call kare {num} turant.",
        "Alert: Rs {amt} debit ho chuka hai. If not you, msg or call on this number {num} immediately.",
        "Hello sir, I am from bank fraud team. Aapke account se Rs {amt} debit hua hai. Rokne ke liye call {num} immediately.",
        "Aapka account se Rs {amt} deducted. Agar aapne transaction nahi kiya toh turant call kare: {num}",
        "Mee account nundi Rs {amt} debit aindi. Meeru cheyakapothe ventane call cheyandi {num} ki.",
        "Warning: Bank account se Rs {amt} kat gaye. Dispute transaction ke liye call kare {num} turant.",
        "Alert: Rs {amt} has been debited. Agar aap nahi ho toh turant {num} par phone karke stop kare."
    ]

    for t_idx, tpl in enumerate(hinglish_templates):
        for i in range(6):
            amt = random.choice(amounts)
            num = random.choice(all_numbers)
            text = tpl.format(amt=amt, num=num)
            samples.append({
                "template_id": f"cb_scam_hinglish_{t_idx + 1}",
                "category": "fake_debit_alert_callback",
                "language": "en" if "account" in text else "hi",
                "text": text,
                "label": "scam"
            })

    print(f"Generated {len(samples)} diverse fictional callback scam samples.")
    return samples

def generate_genuine_hard_negatives():
    random.seed(43)
    samples = []

    banks = ["HDFC Bank", "State Bank of India", "SBI", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Kotak Bank", "Bank of Baroda", "Canara Bank", "Union Bank"]
    merchants = ["Swiggy", "Zomato", "Amazon", "Flipkart", "Uber", "Blinkit", "Myntra", "IRCTC", "Zepto", "DMart", "Tata Neu", "Paytm Merchant", "Apollo Pharmacy"]
    last4_list = ["**4821", "XX9012", "XX5432", "**3344", "XX1122", "**7788", "XX6543", "**2211", "ending 8901", "ending 4321"]
    toll_frees = ["1800 202 6161", "1800 1234", "1800 1080", "1860 267 7777", "1800 258 4455", "1800 425 3800", "1800 11 2211", "1800 102 1661"]

    # --- ENGLISH HARD NEGATIVES (70 samples) ---
    en_legit_templates = [
        "{bank}: Rs {amt} debited from a/c {last4} on {date} for {merch}. Avl Bal: Rs {bal}. Ref: {ref}. If not done by you, call {tf}.",
        "{bank}: INR {amt} debited from A/C {last4} at ATM WDL. Avl Bal: INR {bal}. If not you, SMS BLOCK to 567676 or call {tf}.",
        "{bank}: Your A/C {last4} is debited with INR {amt} on {date} via UPI (Ref No {ref}). Avl Bal: INR {bal}. Call {tf} if not done by you.",
        "₹{amt} debited from {bank} a/c no. {last4} on {date} at {merch}. UPI Ref {ref}. Call {tf} for dispute. NEVER share OTP/PIN.",
        "{bank} Alert: Account {last4} debited for Rs {amt} towards {merch}. Available Balance: Rs {bal}. Ref #{ref}. Visit branch or call {tf} if not recognized.",
        "{bank}: Payment of Rs {amt} done using Card {last4} at {merch}. Total Bal: Rs {bal}. Txn ID {ref}. Call {tf} if not authorized. Bank never asks for PIN.",
        "Dear Customer, A/C {last4} debited by INR {amt} on {date}. Info: {merch}. Avl Bal: Rs {bal}. Dispute? Call {tf} or SMS BLOCK to 567678."
    ]

    for t_idx, tpl in enumerate(en_legit_templates):
        for i in range(10):
            bank = random.choice(banks)
            merch = random.choice(merchants)
            amt = f"{random.randint(50, 4500):,}.{random.choice(['00', '50', '25', '75'])}"
            bal = f"{random.randint(5000, 95000):,}.{random.choice(['00', '50'])}"
            last4 = random.choice(last4_list)
            ref = str(random.randint(100000000000, 999999999999))
            date = f"{random.randint(1, 28)}-Nov-26"
            tf = random.choice(toll_frees)
            text = tpl.format(bank=bank, amt=amt, last4=last4, date=date, merch=merch, bal=bal, ref=ref, tf=tf)
            samples.append({
                "template_id": f"legit_cb_hardneg_en_{t_idx + 1}",
                "category": "legitimate",
                "language": "en",
                "text": text,
                "label": "legitimate"
            })

    # --- HINDI HARD NEGATIVES (45 samples) ---
    hi_legit_templates = [
        "{bank}: खाता {last4} से ₹{amt} डेबिट हुए ({merch})। उपलब्ध शेष: ₹{bal}। संदर्भ: {ref}। यदि आपने नहीं किया तो {tf} पर कॉल करें। ओटीपी कभी साझा न करें।",
        "{bank} सूचना: आपके खाते {last4} से ₹{amt} की निकासी हुई। शेष राशि: ₹{bal}। यूपीआई संदर्भ {ref}। अनधिकृत होने पर टोल फ्री {tf} पर संपर्क करें।",
        "प्रिय ग्राहक, आपके खाते {last4} से ₹{amt} कटे हैं ({date})। शेष: ₹{bal}। यदि यह आपने नहीं किया, तो 567676 पर एसएमएस ब्लॉक भेजें या {tf} पर कॉल करें।",
        "{bank}: कार्ड {last4} द्वारा {merch} पर ₹{amt} का भुगतान सफल। शेष बैलेंस: ₹{bal}। संदर्भ सं. {ref}। सहायता हेतु कॉल करें: {tf}।"
    ]

    for t_idx, tpl in enumerate(hi_legit_templates):
        for i in range(11 if t_idx < 3 else 12):
            bank = random.choice(banks)
            merch = random.choice(merchants)
            amt = f"{random.randint(100, 3500):,}"
            bal = f"{random.randint(8000, 65000):,}"
            last4 = random.choice(last4_list)
            ref = str(random.randint(100000000000, 999999999999))
            date = f"{random.randint(1, 28)} Nov"
            tf = random.choice(toll_frees)
            text = tpl.format(bank=bank, amt=amt, last4=last4, date=date, merch=merch, bal=bal, ref=ref, tf=tf)
            samples.append({
                "template_id": f"legit_cb_hardneg_hi_{t_idx + 1}",
                "category": "legitimate",
                "language": "hi",
                "text": text,
                "label": "legitimate"
            })

    # --- TELUGU HARD NEGATIVES (45 samples) ---
    te_legit_templates = [
        "{bank}: మీ ఖాతా {last4} నుండి ₹{amt} డెబిట్ చేయబడింది ({merch}). నిల్వ: ₹{bal}. రిఫరెన్స్: {ref}. మీరు చేయకపోతే టోల్ ఫ్రీ {tf} కు కాల్ చేయండి.",
        "{bank} అలర్ట్: మీ అకౌంట్ {last4} నుండి ₹{amt} UPI ద్వారా చెల్లించబడింది. మిగిలిన బ్యాలెన్స్: ₹{bal}. లావాదేవీ నం: {ref}. సహాయం కోసం {tf} కు డయల్ చేయండి.",
        "ప్రియమైన కస్టమర్, మీ ఖాతా {last4} నుండి ₹{amt} విత్‌డ్రా అయింది. అందుబాటులో ఉన్న నిల్వ: ₹{bal}. ఈ లావాదేవీ మీరు చేయకపోతే వెంటనే {tf} కు కాల్ చేయండి.",
        "{bank}: కార్డ్ {last4} ద్వారా {merch} వద్ద ₹{amt} చెల్లింపు విజయవంతమైంది. బ్యాలెన్స్: ₹{bal}. రిఫరెన్స్ {ref}. బ్యాంక్ ఎప్పుడూ పిన్ అడగదు. సందేహాలకు {tf}."
    ]

    for t_idx, tpl in enumerate(te_legit_templates):
        for i in range(11 if t_idx < 3 else 12):
            bank = random.choice(banks)
            merch = random.choice(merchants)
            amt = f"{random.randint(100, 3500):,}"
            bal = f"{random.randint(8000, 65000):,}"
            last4 = random.choice(last4_list)
            ref = str(random.randint(100000000000, 999999999999))
            tf = random.choice(toll_frees)
            text = tpl.format(bank=bank, amt=amt, last4=last4, merch=merch, bal=bal, ref=ref, tf=tf)
            samples.append({
                "template_id": f"legit_cb_hardneg_te_{t_idx + 1}",
                "category": "legitimate",
                "language": "te",
                "text": text,
                "label": "legitimate"
            })

    print(f"Generated {len(samples)} natural bank hard negative samples.")
    return samples

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, "data", "synthetic_scam_dataset.csv")

    df_existing = pd.read_csv(dataset_path)
    print(f"Existing dataset rows: {len(df_existing)}")

    # Check if already added
    if (df_existing["category"] == "fake_debit_alert_callback").sum() > 0:
        print("fake_debit_alert_callback rows already present! Removing previous runs to ensure clean append...")
        df_existing = df_existing[df_existing["category"] != "fake_debit_alert_callback"].reset_index(drop=True)
        df_existing = df_existing[~df_existing["template_id"].str.startswith("legit_cb_hardneg_")].reset_index(drop=True)

    scam_samples = generate_callback_scam_samples()
    legit_samples = generate_genuine_hard_negatives()

    df_new = pd.DataFrame(scam_samples + legit_samples)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_csv(dataset_path, index=False)
    print(f"Successfully saved updated dataset with {len(df_combined)} rows to {dataset_path}.")
    print("New category breakdown:")
    print(df_combined["category"].value_counts())

if __name__ == "__main__":
    main()
