# UPI Rakshak AI — NLP Model Report & Evaluation History

> [!IMPORTANT]
> **Superseded by Leakage-Free Gold Benchmark**:
> This document is retained for historical auditability and model provenance tracking.
> An early prototype version evaluated a naive random stratified split of synthetic templates, yielding an artificial 100.00% accuracy due to identical template sentence skeletons appearing in both train and test splits (template memorization).
>
> That evaluation has been completely replaced with an honest, leakage-free benchmark on an independent, hand-crafted **Gold Test Set** evaluated via `backend.app.scripts.evaluate_models`.
>
> **For current, verified benchmark metrics, see: [EVALUATION_REPORT.md](EVALUATION_REPORT.md)**.

---

## 1. Provenance & Evolution History

| Milestone | Architecture | Evaluation Methodology | Resulting Metric | Status |
| :--- | :--- | :--- | :--- | :--- |
| **v1.0 (Prototype)** | 8-Class TF-IDF + Logistic Regression | Random stratified 80/20 train/test split on synthetic templates | 100.00% Accuracy (Defective: template memorization) | **DEPRECATED** |
| **v2.0 (Phase 1 Audit)** | 15-Class Calibrated TF-IDF + Linear Classifier | GroupShuffleSplit by template family + Gold Test Set v1 (306 samples) | 78.52% Macro-F1, 95.41% Scam Recall, 2.73% Legit FPR | **ACTIVE** |
| **v2.1 (Current Release)** | Hierarchical Dual-Stage / Stacked Ensemble + Calibrated Probabilities | GroupShuffleSplit + Expanded Gold Test Set v2 (messy human phrasings) | Programmatically verified via `evaluate_models.py` | **CURRENT** |

---

## 2. Why the 100% Metric Was Invalid

1. **Synthetic Template Leakage**: When templates such as *"Dear user, your {bank} account is blocked, update KYC at {url}"* exist in both train and test splits with only slot variables changing, classifiers memorize the template structure rather than learning true semantic indicators of fraud.
2. **Gold Benchmark Protocol**: Current evaluation uses strictly isolated gold evaluation datasets (`gold_v1.json` and `gold_v2.json`) containing human-written, messy phrasings, forwarded WhatsApp style messages, typos, and 100+ hard negatives that are never trained or tuned on.

Please refer to [EVALUATION_REPORT.md](EVALUATION_REPORT.md) for full programmatic metrics, confusion matrices, and bootstrap confidence intervals.
