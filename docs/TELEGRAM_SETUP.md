# 🤖 Telegram Bot Integration & Deployment Guide

This guide details configuring, running, and testing the official **UPI Rakshak AI Telegram Bot** (`@upirakshak_bot`).

---

## 1. Features & Architecture

- **Channel Agnostic Core**: Powered by [`backend/app/channels/core.py`](../backend/app/channels/core.py).
- **Multimodal Threat Scans**:
  - **Text & Forwarded SMS**: Real-time 15-class NLP intent + Regex Safety Rules + Air-gapped URL analysis.
  - **Payment Screenshots & QR Codes**: Automatic OCR and UPI URI extraction (`pa`, `pn`, `am`, `tn`).
  - **Voice Notes**: Multi-lingual offline privacy fallback notice.
- **Interactive Action Buttons**:
  - `🚨 Dial 1930 Cyber Helpline` (Links directly to official national portal)
  - `🇮🇳 हिंदी में समझें` (Hindi Vernacular Re-explanation)
  - `🇮🇳 తెలుగులో వివరణ` (Telugu Vernacular Re-explanation)
  - `📋 Report Scam` (Flags threat to intelligence analyst queue)
  - `🗑️ Delete My Data` (Permanently purges all scans for this user)
- **Privacy & GDPR/DPDP Compliance**:
  - Raw Telegram user IDs and usernames are **never persisted**.
  - Identifiers are irreversibly hashed using a salted SHA-256 algorithm (`SENDER_HASH_SALT`).
  - Raw user messages are sanitized through PII masking (bank accounts, phone numbers, and OTPs redacted).
  - Group chat messages are processed only when mentioned, and **never stored in the database**.

---

## 2. Configuration (`.env`)

Add the following environment variables to your `.env`:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"
TELEGRAM_BOT_USERNAME="upirakshak_bot"

# Optional: Webhook Secret Token for Production
TELEGRAM_WEBHOOK_SECRET="random_secure_hex_token"

# Salt for One-Way Sender ID Hashing
SENDER_HASH_SALT="upi_rakshak_salt_2026_demo"

# Rate Limiting
CHANNEL_RATE_LIMIT_PER_HOUR=20
```

---

## 3. Creating a Bot via BotFather

1. Open Telegram and search for `@BotFather`.
2. Send `/newbot`.
3. Choose a name: `UPI Rakshak AI`.
4. Choose a username: `upi_rakshak_demo_bot` (or similar).
5. Copy the generated HTTP API Token into `TELEGRAM_BOT_TOKEN` in `.env`.

---

## 4. Running the Bot

### Mode A: Local Development / Demo (Long Polling)
No public URL, ngrok, or SSL certificate required. Simply execute:

```bash
python -m backend.app.channels.telegram --poll
```

### Mode B: Production Webhooks
If running on a public server or Cloud Run with HTTPS:

```bash
# Register the webhook with Telegram API
curl -F "url=https://your-domain.com/api/channels/telegram/webhook" \
     -F "secret_token=random_secure_hex_token" \
     https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/setWebhook
```

---

## 5. Offline Simulation & Testing

You can verify the Telegram processing pipeline without needing a live Telegram API token:

```bash
# Test text scam analysis
python -m backend.app.scripts.simulate_telegram --text "Urgent: SBI KYC suspended. Enter OTP at http://sbi-kyc.top"

# Test QR code / screenshot analysis
python -m backend.app.scripts.simulate_telegram --image backend/app/data/demo_assets/qr_fake_cashback.png

# Test Right-to-be-Forgotten (/delete_data)
python -m backend.app.scripts.simulate_telegram --cmd /delete_data
```

Automated unit tests covering webhook signature validation, rate limits, and privacy hashing:

```bash
pytest backend/tests/test_channels.py -v
```
