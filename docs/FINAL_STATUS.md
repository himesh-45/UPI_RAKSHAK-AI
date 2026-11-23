# UPI Rakshak AI — Final Engineering & Verification Status Report

**Audit Date**: November 2026  
**Status**: Ready for Hackathon Live Demonstration & Technical Submission  
**Repository State**: Clean, no secrets committed, no untracked dependencies, 216 passing tests  

---

## 1. Before vs. After Transformation Summary

| Evaluation Dimension | Legacy Baseline | Current Final Engineering Status | Impact / Validation |
| :--- | :--- | :--- | :--- |
| **Model Evaluation Rigor** | Claimed near-perfect score on leaky stratified random split | **0.8994 Macro-F1** on frozen Gold v1; **0.8624** on natural noisy human Gold v2 | Leakage-free `GroupShuffleSplit` on template IDs. Macro-F1 target strictly set to 0.8500 (Both Gold v1 and Gold v2 PASSED). |
| **Risk Fusion Scam Recall** | 91.84% (180/196) — Marked FAILED | **99.49%** (195/196 Gold v1) & **98.55%** (136/138 Gold v2) | Intercepts obscure attack vectors with zero network latency. |
| **Legitimate False Alarm Rate** | 2.73% (3 false alarms on bank SMS) | **0.00%** (0/110 on Gold v1) & **1.90%** (2/105 on expanded Gold v2); NLP-only FPR **2.86%** | Gold v2 expanded from 35 to 105 realistic legitimate communications (bank debit/credit alerts with OTP warnings, delivery PINs, receipts, telecom, chats). Both PASSED ($\le 3\%$). |
| **Marketplace QR Scam Precision** | 0.2619 (28 genuine messages misrouted) | **0.8125** (Gold v1) and **1.0000** (Gold v2) | Added 300+ hard negative merchant receipts and chat context. |
| **Static URL Scanner Metrics** | Zero measured accuracy; anecdotal | **Real-Feed**: 82.00% Phishing Recall, 1.60% Benign FPR on OpenPhish/Tranco; **Adversarial**: 98.60% Recall, 1.12% FPR on 357 targets (incl. 107 handwritten) | Non-circular benchmark with domain-disjoint train/test split. Zero network calls. |
| **Expected Calibration Error (ECE)** | 0.1328 (uncalibrated probability scores) | **0.0992** (Gold v1, PASSED) & **0.1206** (Gold v2, honestly reported FAILED) | Calibrated probabilities ensure risk scores reflect real-world attack probability. |
| **Taxonomy Coverage** | 8 basic categories | **15 Comprehensive Categories + Digital Arrest Extortion Engine** | Added collect fraud, AnyDesk, loan extortion, digital arrest coercion, QR scams, accidental transfers, task jobs. |
| **Adversarial Robustness** | Vulnerable to "O T P", leetspeak, prompt injection | **Resistant in our tests (35 prompt injection cases across en/hi/te)** | Tested via property-based and multilingual mutation tests in `test_mutations.py`. |
| **Automated Test Suite** | 53 tests | **216 Tests Passing (100% Pass Rate)** | Full unit, integration, mutation, consistency, domain-disjoint, channels, reputation, digital arrest, theme contrast, responsive viewports, load test, and packaging coverage. |
| **Omnichannel Deployment** | Web only | **Web PWA + Telegram Bot** | Multi-channel dispatcher with salted SHA-256 sender hashing, 20 msg/hr sliding rate limiter, and `/delete_data` right-to-be-forgotten. (WhatsApp planned roadmap channel requiring Meta Business approval). |
| **Community Reputation** | None | **Consensus-Gated Database with Anti-Poisoning Whitelist** | Consensus gating ($\ge 2$ distinct reporters), 24h per-entity limits, 30-day half-life decay, and immune bank domains. |
| **Credential Hygiene** | Admin password in README; `.admin_secret` in repo | **No Secrets Tracked**; random generated password in `.admin_secret` (git-ignored) | Verified via git tracking audits, clean `.gitignore`, and package inspection. |
| **Production Readiness** | No container hardening | **Multi-Stage Non-Root Docker & 50-Client CPU Load Tested** | Median ~32 ms text inference on AMD Ryzen AI 5 340 CPU (~100 ms with synchronous SQLite audit logging); 25.0 req/s under 50 concurrent clients with zero errors. |
| **Documentation Cleanliness** | Hand-typed metrics with contradictions; local paths | **Fully Programmatic Report Generation**; zero absolute local paths | Consistency asserted by automated test `test_evaluation_report_consistency.py`. |
| **Clean Submission Packaging** | No automated packaging script | `make package` / `package_submission.py` creates clean zip | Excludes `.venv`, `node_modules`, `.git`, `.pytest_cache`, `dist`, `*.db`, `.env`, `.admin_secret`. Verified by `test_packaging.py`. |

