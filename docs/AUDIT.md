# UPI Rakshak AI — Comprehensive Architectural, Security & ML Audit

**Date**: November 2026  
**Auditor**: Senior ML Engineer, Security Reviewer & Product Designer  
**Scope**: Full codebase audit (`backend/app`, `frontend/src`, `backend/tests`, `docs/`, `docker-compose.yml`)

---

## 1. Executive Summary

UPI Rakshak AI established a solid foundational architecture with multi-signal fusion, offline-first design, and native multilingual support (English, Hindi, Telugu). However, a rigorous audit reveals critical credibility gaps, model evaluation deficiencies, security oversights, and limited coverage of modern Indian cyber fraud vectors. 

This audit documents each finding, root cause, severity, and the remediation roadmap across Phases 1 to 5.

---

## 2. Detailed Findings by Area

### 2.1 Machine Learning, Data & Evaluation Gaps
- **Finding 1.1: Artificial 100% Accuracy from Template Memorization (CRITICAL)**
  - *Location*: [`docs/MODEL_REPORT.md`](MODEL_REPORT.md), [`backend/app/scripts/train_model.py`](../backend/app/scripts/train_model.py)
  - *Root Cause*: Random stratified train/test split on ~3,600 template-generated synthetic samples. Identical template sentence skeletons existed across both train and test partitions. The model memorized template boilerplate rather than learning generalizable semantic fraud signals.
  - *Impact*: In a live hackathon demo or tough judge cross-examination, claiming "100% accuracy" immediately destroys technical credibility.
  - *Remediation*: Implement leakage-free `GroupShuffleSplit` grouping by template ID and MinHash/cosine near-duplicate deduplication. Introduce a completely independent, hand-crafted **Gold Test Set** of 300+ samples (including 100+ hard negatives and 40 natural messy human messages) that is never trained or tuned on.

- **Finding 1.2: 100% Synthetic Data & Narrow Category Taxonomy (HIGH)**
  - *Location*: [`backend/app/scripts/generate_dataset.py`](../backend/app/scripts/generate_dataset.py)
  - *Root Cause*: Data is solely synthetically generated across only 8 legacy categories, omitting the most rampant UPI and digital payment scams in India today.
  - *Missing Categories*:
    1. Collect-request / "enter PIN to receive money" fraud (`collect_request_fraud`)
    2. Remote-access app takeovers (`remote_access_scam`: AnyDesk, TeamViewer, QuickSupport)
    3. Job / Part-time / Telegram / Crypto investment tasks (`job_investment_scam`)
    4. Instant loan-app blackmail and extortion (`loan_app_extortion`)
    5. Fake courier / customs / FedEx parcel seized with narcotics (`courier_customs_scam`)
    6. Marketplace / OLX fake QR code buyer scams (`marketplace_qr_scam`)
    7. Accidental transfer / "wrong number sent money, please return" (`accidental_transfer_scam`)
  - *Remediation*: Ingest real public SMS corpora (UCI SMS Spam, smishing feeds) and expand synthetic generation to 10,000+ samples from 60+ varied templates per category with typos, leetspeak, emoji padding, and mixed scripts.

- **Finding 1.3: Lack of Probability Calibration & Text Normalization (HIGH)**
  - *Location*: [`backend/app/detectors/nlp_classifier.py`](../backend/app/detectors/nlp_classifier.py)
  - *Root Cause*: Raw classifier probabilities were uncalibrated, with no reporting of Expected Calibration Error (ECE) or Brier score. Simple adversarial evasions (e.g., "O T P", "cl1ck", zero-width spaces, Cyrillic homoglyphs) bypassed word-level tokenizers. Language detection relied solely on small keyword heuristics.
  - *Remediation*: Add NFKC normalization, zero-width space removal, leetspeak de-obfuscation, character-ngram language detection, and Platt/isotonic probability calibration.

### 2.2 Security & Credential Hygiene
- **Finding 2.1: Hardcoded Admin Password in Public Documentation (CRITICAL)**
  - *Location*: [`README.md`](../README.md), [`frontend/src/components/LoginModal.jsx`](../frontend/src/components/LoginModal.jsx), [`backend/app/config.py`](../backend/app/config.py)
  - *Root Cause*: Default demo credentials `admin@upirakshak.ai` / `AdminRakshak#2026` were hardcoded in multiple docs and components.
  - *Remediation*: Purge all plaintext passwords from documentation. Read admin credentials strictly from `.env`. On first run if `ADMIN_PASSWORD` is unset, generate a cryptographically secure random password via `secrets.token_urlsafe(16)`, output it once to stdout, and persist a salted bcrypt hash.

- **Finding 2.2: Git Index Tracking `__pycache__` Artifacts (MEDIUM)**
  - *Location*: Git tracking index
  - *Root Cause*: Compiled Python `.pyc` files in `backend/app/__pycache__` and `backend/tests/__pycache__` were tracked by git despite `.gitignore`.
  - *Remediation*: Remove cached `.pyc` and `__pycache__` artifacts from git index and enforce clean repository hygiene.

