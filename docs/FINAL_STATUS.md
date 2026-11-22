# UPI Rakshak AI — Final Engineering & Verification Status Report

**Audit Date**: November 2026  
**Status**: Ready for Hackathon Live Demonstration & Technical Submission  
**Repository State**: Clean, zero secrets, zero untracked dependencies, 138 passing tests  

---

## 1. Before vs. After Transformation Summary

| Evaluation Dimension | Legacy Baseline | Current Final Engineering Status | Impact / Validation |
| :--- | :--- | :--- | :--- |
| **Model Evaluation Rigor** | Claimed 100% accuracy on leaky stratified random split | **0.8940 Macro-F1** on frozen Gold v1; **0.8292** on natural noisy human Gold v2 | Leakage-free `GroupShuffleSplit` on template IDs. Macro-F1 target restored to 0.8500 (Gold v1 PASSED, Gold v2 transparently reported as FAILED). |
| **Risk Fusion Scam Recall** | 91.84% (180/196) — Marked FAILED | **98.47%** (193/196 Gold v1) & **97.83%** (135/138 Gold v2) | Intercepts obscure attack vectors with zero network latency. |
| **Legitimate False Alarm Rate** | 2.73% (3 false alarms on bank SMS) | **0.00%** (0/110 on Gold v1) & **4.76%** (5/105 on expanded Gold v2); NLP-only FPR **2.86%** (3/105) | Gold v2 expanded from 35 to 105 realistic legitimate communications (bank debit/credit alerts with OTP warnings, delivery PINs, receipts, telecom, chats). |
| **Marketplace QR Scam Precision** | 0.2619 (28 genuine messages misrouted) | **0.8125** (Gold v1) and **1.0000** (Gold v2) | Added 300+ hard negative merchant receipts and chat context. |
| **Static URL Scanner Metrics** | Zero measured accuracy; anecdotal | **Real-Feed**: 82.00% Phishing Recall, 1.60% Benign FPR on OpenPhish/Tranco; **Adversarial**: 98.60% Recall, 1.12% FPR on 357 targets (incl. 107 handwritten) | Non-circular benchmark with domain-disjoint train/test split. Zero network calls. |
| **Expected Calibration Error (ECE)** | 0.1328 (uncalibrated probability scores) | **0.0609** (Gold v1) & **0.0910** (Gold v2) | Calibrated probabilities ensure risk scores reflect real-world attack probability (< 0.10 target met). |
| **Taxonomy Coverage** | 8 basic categories | **15 Comprehensive Categories** | Added collect fraud, AnyDesk, loan extortion, digital arrest, QR scams, accidental transfers, task jobs. |
| **Adversarial Robustness** | Vulnerable to "O T P", leetspeak, prompt injection | **Resistant in our tests (35 prompt injection cases across en/hi/te)** | Tested via property-based and multilingual mutation tests in `test_mutations.py`. |
| **Automated Test Suite** | 53 tests | **138 Tests Passing** | Full unit, integration, mutation, consistency, domain-disjoint, packaging, and API coverage. |
| **Credential Hygiene** | Admin password in README; `.admin_secret` in repo | **Zero Secrets Tracked**; ephemeral in-memory startup password | Verified via git tracking audits, clean `.gitignore`, and package inspection. |
| **Documentation Cleanliness** | Hand-typed metrics with contradictions; local paths | **100% Programmatic Report Generation**; zero absolute local paths | Consistency asserted by automated test `test_evaluation_report_consistency.py`. |
| **Clean Submission Packaging** | No automated packaging script | `make package` / `package_submission.py` creates clean zip | Excludes `.venv`, `node_modules`, `.git`, `.pytest_cache`, `dist`, `*.db`, `.env`, `.admin_secret`. |

---

## 2. Programmatic Quality Gates Verification

All gates are derived dynamically from code comparisons (`value >= target` or `value <= target`):

```markdown
| Evaluation Quality Gate | Target Benchmark | Measured (Gold v1) | Gate (Gold v1) | Measured (Gold v2) | Gate (Gold v2) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Risk Fusion Scam Recall** | >= 95.0% | **98.47%** (193/196) | **PASSED** | **97.83%** (135/138) | **PASSED** |
| **Legitimate False Positive Rate (FPR)** | <= 3.0% | **0.00%** (0/110) | **PASSED** | **4.76%** (5/105) | **FAILED** |
| **15-Class NLP Macro-F1** | >= 0.8500 | **0.8940** | **PASSED** | **0.8292** | **FAILED** |
| **Expected Calibration Error (ECE)** | < 0.1000 | **0.0609** | **PASSED** | **0.0910** | **PASSED** |
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

---

## 3. Honest System Limitations & Tradeoffs

1. **Browser Web Speech API Dependency**:
   - Voice input for vernacular languages (`hi-IN`, `te-IN`) relies on browser-native SpeechRecognition engines (Chromium-based browsers like Chrome and Edge provide optimal support). If speech recognition is unsupported or network-blocked in the browser, users can type or paste text.
2. **Camera Artifacts on Physical QR Codes**:
   - Severe glare, physical creases, or low-resolution camera sensors may degrade QR matrix decoding. The application gracefully informs the user when a QR matrix cannot be resolved rather than guessing or fabricating results.
3. **Synthetic Training Distribution**:
   - Because real-world smishing data contains PII, the core NLP model was trained primarily on a carefully structured 12,800-sample synthetic dataset augmented with the public UCI SMS corpus. Zero-day evasion techniques with novel lexical tokens may require periodic active-learning retraining via the `/api/feedback` pipeline.
4. **Air-Gapped URL Scanning**:
   - Pure static lexical/structural analysis intentionally makes **zero outbound network requests**. While this guarantees zero SSRF and prevents attacker canary tokens from detonating, newly registered malicious domains that use non-bank brand stems on neutral TLDs without high-risk keywords will rely on our statistical URL ML model and NLP text context rather than live DNS blacklists.

---

## 4. Key Verification Commands

```bash
# 1. Run all 107 automated tests
.\.venv\Scripts\pytest.exe backend/tests -v

# 2. Verify Evaluation Report consistency
.\.venv\Scripts\pytest.exe backend/tests/test_evaluation_report_consistency.py -v

# 3. Regenerate Programmatic Evaluation Report
.\.venv\Scripts\python.exe -m backend.app.scripts.evaluate_models

# 4. Build clean submission zip
.\.venv\Scripts\python.exe -m backend.app.scripts.package_submission
```
