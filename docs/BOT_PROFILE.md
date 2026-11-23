# Official Bot Profile & Configuration Guide (Telegram & WhatsApp)

> **Profile Identifier**: `@UPIRakshakBot`  
> **Bot Name**: `UPI Rakshak Guardian`  
> **Avatar Asset**: `docs/assets/guardian_avatar.png` (640x640 PNG, high-contrast cyber guardian emblem)

---

## 1. Telegram BotFather Configuration

### A. Bot Name (`/setname`)
```text
UPI Rakshak Guardian
```

### B. Short Description (`/setshortdescription`)
Shown on the bot's invite link and preview page (maximum 120 characters):

- **English**:
  ```text
  Evidence-based AI guardian defending against UPI fraud, digital arrest, and phishing. Multi-lingual & offline-ready.
  ```
- **Hindi (`/setshortdescription` -> `hi`)**:
  ```text
  यूपीआई फ्रॉड, डिजिटल अरेस्ट और फर्जी संदेशों से सुरक्षा देने वाला आधिकारिक एआई रक्षक।
  ```
- **Telugu (`/setshortdescription` -> `te`)**:
  ```text
  యూపీఐ మోసాలు, డిజిటల్ అరెస్ట్ బెదిరింపుల నుండి రక్షించే అధికారిక ఏఐ డిజిటల్ గార్డియన్.
  ```

### C. Description (`/setdescription`)
Shown before users tap "Start" in the bot window:

- **English**:
  ```text
  🛡️ Welcome to UPI Rakshak Guardian — your evidence-based digital payments safety assistant.

  What I can do:
  • Analyze suspicious SMS, links, UPI IDs, and QR codes before you pay.
  • Explain 1930 Cyber Helpline & cybercrime.gov.in complaint procedures.
  • Provide Golden Hour emergency playbooks if money was lost.
  • Explain how to verify bank alerts and identify digital arrest scams.

  🔒 Privacy Guarantee:
  We never store your raw phone numbers or plain-text OTPs. Sender IDs are one-way hashed with salted SHA-256.
  ```

- **Hindi (`/setdescription` -> `hi`)**:
  ```text
  🛡️ यूपीआई रक्षक में आपका स्वागत है — वित्तीय साइबर सुरक्षा और डिजिटल भुगतान रक्षक।

  मैं आपकी क्या सहायता कर सकता हूँ:
  • किसी भी संदिग्ध एसएमएस, लिंक, यूपीआई आईडी या क्यूआर कोड की त्वरित जांच।
  • राष्ट्रीय साइबर हेल्पलाइन 1930 और cybercrime.gov.in पर शिकायत दर्ज करने के नियम।
  • पैसे कटने पर 'गोल्डन ऑवर' आपातकालीन सुरक्षा कदम।
  • डिजिटल अरेस्ट और बिजली बिल फ्रॉड की पहचान।

  🔒 पूर्ण डेटा गोपनीयता:
  हम आपका फोन नंबर या संदेश स्टोर नहीं करते। सभी आईडी हैश द्वारा सुरक्षित हैं।
  ```

- **Telugu (`/setdescription` -> `te`)**:
  ```text
  🛡️ యూపీఐ రక్షక్ కు స్వాగతం — మీ డిజిటల్ చెల్లింపుల సైబర్ రక్షకుడు.

  నేను ఎలా సహాయపడగలను:
  • అనుమానాస్పద ఎస్ఎంఎస్, లింకులు, యూపీఐ ఐడీలు మరియు క్యూఆర్ కోడ్ల తనిఖీ.
  • జాతీయ హెల్ప్‌లైన్ 1930 మరియు cybercrime.gov.in లో ఫిర్యాదు చేసే మార్గదర్శకాలు.
  • డబ్బులు పోయినప్పుడు గోల్డెన్ అవర్ అత్యవసర నివారణ చర్యలు.
  • డిజిటల్ అరెస్ట్ మరియు నకిలీ కాల్స్ గుర్తింపు.

  🔒 పూర్తి గోప్యత:
  మీ ఫోన్ నంబర్లు లేదా వ్యక్తిగత వివరాలు మా వద్ద నిల్వ చేయబడవు.
  ```

### D. About Text (`/setabouttext`)
Shown in the bot's profile card (maximum 120 characters):
```text
Official citizen fraud protection assistant. Grounded in NPCI, RBI, and I4C (1930) safety frameworks.
```

### E. Bot Commands List (`/setcommands`)
Copy-paste this exact block directly into `@BotFather`:

```text
start - Initialize Rakshak Assistant and view capabilities
check - Scan a suspicious SMS, UPI ID, payment link, or script
report - Guidelines on filing complaints via 1930 & cybercrime.gov.in
emergency - Immediate Golden Hour steps if money was lost or OTP shared
help - How-to guides, FAQ, and payment safety rules
language - Switch between English, हिंदी, and తెలుగు
delete_data - Permanently erase all analysis records linked to your hashed ID
```

---

## 2. WhatsApp Business Profile Specifications

For Cloud API (Meta for Developers) or Twilio WhatsApp Console:

- **Business Display Name**: `UPI Rakshak Guardian`
- **Category**: `Finance & Technology Security`
- **Business Description**:  
  `Evidence-based conversational safety brain helping Indian citizens detect UPI scams, block rogue handles, and file reports with the national 1930 helpline. Zero PII stored.`
- **Official Website**: `https://upirakshak.ai`
- **Support Email**: `help@upirakshak.ai`
- **Profile Picture**: Use `docs/assets/guardian_avatar.png` (640x640px).

---

## 3. Interactive Keyboards & Fallbacks

- **Telegram**: Renders native inline buttons (`InlineKeyboardMarkup`) with callback data (`dial_1930`, `check_another`, `emergency_steps`, `lang_hi`, `lang_te`, `delete_data`).
- **WhatsApp Cloud API**: Uses interactive Quick Reply Buttons and List Messages for supported business numbers.
- **WhatsApp Fallback**: Emits clean formatted numbered lists when conversational buttons are not provisioned on the sender's carrier plan.