### 2.3 URL Scanner Evaluation & Coverage Gaps
- **Finding 3.1: No Measured Performance on Held-Out Domain Feeds (HIGH)**
  - *Location*: [`backend/app/detectors/url_scanner.py`](../backend/app/detectors/url_scanner.py)
  - *Root Cause*: URL scanner rules had unit tests for a few examples, but lacked empirical measurement (Precision, Recall, F1) against held-out phishing URLs and benign domain lists.
  - *Remediation*: Build a benchmark dataset of 500+ phishing URLs and 500+ benign domains (from OpenPhish/PhishTank and Tranco) with domain-level train/test splits. Add 80+ Indian banking, UPI, NBFC, and government entity domains to the impersonation registry with strict registered-domain matching (e.g., ensuring `sbi.co.in.evil.com` is flagged while `sbi.co.in` is safe).

### 2.4 OCR Reliability & Honesty
- **Finding 4.1: Silent Empty Result on Host OCR Absence (HIGH)**
  - *Location*: [`backend/app/detectors/ocr_pipeline.py`](../backend/app/detectors/ocr_pipeline.py)
  - *Root Cause*: When Tesseract binaries were absent on the host OS, text extraction silently failed and returned `""`, leading the backend to evaluate an empty string without informing the user.
  - *Remediation*: Provide honest OCR state reporting in the API and UI (`ocr_available: false`, `"OCR engine unavailable on host; paste text or deploy via Docker"`). Integrate RapidOCR / EasyOCR as a pip-installable fallback that works without host C++ packages, while ensuring Dockerfile installs Tesseract with `eng`, `hin`, and `tel` traineddata.

### 2.5 RAG Knowledge Base Breadth
- **Finding 5.1: Small Knowledge Base (8 Entries) (MEDIUM)**
  - *Location*: [`backend/app/rag/knowledge_base.json`](../backend/app/rag/knowledge_base.json)
  - *Root Cause*: The knowledge base had only 8 entries, lacking coverage for courier scams, loan harassment, SIM swapping, mule accounts, chargebacks, and state-specific utility boards.
  - *Remediation*: Expand to 60+ concise, factual entries citing NPCI, RBI Master Circulars, SEBI advisories, CERT-In, and the 1930 Golden Hour protocol.

### 2.6 Product, Explainability & User Experience Gaps
- **Finding 6.1: Lack of Token-Level Explainability (MEDIUM)**
  - *Location*: Frontend Result Card
  - *Root Cause*: Users could see signals, but could not see *which exact words or tokens* in their message triggered the detection.
  - *Remediation*: Add inline token-level highlighting with interactive tooltips and a waterfall chart decomposing the score contribution per detector.

- **Finding 6.2: Missing Critical Victim Flows (HIGH)**
  - *Location*: Frontend Action Box & Assistant
  - *Root Cause*: If a victim has already sent money or entered their PIN, generic advice is insufficient.
  - *Remediation*: Add an **Emergency Mode** with step-by-step Golden Hour actions (Call 1930, bank fraud desk numbers, account freeze), a **Scam Story/Timeline** explaining how the scam unfolds, a **VPA / Collect Request Verifier**, a **PWA manifest** for mobile quick-sharing, and a **Family / Elder Mode** with large fonts and voice readout.

---

## 3. Remediation Matrix

| Area | Current State | Target State | Phase |
|---|---|---|---|
| **Dataset** | 3,600 synthetic rows, 8 classes | 10,000+ synthetic + real public SMS/URLs, 15 classes, 300+ gold set | Phase 1 |
| **Splitting** | Random row split (leakage) | `GroupShuffleSplit` on template IDs + MinHash deduplication | Phase 1 |
| **Model** | Uncalibrated TF-IDF Logistic Regression | Calibrated Ensemble + engineered features + text normalizer | Phase 1 |
| **URL Scanner** | 21 domains, unmeasured accuracy | 80+ Indian brands, strict domain matching, evaluated on held-out data | Phase 1 |
| **OCR** | Silent empty fallback | Honest state in API/UI, RapidOCR/EasyOCR fallback, Docker packs | Phase 1 |
| **RAG Knowledge** | 8 entries | 60+ verified entries across all scam vectors | Phase 1 & 2 |
| **Explainability** | General bullets only | Inline token-level highlighting + Score Waterfall | Phase 2 |
| **UX & Features** | Basic cards | Elder mode, Scam timeline, Emergency mode, VPA checker, PWA | Phase 2 & 3 |
| **Security** | Hardcoded credentials | Random admin password, zero secrets in repo, network-isolation test | Phase 4 |
| **Tests & CI** | 53 unit tests | 100+ tests (property, mutation, Playwright e2e) + GitHub Actions CI | Phase 5 |

---

*Audit completed. Proceeding directly to Phase 1 execution.*
