# UPI Rakshak AI — 3-Minute Hackathon Demo Video & Voiceover Script

This document provides the definitive, second-by-second screen recording script for the 3-minute hackathon submission video.

---

## Technical Specifications
- **Target Duration**: Exactly 3 minutes (180 seconds)
- **Resolution**: 1920x1080 (16:9), 60 FPS
- **Audio**: Clean 48kHz microphone audio, studio voiceover
- **Host**: `http://localhost:5173` (with clean browser profile, bookmarks bar hidden, 100% zoom)
- **Live Channels**: Telegram Bot (`@upi_rakshak_bot`) open on mobile phone or desktop client

---

## Second-by-Second Video Script

### 0:00 – 0:30 | The Crisis & The Architectural Principle
- **Visual**: Start on the clean, modern dark-mode home interface (`/`). The badge reads *"Multilingual Scam Detection • Offline-First"*.
- **Camera/Cursor**: Smooth zoom towards the multi-layered analysis tabs.
- **Voiceover**:
  > *"Every month, India processes over 13 billion UPI transactions. But alongside financial inclusion came an explosion in psychological extortion: fake bank KYC closures, OLX collect-request traps, and coercive 'Digital Arrest' scams. Victims don't lose money because their software was hacked—they lose money because they were deceived.*
  > 
  > *Meet UPI Rakshak AI: an evidence-based, offline-first fraud detection engine supporting English, Hindi, and Telugu (core engine runs without internet; bots need internet). Unlike chatbots that ask an LLM 'is this a scam?', our verdict is derived deterministically from independent mathematical detectors running on a commodity CPU in ~32 milliseconds."*

---

### 0:30 – 1:15 | Omnichannel Protection: Telegram Bot & Live Mobile QR
- **Visual**: Switch to the **"Judge / Try"** portal (`/try`). Show the live QR codes: Web App and Telegram Bot.
- **Action**: Pick up a smartphone on camera and scan the Telegram QR code. Forward a suspicious SMS:
  `"Dear Customer, your SBI account is blocked. Update PAN card at http://sbi-kyc-update.top"`
- **Visual**: In under 1 second, Telegram replies with the detailed safety report: **HIGH RISK (100/100)**, listing brand typosquatting, phishing keywords, and actionable advice.
- **Voiceover**:
  > *"Real users don't copy-paste text into a web app when they're in panic. They live in messaging apps. Watch as I forward a phishing SMS to our Telegram bot on my phone.*
  > 
  > *Instantly, it replies with a complete breakdown in their language. Notice that every sender identity is salted and hashed with SHA-256 before storage, and phone numbers are completely masked. If the user types `/delete_data`, their entire audit trail is permanently purged, honoring the Digital Personal Data Protection Act."*

---

### 1:15 – 2:00 | Digital Arrest Extortion & Statutory Legal Grounding
- **Visual**: Navigate to the **"Digital Arrest"** module (`/arrest`).
- **Action**: Click the preset scenario: **"FedEx Narcotics Parcel (Mumbai Police)"**. Click **"Analyze Call Script / Threat"**.
- **Visual**: Immediate display: **CRITICAL ALERT: COERCIVE DIGITAL EXTORTION (Score: 100/100)**.
  Highlight the amber **"Statutory Legal Truth"** banner citing **CrPC Section 41 / BNSS Section 35**.
- **Voiceover**:
  > *"Now, let's examine India's fastest-growing cyber threat: Digital Arrest scams, where fraudsters pose as CBI or Mumbai Police demanding money for seized narcotics parcels.*
  > 
  > *UPI Rakshak AI identifies the deadly intersection of agency impersonation, contraband threats, and virtual confinement. But more importantly, it arms the victim with statutory Indian legal reality: Indian law recognizes no concept of 'Digital Arrest' or Skype courtrooms, and police never ask for money transfers to 'RBI escrow accounts'. It even formats an official complaint ready for National Helpline 1930."*

---

### 2:00 – 2:30 | Hard Negatives & Zero-Network Offline Speed
- **Visual**: Return to the main Analyzer (`/`). Click **"Quick Test Scenarios"** $\rightarrow$ **"Genuine Swiggy Refund & Bank SMS"**. Click **"Check Scam Threat"**.
- **Visual**: Instant verdict: **SAFE (Score: 0/100)**. Show the Waterfall chart displaying 0 points.
- **Voiceover**:
  > *"A fraud detector is useless if it panics on real messages. Here is a genuine refund confirmation with amounts and transaction IDs. Notice how our calibrated classifier scores it 0 out of 100—SAFE.*
  > 
  > *And examine our load test results: median CPU text inference latency is ~32 milliseconds, running on a standard laptop CPU without a single GPU. Core detection makes zero outbound network calls, meaning banks and defense intranets can deploy it locally without internet with zero data leakage."*

---

### 2:30 – 3:00 | Community Defense & Live 1930 Incident Reporting
- **Visual**: Show the **"VPA Reputation"** tab and the **"Prefilled 1930 Complaint Dossier"** modal.
- **Action**: Click **"Copy Formal Complaint"**. Confetti or green check appears.
- **Voiceover**:
  > *"When a victim is targeted, UPI Rakshak AI doesn't stop at an alert. It checks our crowd-consensus reputation database—protected against poisoning by consensus gating and immune whitelists—and pre-fills a formal cybercrime report for Helpline 1930.*
  > 
  > *From mobile messaging to air-gapped banking servers: UPI Rakshak AI brings digital trust and forensic protection to 1.4 billion Indians. Thank you."*

---

## Contingency & Fallback Plans
1. **If Telegram Bot is unreachable during live shoot**: Use the built-in interactive simulator (`python -m backend.app.channels.simulate_telegram`) or demonstrate the same input in the Web Analyzer.
2. **If Phone Camera doesn't focus on QR**: Click the direct hyperlink beneath the QR code on the desktop browser.
3. **Audio Check**: Ensure microphone levels are between -12dB and -6dB with zero background hum.
