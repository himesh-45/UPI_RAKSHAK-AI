# UPI Rakshak AI — 3-Minute Evaluator Demo Script

> **Objective**: Walk judges through the core capabilities of UPI Rakshak AI in under 3 minutes, showing evidence-based detection, multilingual reasoning, static URL analysis, QR parsing, and the admin dashboard.

---

## ⏱️ Minute 0:00 – 0:45 | Overview & The Classic Scam Test

1. **Open the Web UI**:
   - Navigate to `http://localhost:5173`.
   - Highlight the banner: **Offline-First • Evidence-Based • Multilingual (EN / HI / TE)**.
   - Explain the philosophy: *"We do NOT ask an LLM 'is this a scam?'. Instead, independent detectors for NLP, deterministic rules, URLs, and QR codes mathematically fuse evidence into a calibrated safety report."*

2. **Run Demo Sample #1 (Classic OTP & Block Threat)**:
   - Under the text box, click the chip: `Classic OTP / Block Threat`.
   - Input populates: *"Your UPI account will be blocked. Click here to verify immediately and enter your OTP: http://sbi-kyc-verify.top/verify"*
   - Click **Analyze Threat**.
   - **Show Judges**:
     - **Score**: `85–95 / 100` (`HIGH RISK`).
     - **Itemized Evidence List**: Points out the Credential Theft Attempt (OTP request), Artificial Urgency (Block threat), and Deceptive Link with Phishing Keywords.
     - **Recommended Actions**: *"Do NOT share your OTP, UPI PIN, or CVV. Bank employees will NEVER ask for your secret PIN."*
     - **National Helpline Banner**: Direct button to dial `1930` and link to `cybercrime.gov.in`.

---

## ⏱️ Minute 0:45 – 1:30 | Multilingual Detection (Telugu & Hindi)

1. **Test Native Telugu Scam**:
   - Switch language to **తెలుగు** in top navbar, or click the chip: `Telugu Bank KYC Scam (తెలుగు)`.
   - Input: *"ప్రియమైన వినియోగదారుడా, మీ SBI ఖాతా కేవైసీ పెండింగ్ ఉన్నందున ఈ రాత్రి బ్లాక్ చేయబడుతుంది. వెంటనే నవీకరించండి: http://sbi-kyc-update-portal.top"*
   - Click **Analyze Threat**.
   - **Show Judges**:
     - Language detected as Telugu (`te`).
     - Score: `HIGH RISK`.
     - Explanation rendered completely in native Telugu with actionable Do's and Don'ts.

2. **Test Hindi Electricity Disconnection Scam**:
   - Switch language to **हिंदी**, or click the chip: `Hindi Electricity Threat (हिंदी)`.
   - Input: *"प्रिय उपभोक्ता, आपके बिजली का बिल अपडेट नहीं होने के कारण आज रात 9:30 बजे बिजली काट दी जाएगी। तुरंत भुगतान करें: http://bijli-bill-pay.online/auth"*
   - Click **Analyze Threat**.
   - **Show Judges**:
     - Classified under `electricity_disconnection`.
     - Flags the coercive "आज रात 9:30 बजे" ultimatum and high-risk `.online` TLD.
     - Advises against calling personal numbers; cites official state utility portal.

---

## ⏱️ Minute 1:30 – 2:15 | QR Code Decoding & Hard Negative (Genuine Bank SMS)

1. **Test QR Code Inspection**:
   - Switch to the **Screenshot / QR** tab.
   - Click the chip: `Fake Cashback QR Image`.
   - The preview loads `qr_fake_cashback.png`.
   - Click **Analyze Threat**.
   - **Show Judges**:
     - The engine decodes `upi://pay` without opening or visiting it.
     - Detects anomaly: Payee name claims *"GPay Cashback Reward"*, but the destination VPA belongs to an individual personal address (`scammer891@okhdfcbank`).
     - Highlights the UPI architecture rule: *"Scanning a QR code ALWAYS debits funds; you can never receive cashback by scanning a QR."*

2. **Test Hard Negative (Genuine Bank Alert is SAFE)**:
   - Switch back to the **Message / SMS** tab.
   - Click the chip: `Genuine Bank Alert (Safe)`.
   - Input: *"HDFC Bank: An amount of Rs. 1,450.00 is debited from account ending 4821 on 21-Nov-2026 for UPI/Swiggy. Available balance: Rs. 24,190.00. NEVER share your OTP or PIN with anyone."*
   - Click **Analyze Threat**.
   - **Show Judges**:
     - Score: `< 20 / 100` (`SAFE`).
     - Notice: Although the word "OTP" appears, the rule engine recognizes the negative advisory context (*"NEVER share your OTP"*), preventing false positives.

---

## ⏱️ Minute 2:15 – 3:00 | Admin Intelligence Dashboard & Voice Assistant

1. **Admin Intelligence Dashboard**:
   - Click **Admin Intelligence** in the navbar.
   - Click the **Admin** button to log in with demo credentials: `admin@upirakshak.ai` / `AdminRakshak#2026`.
   - **Show Judges**:
     - Prominent label: `SIMULATED DEMO DATA – Seeded historical patterns alongside live analyses for evaluation purposes`.
     - Filter tabs: Toggle between **All Data**, **Live Data**, and **Simulated Seed Data**. Notice that the live checks performed in the previous minutes appear in the Live table!
     - Interactive Recharts: Category Distribution, 7-Day Trend, Language Breakdown, and Top Triggered Signals.

2. **Multilingual Voice Assistant**:
   - Click **AI Assistant** in the navbar.
   - Type or speak via microphone: *"నాకు ఈ మెసేజ్ వచ్చింది. ఇది నిజమా?"* or *"Someone sent a collect request for Rs 2500 cashback. Is it safe?"*.
   - Point out that the assistant's reply is strictly grounded in detector evidence and verified RAG citations (NPCI guidelines & 1930 helpline).

3. **Conclusion**:
   - 100% offline-ready, zero paid API dependencies, 53 passing automated tests.
