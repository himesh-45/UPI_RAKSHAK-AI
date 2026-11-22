# 💬 WhatsApp Bot Integration & Deployment Guide

This guide details configuring, running, and testing the **UPI Rakshak AI WhatsApp Bot** across both **Twilio Sandbox** and **Meta WhatsApp Cloud API**.

---

## 1. Features & Architecture

- **Unified Processing Core**: Shares the identical evidence fusion and privacy core as the web and Telegram channels.
- **Provider Agnostic**:
  - **Twilio WhatsApp API**: Ideal for developer sandboxes, hackathon demonstrations, and rapid prototyping.
  - **Meta WhatsApp Cloud API**: High-throughput official BSP infrastructure with interactive button messages.
- **Multimodal Scanning**:
  - Automatic download and RapidOCR/OpenCV analysis of forwarded payment screenshots and QR codes (up to 5MB).
  - Text, link, and VPA parsing.
- **Privacy By Design**:
  - Sender phone numbers are immediately hashed with salted SHA-256 (`SENDER_HASH_SALT`).
  - Text stored in history is sanitized through PII masking.
  - Command `/delete_data` permanently erases all scans associated with the user's hashed ID.

---

## 2. Configuration (`.env`)

Add the following environment variables to your `.env`:

```bash
# General Channel Privacy
SENDER_HASH_SALT="upi_rakshak_salt_2026_demo"
CHANNEL_RATE_LIMIT_PER_HOUR=20

# -------------------------------------------------------------------
# Option A: Twilio WhatsApp Sandbox
# -------------------------------------------------------------------
WHATSAPP_PROVIDER="twilio"
TWILIO_ACCOUNT_SID="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
TWILIO_AUTH_TOKEN="your_twilio_auth_token"
TWILIO_WHATSAPP_NUMBER="whatsapp:+14155238886"

# -------------------------------------------------------------------
# Option B: Meta WhatsApp Cloud API
# -------------------------------------------------------------------
# WHATSAPP_PROVIDER="meta"
# META_WHATSAPP_TOKEN="EAA..."
# META_PHONE_NUMBER_ID="100000000000000"
# META_VERIFY_TOKEN="your_webhook_verification_token"
# WHATSAPP_APP_SECRET="your_meta_app_secret"
```

---

## 3. Provider Setup

### Setting Up Twilio Sandbox (Fastest for Demo)
1. Log in to your Twilio Console and navigate to **Messaging -> Try it out -> Send a WhatsApp message**.
2. Connect your personal WhatsApp by sending the sandbox keyword (e.g., `join code-word`) to `+1 415 523 8886`.
3. In the Twilio Console Sandbox Settings:
   - **WHEN A MESSAGE COMES IN**:
     `POST https://your-domain.com/api/channels/whatsapp/twilio`
4. The bot will automatically respond with TwiML safety reports.

### Setting Up Meta WhatsApp Cloud API
1. Create an app on [developers.facebook.com](https://developers.facebook.com) with the **WhatsApp** product.
2. In **WhatsApp -> Configuration**:
   - **Callback URL**: `https://your-domain.com/api/channels/whatsapp/meta`
   - **Verify Token**: Match `META_VERIFY_TOKEN` in `.env`.
   - Click **Verify and Save** (Meta sends a GET request with `hub.challenge`).
   - Subscribe to the `messages` webhook field.
3. Add a test phone number and send a test message.

---

## 4. Offline Simulation & Testing

You can verify the WhatsApp processing pipeline without needing a live Twilio account or Meta developer credentials:

```bash
# Test Hindi Collect Request Scam
python -m backend.app.scripts.simulate_whatsapp --text "बधाई हो! आपको Google Pay पर ₹3,000 कैशबैक मिला है। तुरंत पाने के लिए पिन दर्ज करें।" --lang hi

# Test English KYC Phishing Link
python -m backend.app.scripts.simulate_whatsapp --text "SBI alert: Update KYC at http://onlinesbi.sbi.co.in.kyc-verify.top or account blocked"

# Test Right-to-be-Forgotten (/delete_data)
python -m backend.app.scripts.simulate_whatsapp --cmd /delete_data
```

Automated unit tests covering signature validation, challenge handshakes, rate limits, and PII protection:

```bash
pytest backend/tests/test_channels.py -v
```
