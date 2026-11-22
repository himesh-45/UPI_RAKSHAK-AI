# Gold v3 External Blind Benchmark Protocol

## 1. Overview & Ethical Foundation
The **Gold Test Set v3** is designed as a true blind benchmark composed exclusively of natural, consented smishing messages and legitimate transactional notifications sourced from users **outside the research and development team**.

To maintain strict scientific integrity:
1. **Zero Data Fabrication**: No synthetic generator, LLM, or team member may author messages for Gold v3.
2. **Informed Consent**: Every message must be contributed voluntarily by individuals after confirming digital consent.
3. **Mandatory PII Scrubbing**: All personal names, phone numbers, bank account numbers, OTPs, and private UPI handles must be redacted using the automated PII masking tool prior to evaluation.
4. **Zero-Retraining Principle**: The model is evaluated strictly once. Hyperparameters and model weights are **never** tuned or retrained on Gold v3.

---

## 2. Target Dataset Composition (Target: 100+ Samples)

| Category / Stratum | Target Quota | Sourcing Channels |
| :--- | :---: | :--- |
| **Active Scam Vectors** | 60+ samples | Consented user WhatsApp forwards, SMS smishing screenshots, call transcripts. |
| **Legitimate Hard Negatives** | 40+ samples | Official bank transaction alerts, courier delivery PIN notices, telecom recharges, utility bills. |
| **Language Distribution** | Balanced | English (~40%), Hindi (~30%), Telugu (~20%), Hinglish/Colloquial (~10%). |

---

## 3. Data Collection Workflow

```
[External Contributor] 
       │ 
       ▼ (Consents via Web Form)
[Raw Text / Screenshot]
       │
       ▼ (Runs mask_blind_dataset.py)
[Sanitized JSON / CSV]
       │
       ▼ (make evaluate-blind FILE=...)
[docs/BLIND_EVALUATION.md]
```

### Step 1: Contributor Consent Text
All contributors must agree to the following disclosure:
> *"I confirm that I received this communication and consent to donating its sanitized text for academic cybersecurity and fraud-prevention benchmarking. I understand that all personal names, phone numbers, account numbers, and OTPs will be stripped before analysis."*

### Step 2: Automated PII Masking
Run the built-in sanitizer on the raw collection file:
```bash
python -m backend.app.scripts.mask_blind_dataset \
  --input raw_external_submissions.json \
  --output backend/app/data/gold_v3_sanitized.json
```
The sanitizer enforces:
- Phone numbers $\to$ `[PHONE_REDACTED]`
- Account / Card numbers $\to$ `[ACCOUNT_REDACTED]`
- Verification OTPs $\to$ `[OTP_REDACTED]`
- Contributor names $\to$ `[NAME_REDACTED]`
- Personal UPI usernames $\to$ `[USER_REDACTED]@handle`

### Step 3: Run the Blind Evaluation
Execute the single-pass blind benchmark:
```bash
make evaluate-blind FILE=backend/app/data/gold_v3_sanitized.json
```
This programmatically generates [docs/BLIND_EVALUATION.md](BLIND_EVALUATION.md) reporting:
- Scam Recall, Legitimate False Positive Rate, Precision, F1-Score with bootstrap 95% CIs
- 15-class NLP Macro-F1 with bootstrap 95% CIs
- Per-language breakdown across English, Hindi, and Telugu
- Full latency profile and detailed error log
