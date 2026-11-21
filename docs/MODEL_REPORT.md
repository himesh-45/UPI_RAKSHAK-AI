# UPI Rakshak AI — NLP Model Report & Evaluation

> [!CAUTION]
> **SYNTHETIC DATASET DISCLAIMER**:
> This model was trained on a synthetic dataset generated via algorithmic templates, slot filling, and perturbation.
> The reported performance metrics reflect validation on this synthetic distribution and **do NOT represent real-world fraud detection accuracy or guarantees**.
> Real-world threat actors constantly vary their phrasing, domains, and evasion tactics.

## 1. Executive Summary
- **Architecture**: Dual Feature Extraction (Word n-grams (1, 2) + Char-wb n-grams (3, 5)) + Multiclass Logistic Regression
- **Training Samples**: 2880
- **Test Samples**: 720 (20% stratified holdout)
- **Overall Accuracy**: 100.00%
- **Inference Latency**: < 4ms per sample (CPU, single-threaded)
- **Supported Languages**: English, Hindi (Devanagari), Telugu (Telugu Script), Hinglish, Romanized Telugu

## 2. Per-Class Performance Metrics

| Category | Precision | Recall | F1-Score | Support |
| --- | --- | --- | --- | --- |
| `electricity_disconnection` | 1.0000 | 1.0000 | 1.0000 | 90 |
| `fake_bank_kyc` | 1.0000 | 1.0000 | 1.0000 | 90 |
| `fake_customer_support` | 1.0000 | 1.0000 | 1.0000 | 90 |
| `fake_govt_scheme` | 1.0000 | 1.0000 | 1.0000 | 90 |
| `fake_upi_refund_cashback` | 1.0000 | 1.0000 | 1.0000 | 90 |
| `legitimate` | 1.0000 | 1.0000 | 1.0000 | 90 |
| `lottery_prize` | 1.0000 | 1.0000 | 1.0000 | 90 |
| `otp_pin_theft` | 1.0000 | 1.0000 | 1.0000 | 90 |

- **Macro Average F1**: 1.0000
- **Weighted Average F1**: 1.0000

## 3. Confusion Matrix

| True \ Pred | electricity_disconnection | fake_bank_kyc | fake_customer_support | fake_govt_scheme | fake_upi_refund_cashback | legitimate | lottery_prize | otp_pin_theft |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **electricity_disconnection** | 90 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **fake_bank_kyc** | 0 | 90 | 0 | 0 | 0 | 0 | 0 | 0 |
| **fake_customer_support** | 0 | 0 | 90 | 0 | 0 | 0 | 0 | 0 |
| **fake_govt_scheme** | 0 | 0 | 0 | 90 | 0 | 0 | 0 | 0 |
| **fake_upi_refund_cashback** | 0 | 0 | 0 | 0 | 90 | 0 | 0 | 0 |
| **legitimate** | 0 | 0 | 0 | 0 | 0 | 90 | 0 | 0 |
| **lottery_prize** | 0 | 0 | 0 | 0 | 0 | 0 | 90 | 0 |
| **otp_pin_theft** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 90 |

## 4. Hard Negatives & Safety Guardrails
The dataset explicitly incorporates hard negative samples to prevent false positives on genuine banking communications:
- Bank transaction SMS with "Do not share OTP" notices.
- Login two-factor authentication alerts.
- Legitimate utility bills with standard payment deadlines.
- Real e-commerce package tracking alerts.

Combined with our **Deterministic Rule Safety Layer**, any message that instructs a user to "enter UPI PIN to receive money" or share CVV/OTP triggers an immediate high-severity safety flag regardless of ML model confidence.
