# UPI Rakshak AI — Architectural & Implementation Decisions

This document records technical and design decisions made to keep the system robust, demo-ready, and compliant with all project requirements.

## 1. Zero External API Dependency (Offline First)
- **Decision**: The entire core engine (NLP, static URL scanner, QR parser, OCR, RAG retrieval, and risk fusion) operates 100% offline without requiring internet access or third-party API keys.
- **Rationale**: Real-world fraud analysis must be fast, private, and resilient to third-party downtime or quotas. Any LLM provider (Gemini or Anthropic) is purely optional behind a feature flag; when no key is configured, a deterministic multilingual template engine produces grounded explanations.

## 2. Evidence-Based Fusion vs. LLM "Vibes"
- **Decision**: The final risk score (0–100) and verdict (`SAFE`, `SUSPICIOUS`, `HIGH RISK`) are calculated mathematically by the `RiskFusionEngine` through weighted signal accumulation and safety overrides, NOT by asking an LLM.
- **Rationale**: LLMs hallucinate and can be jailbroken by deceptive phishing prompts. A deterministic fusion of verified signals (OTP request, collect request anomaly, brand typosquatting, urgency threats) ensures explainability and consistent safety guarantees.

## 3. Honest OCR Engine & RapidOCR Integration
- **Decision**: Tesseract C++ OCR is used when present; `rapidocr-onnxruntime` operates as an instant pip-installable fallback that runs locally on ONNX runtime. If no OCR engine is available, the system honestly reports `ocr_available: false` and instructs the user to paste text. No mock/fabricated results are ever returned.
- **Rationale**: Eliminates system dependency failures while maintaining strict honesty and transparency.

## 4. Sensitive Data Masking Before Storage
- **Decision**: All incoming analysis inputs are stripped of identifiable credentials before saving to SQLite. Phone numbers (`\b[6-9]\d{9}\b`), 12-16 digit account numbers, 4-6 digit OTPs, and private UPI IDs are masked as `[REDACTED_PHONE]`, `[REDACTED_OTP]`, etc. Users can also pass `save_history: false` for confidential checks.
- **Rationale**: Privacy-by-design is non-negotiable for financial fraud detection.

## 5. Synthetic Dataset Generation & Disclaimer
- **Decision**: We generate 10,800+ synthetic multilingual samples covering 15 distinct scam categories across English, Hindi, Telugu, Hinglish, and Romanized Telugu, supplemented with 2,000 real public SMS messages from the UCI SMS Spam corpus.
- **Rationale**: Real scam data contains active malicious URLs, personal victim phone numbers, and PII. Fictionalized samples ensure model training without privacy or ethical risks. A clear disclaimer is rendered in `EVALUATION_REPORT.md` and the UI.

## 6. Static-Only URL Analysis
- **Decision**: The URL scanner NEVER performs HTTP requests, socket connections, or DNS resolutions against suspicious domains.
- **Rationale**: Resolving attacker-controlled domains can alert attackers (canary tokens), trigger malicious payloads, or expose evaluator IP addresses. Pure static analysis (edit distance, entropy, TLD risk, homoglyphs) is safe and fast.

## 7. Multilingual Grounding
- **Decision**: The Assistant and explanations strictly support English, Hindi (`hi-IN`), and Telugu (`te-IN`). All i18n strings are maintained in synchronized JSON bundles, and explanations cite factual RAG passages and 1930 Cybercrime Helpline protocols.

## 8. Group-Level Splits & Independent Gold Test Set
- **Decision**: All model evaluation uses `GroupShuffleSplit` on template/source IDs combined with MinHash near-duplicate deduplication. A hand-curated **Gold Test Set** of 306 samples (including 110 hard negatives and 45 natural messy human messages) is strictly isolated and never trained or tuned on.
- **Rationale**: Eliminates template memorization and data leakage, delivering true generalizability and defensible metrics during technical evaluation.

## 9. Integration of Real Public Data
- **Decision**: Supplement synthetic data with real public corpora (UCI SMS Spam Collection, open smishing sets, Tranco benign domains, public phishing feeds). Document all sources, licenses, and collection methodology in `docs/DATA_SOURCES.md`.
- **Rationale**: Grounds the model in real-world human phrasing, typos, and SMS conventions alongside controlled synthetic attack patterns.

## 10. Honest OCR Availability Reporting
- **Decision**: Eliminate any mock/silent OCR fallbacks. If Tesseract and fallback OCR engines are unavailable on the host, the backend honestly surfaces `ocr_available: false` and instructs the user to paste text.
- **Rationale**: Absolute transparency is critical for cybersecurity tools. Fabricating or guessing OCR results violates core hackathon trust criteria.

## 11. Ephemeral Admin Password Generation
- **Decision**: Remove all default passwords from documentation, `.env.example`, and frontend source code. If `ADMIN_PASSWORD` is not configured in `.env`, the server generates a cryptographically random 16-character string on first startup, prints it to stdout once, and stores a salted bcrypt hash.
- **Rationale**: Eliminates default credential vulnerabilities.

## 12. Extended Taxonomy to 15 Categories
- **Decision**: Expand scam classification from 8 legacy categories to 15 comprehensive categories reflecting modern digital fraud in India (collect requests, AnyDesk remote access, loan app harassment, courier/customs parcels, marketplace QR scams, accidental transfer scams, job/crypto tasks).
- **Rationale**: Matches real-world threat intelligence reported to 1930 / MHA.

## 13. Dominant-Signal Evidence Fusion with Corroboration
- **Decision**: In cybersecurity risk assessment, averaging dilutes acute threats. Risk score is computed from the dominant credible detector signal (Calibrated NLP, Rules, URL Scanner, QR Anomaly) with additive corroboration bonuses when 2 or more independent detectors flag the threat.
- **Rationale**: Prevents high-risk phishing links from being downplayed by short or neutral text accompanying the URL.

