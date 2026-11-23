# Rakshak Assistant — Comprehensive Evaluation Report

> **Methodology Standard**:
> All metrics are mathematically computed from execution against the held-out test datasets in `docs/assistant_eval/`.
> Zero hand-typed or simulated benchmark values.
> Generated on: **2026-11-23 18:51:58 UTC**

---

## 1. Executive Metric Summary

| Evaluation Metric | Measured Value | 95% Confidence Interval | Target Threshold | Gate Status |
| :--- | :---: | :---: | :---: | :---: |
| **Intent Classification Accuracy** | **100.00%** | [100.00%, 100.00%] | ≥ 90.0% | **PASSED** |
| **Intent Classification Macro-F1** | **1.0000** | — | ≥ 0.8500 | **PASSED** |
| **Help Retrieval Recall@1** | **96.67%** | [91.67%, 100.00%] | ≥ 80.0% | **PASSED** |
| **Help Retrieval Recall@2** | **98.33%** | [95.00%, 100.00%] | ≥ 90.0% | **PASSED** |
| **Harmful Scam Request Refusal** | **100.00%** | [100.00%, 100.00%] | ≥ 95.0% | **PASSED** |
| **Prompt Injection Defense Rate** | **100.00%** | [100.00%, 100.00%] | ≥ 95.0% | **PASSED** |
| **Non-Analyze Verdict Purity** | **100.00%** | [100.0%, 100.0%] | 100.0% | **PASSED** |
| **Median Offline Response Latency** | **9.59 ms** | P95: 11.28 ms | ≤ 50.0 ms | **PASSED** |

---

## 2. Intent Confusion Matrix

Evaluated across 150 multilingual held-out samples in English, Hindi, Telugu, and Hinglish.

```text
Labels: ['ANALYZE', 'EMERGENCY', 'GREETING', 'HELP', 'OUT_OF_SCOPE', 'UNCLEAR']
Confusion Matrix:
[[30  0  0  0  0  0]
 [ 0 30  0  0  0  0]
 [ 0  0 20  0  0  0]
 [ 0  0  0 30  0  0]
 [ 0  0  0  0 20  0]
 [ 0  0  0  0  0 20]]
```

---

## 3. Groundedness & Safety Guardrails Verification

1. **PII Masking**: Indian mobile numbers (`[PHONE]`), bank accounts (`[ACCOUNT]`), and OTP digits (`[OTP]`) are pre-masked before any external LLM processing.
2. **Statutory Domain Whitelisting**: Any URL or phone number not in statutory registries (`cybercrime.gov.in`, `rbi.org.in`, `npci.org.in`, `sancharsaathi.gov.in`) is stripped and replaced with official portal verification links.
3. **Zero Synthetic Verdicts**: The language model is strictly prohibited from generating `SAFE`, `SUSPICIOUS`, or `HIGH RISK` verdicts. Scam scores originate solely from deterministic detectors.
4. **Fail-Safe Fallback**: Any external network timeout (15s), missing key, or daily cap exhaustion triggers instantaneous offline template fallback without user interruption.