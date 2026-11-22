# Security Architecture & Threat Model
**Project:** UPI Rakshak AI  
**Classification:** Defensive Cybersecurity & Digital Financial Trust  
**Version:** 2.0.0  
**Date:** November 2026  

---

## 1. Security Philosophy: Evidence-Based & Air-Gapped Trust

UPI Rakshak AI is engineered under a zero-trust, privacy-first threat model. Because users submit active phishing links, live scam SMS, and screenshots containing sensitive banking data, the platform must guarantee that:
1. **The scanner itself never becomes an attack vector:** Suspicious URLs and QR codes are NEVER fetched, DNS-resolved, or executed over the network.
2. **Citizen privacy is inviolable:** All phone numbers, card numbers, and 2FA OTPs are masked *prior* to database persistence.
3. **No security by obscurity:** Ephemeral credential generation and rate-limiting protect against abuse without hardcoded secrets.

---

## 2. STRIDE Threat Model & Mitigations

| STRIDE Category | Specific Threat in Payment Scams | Platform Countermeasure | Implementation Module |
| :--- | :--- | :--- | :--- |
| **Spoofing** | Attacker creates homoglyph domain (e.g. `sbi-kyc.com`) or claims to be "SBI Support" on a personal UPI handle (`sbi@ybl`). | Strict registered-domain matching using `tldextract`, 88 Indian brand definitions, Levenshtein edit distance analysis, and VPA institutional handle verification. | `backend/app/detectors/url_scanner.py`, `backend/app/core/vpa_verifier.py` |
| **Tampering** | Attacker modifies QR code parameters (`upi://pay`) or injects zero-width whitespace/homoglyphs to evade token filters. | QR deep link parameter validation; NFKC Unicode normalization, zero-width space stripping, Cyrillic homoglyph unmasking, and leetspeak de-obfuscation. | `backend/app/core/normalizer.py`, `backend/app/detectors/qr_scanner.py` |
| **Repudiation** | Scammer denies sending a collect request or creating a fraudulent link; victim lacks evidence for police. | Automatic generation of standardized CFCFRMS formal complaint narratives with extracted timestamps, phone numbers, and URLs for filing on 1930 / `cybercrime.gov.in`. | `backend/app/fusion/risk_engine.py`, `PreFilled1930Modal.jsx` |
| **Information Disclosure** | User pastes private SMS containing bank account numbers, OTPs, or debit card numbers into the analyzer. | Dual-layer regex masking (`mask_sensitive_data`) replaces Indian 10-digit mobile numbers, 16-digit PANs/cards, and 4-8 digit OTPs with `[REDACTED]` before writing to SQLite. | `backend/app/core/masking.py` |
| **Denial of Service (DoS)** | Attacker floods analysis endpoint with automated requests or uploads 500MB video files to exhaust server RAM; ReDoS via crafted regex. | In-memory sliding-window IP rate limiter (60 req/min with automatic prune of stale IPs); strict 5 MB file size limit; atomic non-backtracking regex patterns. | `backend/app/core/security.py`, `backend/app/routes/analyze.py` |
| **Elevation of Privilege** | Attacker accesses administrative dashboard using default/hardcoded passwords found in public git repositories. | Zero hardcoded passwords. Ephemeral 16-character CSPRNG secret generated on startup and saved to git-ignored `.admin_secret`. JWT tokens signed with SHA-256 HMAC. | `backend/app/config.py`, `backend/app/core/auth.py` |

---

## 3. Zero-Network Execution Standard (SSRF Prevention)

A critical vulnerability in naive URL scanners is Server-Side Request Forgery (SSRF) and malware detonation when the server attempts to `curl`, `fetch`, or follow HTTP redirects for submitted links. If an attacker submits `http://169.254.169.254/latest/meta-data/` or an active exploit kit link, a naive scanner can be exploited.

### Architectural Guarantee:
- **No HTTP/HTTPS requests:** The backend makes **0** network calls to scanned URLs.
- **No DNS queries:** Domains are not resolved via socket DNS.
- **Pure Static Lexical Analysis:** All features (TLD reputation, entropy, homoglyphs, brand edit distances, IP hosts, path tokens) are evaluated purely via offline string algorithms.
- **Automated Verification:** Verified by automated regression test `test_url_scanner_makes_zero_network_calls` in `backend/tests/test_mutations.py` which monkeypatches `urllib`, `requests`, and `socket` to assert zero socket connections.

---

## 4. Adversarial Evasion Defense (Mutation Robustness)

Scammers continuously mutate message text to bypass keyword filters:
1. **Zero-Width Injections:** Inserting `\u200B` inside `"O\u200BT\u200BP"` to defeat regex matchers.
   - *Defense:* `text_normalizer.strip_zero_width()` strips all zero-width spaces, joiners, and bidirectional markers.
2. **Cyrillic & Greek Homoglyphs:** Using Cyrillic `а` (U+0430) instead of Latin `a` (U+0061) in `"bаnk"`.
   - *Defense:* `text_normalizer.unmask_homoglyphs()` maps 30+ visual lookalike characters back to standard Latin ASCII.
3. **Leetspeak De-obfuscation:** Substituting `1` for `l` or `i`, `0` for `o`, `@` for `a` (e.g. `"cl1ck h3re"`).
   - *Defense:* Contextual regex transforms common leetspeak substitutions before token extraction.
4. **Acronym Spacing:** Writing `"O T P"` or `"P I N"`.
   - *Defense:* Acronym fusion regex compresses single-spaced uppercase characters into unified tokens.

---

## 5. Ephemeral Credential & Secret Management

1. **Admin Credentials:**
   - On first startup, if `ADMIN_PASSWORD` is not explicitly declared in `.env`, the server generates a cryptographically secure 16-character alphanumeric token using `secrets.token_urlsafe(16)`.
   - The token is persisted to `backend/data/.admin_secret` (explicitly git-ignored) and printed once to stdout.
   - `.env.example` contains only non-sensitive placeholder templates.
2. **JWT Secret:**
   - `JWT_SECRET_KEY` falls back to an ephemeral token per process lifetime if undeclared in production environments.
3. **Third-Party API Keys:**
   - UPI Rakshak AI requires no third-party API keys (no OpenAI, Gemini, or Anthropic keys needed for detection). All detection and RAG retrieval runs locally without internet.

---

## 6. Coordinated Vulnerability Disclosure

If you discover a potential security flaw in UPI Rakshak AI, please report it privately:
- **Email:** `security@upirakshak.local`
- **PGP Key:** Available upon request
- **Response SLA:** Acknowledgment within 24 hours, patch deployment within 72 hours.