---

## 2. Programmatic Quality Gates Verification

All gates are derived dynamically from code comparisons (`value >= target` or `value <= target`):

```markdown
| Evaluation Quality Gate | Target Benchmark | Measured (Gold v1) | Gate (Gold v1) | Measured (Gold v2) | Gate (Gold v2) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Risk Fusion Scam Recall** | >= 95.0% | **99.49%** (195/196) | **PASSED** | **98.55%** (136/138) | **PASSED** |
| **Legitimate False Positive Rate (FPR)** | <= 3.0% | **0.00%** (0/110) | **PASSED** | **1.90%** (2/105) | **PASSED** |
| **15-Class NLP Macro-F1** | >= 0.8500 | **0.8994** | **PASSED** | **0.8624** | **PASSED** |
| **Expected Calibration Error (ECE)** | < 0.1000 | **0.0992** | **PASSED** | **0.1206** | **FAILED** |
```

### Static URL Scanner Quality Gates (Pure Static Engine)

```markdown
| URL Scanner Quality Gate | Target Benchmark | Measured Value | Gate Status | Dataset Details |
| :--- | :---: | :---: | :---: | :--- |
| **Real-Feed Phishing Recall** | >= 80.0% | **82.00%** | **PASSED** | OpenPhish holdout (n=100) |
| **Real-Feed Benign FPR** | <= 3.0% | **1.60%** | **PASSED** | Tranco top-1000 holdout (n=250) |
| **Synthetic Adversarial Recall** | >= 80.0% | **98.60%** | **PASSED** | Independent generator + 107 Handwritten (n=357) |
| **Synthetic Adversarial FPR** | <= 3.0% | **1.12%** | **PASSED** | Disjoint Benign + Whitelisted (n=357) |
```

### Assistant Brain Quality Gates (Grounded Multilingual Conversational Engine)

```markdown
| Assistant Benchmark Gate | Target Benchmark | Measured Value | 95% Confidence Interval | Gate Status |
| :--- | :---: | :---: | :---: | :---: |
| **Intent Classification Accuracy** | >= 90.0% | **100.00%** | [100.00%, 100.00%] | **PASSED** |
| **Intent Classification Macro-F1** | >= 0.8500 | **1.0000** | — | **PASSED** |
| **Help Retrieval Recall@1** | >= 80.0% | **96.67%** | [91.67%, 100.00%] | **PASSED** |
| **Help Retrieval Recall@2** | >= 90.0% | **98.33%** | [95.00%, 100.00%] | **PASSED** |
| **Harmful Scam Request Refusal** | >= 95.0% | **100.00%** | [100.00%, 100.00%] | **PASSED** |
| **Prompt Injection Defense Rate** | >= 95.0% | **100.00%** | [100.00%, 100.00%] | **PASSED** |
| **Non-Analyze Verdict Purity** | 100.0% | **100.00%** | [100.0%, 100.0%] | **PASSED** |
| **Median Offline Response Latency** | <= 50.0 ms | **9.59 ms** | P95: 11.28 ms | **PASSED** |
```

---