## 14. Context-Aware Negation & Warning Context Suppression
- **Decision**: The rule safety layer evaluates context windows for negation phrases ("never share your OTP", "do not disclose your PIN", "bank never asks for confidential details") and Delivery OTP instructions ("share OTP only upon delivery"). Genuine security advisories trigger negative risk weighting and score suppression (`<= 20`, `SAFE`).
- **Rationale**: Completely prevents false positive flagging on genuine bank notifications containing mandatory RBI security warnings.

## 15. 88 Official Indian Brands with Strict Registered-Domain Matching
- **Decision**: Expanded official entities to 88 Indian public/private banks, state DISCOMs, government portals, and payment apps. The URL scanner uses `tldextract` registered-domain verification to ensure subdomain tricks (e.g. `sbi.co.in.evil.xyz`) are flagged as critical brand impersonation while genuine subdomains (`retail.onlinesbi.sbi`) remain safe.
- **Rationale**: Defends against the most prevalent modern phishing evasion tactic in Indian digital banking.

### Decision 16: Localized 3-Stage Attack Anatomy Timeline (Scam Story Engine)
- **Choice**: Implemented deterministic, localized 3-stage timelines (`scam_story_engine`) in English, Hindi, and Telugu covering all 15 fraud categories.
- **Rationale**: LLM generation in production introduces latency, hallucinations, and non-deterministic advice. Deterministic playbooks based on real-world cybercrime telemetry provide instant, authoritative step-by-step guidance.

### Decision 17: Token-Level Highlighting & Score Waterfall Decomposition
- **Choice**: Computed character offsets (`HighlightSpan`) for acute threat tokens and an additive/subtractive step-by-step points decomposition (`WaterfallStep`).
- **Rationale**: Solves the black-box AI criticism by showing judges and users exactly which detector contributed how many points and which specific phrases triggered alerts.

### Decision 18: Pre-Filled 1930 Citizen Cybercrime Complaint Generator
- **Choice**: Automatically structured extracted telephone numbers, suspect URLs, and payee VPAs into a standardized CFCFRMS formal complaint template.
- **Rationale**: Victims reporting to `cybercrime.gov.in` during panic struggle to articulate technical details. Pre-formatting the narrative with UTR placeholders maximizes the chance of freezing mule accounts during the Golden Hour.

### Decision 19: Offline RAG Expansion to 89 Verified Regulatory Entries
- **Choice**: Expanded knowledge base from 8 to 89 authoritative entries covering NPCI circulars, RBI customer protection frameworks, top 10 Indian bank emergency hotlines, and cyber law provisions.
- **Rationale**: Replaces superficial tips with legally cited actionable guidance while maintaining sub-millisecond offline TF-IDF retrieval speed.

### Decision 20: Pre-Payment UPI ID (VPA) Safe-Check Engine
- **Choice**: Built dedicated VPA validator evaluating handle PSP registry, retail vs. institutional brand spoofing, and collect-request trick flags.
- **Rationale**: Shifts scam defense left—preventing transfers before authorization occurs rather than merely diagnosing fraud after financial loss.

### Decision 21: Continuous Improvement Feedback Loop
- **Choice**: Added `/api/feedback` endpoint persisting user corrections to SQLite and an automated retrain staging script (`retrain_from_feedback.py`).
- **Rationale**: Enables judges to inspect how real-world false positives/negatives are audited and incorporated into subsequent training iterations.

### Decision 22: Family/Elder Mode with Web Speech API Audio Synthesis
- **Choice**: Integrated high-contrast large font toggle and browser-native SpeechSynthesisUtterance in `en-IN`, `hi-IN`, and `te-IN`.
- **Rationale**: Addresses critical accessibility needs for senior citizens and low-literacy users without requiring heavy third-party audio API keys.

### Decision 23: Security Hardening & Zero-Network Guarantee
- **Choice**: Enforced 5MB maximum file upload cap, sliding-window rate limiting with 5-minute stale IP prune, and pure static offline analysis with 0 socket connections to scanned URLs.
- **Rationale**: Prevents DoS memory exhaustion, SSRF vulnerabilities, and malicious link detonation while protecting user privacy.


### Decision 24: Comprehensive Zero-Network CI/CD Pipeline & Automated Verification Gate
- **Choice**: Created `.github/workflows/ci.yml` orchestrating headless Python 3.11 test execution, Tesseract OCR system packages (`eng`, `hin`, `tel`), leakage-free ML evaluation gate verification, URL security benchmark, and Node.js Vite production build.
- **Rationale**: Guarantees repeatable, automated verification of code quality, model accuracy thresholds, and frontend assets on every commit without external API dependencies.

### Decision 25: 100% Secret-Free Deployment Architecture & Credential Hardening
- **Choice**: Removed all default hardcoded admin passwords from `README.md`, `docker-compose.yml`, and documentation. The backend generates a random 16-character credential on first boot if `ADMIN_PASSWORD` is unset, prints it once to the console, and stores it in `data/.admin_secret`.
- **Rationale**: Completely eliminates hardcoded credential vulnerabilities in public repositories and enforces production security best practices.

### Decision 26: Complete 3-Minute Live Judge Presentation Script & 20-Point Technical Defense Matrix
- **Choice**: Authored comprehensive evaluation documentation (`docs/DEMO_SCRIPT.md`, `docs/JUDGE_QA.md`, and `docs/PITCH_OUTLINE.md`) detailing the 3-minute live presentation flow, answers to 20 tough technical judge questions, and slide-by-slide pitch deck alignment.
- **Rationale**: Equips the team with rigorous empirical defense points, code citations, and live demo choreography targeting maximum scoring across all hackathon evaluation criteria.
