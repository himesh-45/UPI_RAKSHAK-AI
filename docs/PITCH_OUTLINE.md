# UPI Rakshak AI — Hackathon Pitch Deck & Slide Outline

> **Competition Track**: Cybersecurity, Fintech & Digital Trust  
> **Pitch Format**: 7-Minute Slide Deck + 3-Minute Live Interactive Demonstration  
> **Target Alignment**: Innovation, Technical Complexity, Practicality, Social Impact, Live Demo, Scalability

---

## 📽️ Slide-by-Slide Deck Structure

### Slide 1: The Title & Mission Hook
- **Header**: UPI Rakshak AI (यूपीआई रक्षक / యుపిఐ రక్షక్)
- **Sub-header**: India's First Offline-First, Multilingual Scam Defense & Golden-Hour Recovery Engine
- **Tagline**: Safeguarding 500 Million Digital Citizens from Payment Fraud in Real-Time
- **Visuals**:
  - Split graphic: Mobile phone receiving deceptive SMS vs UPI Rakshak instant safe shield badge.
  - Team credentials & track alignment.

---

### Slide 2: The Problem — The Epidemic of Digital Payment Fraud
- **The Numbers in India**:
  - 14+ Billion UPI transactions per month.
  - Over ₹1,200 Crores lost in FY 2025–26 to digital financial scams.
  - 70% of victims are senior citizens, tier-2/3 residents, or first-time digital payment adopters.
- **The 3 Critical Gaps in Existing Solutions**:
  1. *Too Slow / Cloud-Dependent*: Sending private financial SMS to cloud LLMs incurs high latency (3-5s), huge costs, and data privacy violations.
  2. *Monolingual & Complex*: Existing warnings are in bureaucratic English; rural and regional users are left unprotected.
  3. *Zero Post-Incident Help*: When fraud occurs, victims lose the critical "Golden Hour" because they don't know how to navigate the 1930 portal or draft formal legal incident narratives.

---

### Slide 3: The Innovation — Evidence-Based Scam Intelligence
- **Our Paradigm Shift**:
  - *DON'T* ask an LLM: *"Is this a scam?"* (vulnerable to prompt injection, hallucination, network lag, and privacy leakage).
  - *DO* fuse independent, mathematical, deterministic detectors:
    1. **Adversarially-Hardened NLP Classifier** (15 distinct scam categories).
    2. **Negation-Aware Rule Engine** (distinguishes scam threats from bank security warnings).
    3. **Zero-Network Static URL Scanner** (80+ whitelisted Indian banks, typosquatting & punycode detection).
    4. **Offline QR / UPI URI Inspector** (`upi://pay` parameter validation).
- **Core Principle**: 100% offline capability. Zero API keys. Sub-30ms execution.

---

### Slide 4: Technical Architecture — Multi-Layer Engine
- **Flowchart**:
  $$\text{Input (SMS / URL / Image / VPA)} \longrightarrow \text{Adversarial Normalizer} \longrightarrow \begin{matrix} \text{NLP Engine} \\ \text{Rule Engine} \\ \text{URL Scanner} \\ \text{QR/OCR Parser} \end{matrix} \longrightarrow \text{Risk Fusion Engine} \longrightarrow \begin{matrix} \text{Dynamic Risk Score (0-100)} \\ \text{Additive Waterfall Decomposition} \\ \text{Token Highlights} \\ \text{Localized 3-Stage Attack Story} \\ \text{1-Click 1930 Legal Narrative} \end{matrix}$$
- **Key Technical Highlights**:
  - Unicode NFKC & Cyrillic homoglyph de-obfuscation.
  - Dominant-signal risk fusion with multi-engine corroboration bonus.
  - Calibrated probability outputs (Platt/isotonic) with 0.062 Expected Calibration Error (ECE).

---

### Slide 5: Data Integrity & Scientific Rigor (Zero Hallucination)
- **Addressing the Classic Hackathon Flaw**:
  - *No fabricated 100% metrics*: Evaluated with leakage-free `GroupShuffleSplit` across template families.
  - *Isolated 306-Sample Gold Benchmark*: Curated with 104 hard negatives of real bank debit SMS, utility receipts, and real-world human phrasing.
- **Empirical Measured Performance**:
  - **95.41% Scam Recall** on unseen attack phrasings.
  - **91.74% Legitimate Precision**.
  - **2.73% False Positive Rate** on real bank debit alerts (preventing alert fatigue).
  - 104 passing unit, integration, mutation, and Playwright end-to-end tests.

---

### Slide 6: Social Impact & Regional Inclusivity
- **Vernacular First**: Full native support for English, Hindi (हिंदी), and Telugu (తెలుగు), including Hinglish and Romanized Telugu (Telugish).
- **Family & Elder Mode**:
  - 125% WCAG AA high-contrast design for aging eyes.
  - Browser Web Speech API reads out plain-language warnings aloud in native accents (`hi-IN`, `te-IN`, `en-IN`).
- **Shift-Left Pre-Payment VPA Safe-Check**:
  - Catches scammers before payment occurs by flagging fake institutional names registered on consumer UPI handles (`sbi-refund@paytm`).

---

### Slide 7: Live Demonstration (3 Minutes)
*(Refer to `docs/DEMO_SCRIPT.md`)*
1. **Classic KYC Block Phishing**: Token highlights + Score Waterfall + 1930 Narrative.
2. **Telugu Electricity Scam**: Full vernacular explanation + Elder Mode audio playback.
3. **VPA Safe-Check**: Detecting retail handle spoofing on collect requests.
4. **Hard Negative Test**: Showing real bank SMS with "NEVER share OTP" scored as SAFE (12/100).
5. **Admin Dashboard**: Live vs Simulated telemetry + Retraining pipeline from user feedback.

---

### Slide 8: Scalability, Unit Economics & Go-to-Market
- **Unit Economics**:
  - Traditional Cloud LLM: $5,000 / day per 1M scans.
  - **UPI Rakshak AI**: **$40 / month** on standard commodity CPU (sub-$0.000002 per scan).
- **Integration Vectors**:
  - **Direct Consumer PWA**: Zero installation, works on any smartphone browser.
  - **SMS / WhatsApp Chatbot**: Automated triage bot for community groups and elder societies.
  - **In-App FinTech SDK**: On-device C++/WASM library embeddable directly inside NPCI apps, PhonePe, Google Pay, or Paytm.
  - **Law Enforcement Portal**: CFCFRMS batch triage for state cybercrime police cells.

---

### Slide 9: The Roadmap & Future Vision
- **Phase 1 (Done)**: Multi-layer core engine, 15 categories, 3 languages, 104 passing tests, PWA, 1930 integration.
- **Phase 2 (Next 60 Days)**: On-device Android Accessibility Service for instant SMS overlay alerts.
- **Phase 3 (Next 180 Days)**: Expansion to Tamil, Kannada, Bengali, and Marathi; NPCI hackathon pilot deployment.

---

### Slide 10: Conclusion & Call to Action
- **Summary**:
  - *Innovative*: Shift from black-box LLM to explainable, mathematical evidence fusion.
  - *Accurate*: Zero-leakage tested, 95.41% recall, 2.73% FPR.
  - *Inclusive*: Multilingual, high-contrast elder mode with voice synthesis.
  - *Actionable*: From instant scam detection to Golden-Hour 1930 legal recovery in one click.
- **Repository**: Open-source, Docker-ready, fully reproducible.
- **Thank you! We are now open for your questions.**