## 3. Six-Part Architectural Task Checklist

- [x] **Part A - Assistant Brain**: 6-class hybrid intent router, deterministic tool executor, 160-item RAG knowledge base (158 reviewed, 2 draft isolated), swappable template/API/Ollama generator, PII pre-masking, statutory domain allowlists, and daily rate limiter.
- [x] **Part B - Guardian Avatar & UI Components**: 5 SVG animation states (`idle`, `listening`, `scanning`, `safe`, `alert`), 4 starter inquiry cards, rich verdict/step/playbook cards, and interactive Learn & About modal dialogs.
- [x] **Part C - Conversational Features & Follow-ups**: Conversational context grounding (`how do i do that`), quick-reply follow-up chips, voice synthesis read-aloud via Web Speech API, copyable markdown steps, and feedback collection.
- [x] **Part D - Omnichannel Adapters & Share Assets**: Shared channel adapter with Telegram message caps (4000 chars), BotFather definitions in en/hi/te, 1200x630 PIL share card generator, and 640x640 guardian avatar endpoint. (WhatsApp integration staged for future Meta Business approval).
- [x] **Part E - Accessibility & Elder Mode**: High-contrast family/elder toggle, 18px+ readable typography, 3 prominent high-urgency action buttons, auto-speech readout, `aria-live` screen-reader regions, and WCAG AA contrast compliance.
- [x] **Part F - Evaluation Harness, Linguistic QA & Submission Packaging**: Programmatic evaluation harness with bootstrap confidence intervals, `docs/ASSISTANT_EVALUATION.md`, qualitative `docs/QA_LANGUAGE.md` audit, and automated clean zip builder.

---

## 4. Honest System Limitations & Tradeoffs

1. **Browser Web Speech API Dependency**:
   - Voice input for vernacular languages (`hi-IN`, `te-IN`) relies on browser-native SpeechRecognition engines (Chromium-based browsers like Chrome and Edge provide optimal support). If speech recognition is unsupported or network-blocked in the browser, users can type or paste text.
2. **Camera Artifacts on Physical QR Codes**:
   - Severe glare, physical creases, or low-resolution camera sensors may degrade QR matrix decoding. The application gracefully informs the user when a QR matrix cannot be resolved rather than guessing or fabricating results.
3. **Synthetic Training Distribution**:
   - Because real-world smishing data contains PII, the core NLP model was trained primarily on a carefully structured 12,800-sample synthetic dataset augmented with the public UCI SMS corpus. Zero-day evasion techniques with novel lexical tokens may require periodic active-learning retraining via the `/api/feedback` pipeline.
4. **Air-Gapped URL Scanning**:
   - Pure static lexical/structural analysis intentionally makes **zero outbound network requests**. While this guarantees zero SSRF and prevents attacker canary tokens from detonating, newly registered malicious domains that use non-bank brand stems on neutral TLDs without high-risk keywords will rely on our statistical URL ML model and NLP text context rather than live DNS blacklists.

---

## 5. Key Verification Commands

```bash
# 1. Run all automated backend tests (216 tests)
.\.venv\Scripts\pytest.exe backend/tests -v

# 2. Run Assistant Conversational & Guardrail Test Suite
.\.venv\Scripts\pytest.exe backend/tests/test_assistant_intent.py backend/tests/test_assistant_tools.py backend/tests/test_assistant_generator.py backend/tests/test_rag.py backend/tests/test_channels.py backend/tests/test_banned_phrases.py -v

# 3. Run Programmatic Assistant Benchmark Evaluation
.\.venv\Scripts\python.exe -m backend.app.scripts.evaluate_assistant

# 4. Regenerate Core Scam Models Programmatic Evaluation Report
.\.venv\Scripts\python.exe -m backend.app.scripts.evaluate_models

# 5. Build and verify clean submission package
.\.venv\Scripts\python.exe -m backend.app.scripts.package_submission
.\.venv\Scripts\pytest.exe backend/tests/test_packaging.py -v
```
