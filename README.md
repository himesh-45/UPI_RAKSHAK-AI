# 🛡️ UPI Rakshak AI (यूपीआई रक्षक / యూపీఐ రక్షక్)

> **Real-Time, Multilingual (English, Hindi, Telugu), Evidence-Based Digital Payment Scam Detection & Prevention Platform.**
>
> ⚡ **Offline-First**: Fully functional without internet or API keys. Zero external dependency.
> ⚖️ **Evidence-Based**: Final verdict stems from independent detectors mathematically fused together, NOT by asking an LLM "is this a scam?".

---

## 📌 Key Highlights

- **Multi-Layer Intelligence Engine**: Integrates 6 independent detectors (Multilingual NLP, Deterministic Rule Layer, Static URL Scanner, OpenCV QR & UPI pay parser, OCR pipeline, and RAG Knowledge Engine).
- **Trilingual Native Support**: Full UI and AI Assistant in **English**, **Hindi (हिंदी)**, and **Telugu (తెలుగు)** with native script, Hinglish, and Romanized Telugu handling.
- **Voice-Enabled Assistant**: Web Speech API integration with language selector (`en-IN`, `hi-IN`, `te-IN`).
- **Privacy by Design**: Sensitive PII (10-digit mobile numbers, account numbers, card digits, OTPs) is automatically masked before persistence.
- **Safety Guarantee**: Suspicious URLs and QR payloads are NEVER fetched, opened, or executed.
- **50+ Automated Tests**: Comprehensive unit and integration test suite passing out of the box.

---

## 🏛️ Architecture Overview

```
                                  [ User Input ]
                   (Text / Suspicious URL / Screenshot / QR Code)
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
    [ NLP Classifier & ]       [ Static URL Scanner ]    [ Screenshot & QR Module ]
    [ Rule Safety Layer]       (Edit-dist, shorteners,   (OCR en/hi/te, UPI URI
    (TF-IDF + LinearModel,      Punycode, TLDs, brands)   pa/pn/am/tn param parser)
     OTP/Collect/Urgency rules)         │                          │
             │                          │                          │
             └──────────────────────────┼──────────────────────────┘
                                        ▼
                           [ Risk Fusion Engine ]
                (Weighted multi-signal aggregation 0-100,
                 hard-override safety rules, verdict assignment)
                                        │
                                        ▼
                     [ RAG Knowledge Retrieval Engine ]
                  (Verified offline safety playbooks, 1930
                   helpline citations, actionable do's/don'ts)
                                        │
             ┌──────────────────────────┴──────────────────────────┐
             ▼                                                     ▼
     [ Safety Report API ]                               [ Multilingual Assistant ]
   (Verdict, Score 0-100,                              (Chat, Voice Web Speech API,
    Ranked Evidence, Actions,                           English / Hindi / Telugu,
    Masked Audit Log)                                   Deterministic / LLM fallback)
             │                                                     │
             └──────────────────────────┬──────────────────────────┘
                                        ▼
                           [ Responsive Frontend UI ]
                  (React + Vite + Tailwind CSS + Recharts)
                  (Analyzer, Chat, Admin Intel Dashboard, About)
```

---

## 🚀 Quickstart

### Option 1: Docker Compose (Recommended)

```bash
docker compose up --build
```

- **Frontend Web UI**: [http://localhost:3000](http://localhost:3000)
- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Admin Login**: `admin@upirakshak.ai` / `AdminRakshak#2026`

---

### Option 2: Local One-Command Run

#### Linux / macOS
```bash
chmod +x run.sh
./run.sh
```

#### Windows
```cmd
run.bat
```

- **Frontend Web UI**: [http://localhost:5173](http://localhost:5173)
- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option 3: Manual Step-by-Step Setup

#### 1. Backend Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install requirements
pip install -r backend/requirements.txt

# Seed dataset, ML model, and simulated demo records
python -m backend.app.scripts.generate_dataset
python -m backend.app.scripts.train_model
python -m backend.app.scripts.generate_demo_assets
python -m backend.app.scripts.seed_db

# Start backend server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Automated Testing

Run the full automated test suite (53 tests covering all detectors, fusion engine, RAG, masking, assistant, and REST API):

```bash
# Run pytest with virtual environment
python -m pytest backend/tests -v
```

### Test Suite Structure
| Test File | Modules Tested | Passing Tests |
|---|---|---|
| `backend/tests/test_nlp_rules.py` | Language detection, Multiclass NLP, Safety Rules | 8 tests |
| `backend/tests/test_url_scanner.py` | Static URL analyzer, brand typosquatting, IDN, shorteners | 10 tests |
| `backend/tests/test_qr_ocr.py` | OpenCV QR decoder, `upi://pay` parser, OCR pipeline | 5 tests |
| `backend/tests/test_rag.py` | Factual RAG retriever, cosine similarity, citations | 4 tests |
| `backend/tests/test_fusion.py` | Multi-signal fusion, hard overrides, verdict calibration | 6 tests |
| `backend/tests/test_assistant.py` | Multilingual assistant, grounded explanations | 4 tests |
| `backend/tests/test_masking.py` | PII regex masking (phone, cards, accounts, OTP) | 4 tests |
| `backend/tests/test_health.py` | FastAPI health check endpoint | 1 test |
| `backend/tests/test_api.py` | End-to-end REST API integration, JWT authentication | 11 tests |
| **Total** | | **53 tests (100% passing)** |

---

## 📋 REST API Endpoints

Interactive OpenAPI documentation is available at `http://localhost:8000/docs`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status and offline capability flag |
| `POST` | `/api/analyze/text` | Full multi-signal analysis of SMS/messages |
| `POST` | `/api/analyze/url` | Static analysis of suspicious links (never executed) |
| `POST` | `/api/analyze/image` | OCR and QR `upi://pay` parameter anomaly detection |
| `POST` | `/api/assistant/chat` | Multilingual safety assistant dialogue |
| `POST` | `/api/report` | User-submitted threat incident recording |
| `GET` | `/api/dashboard/stats` | Aggregated threat intelligence metrics & charts |
| `GET` | `/api/history` | Audit log with masked PII and simulation filter |
| `POST` | `/api/auth/login` | Secure JWT admin authentication |

---

## 🔍 The 8 Detected Scam Categories

1. **Fake Bank KYC Phishing**: Coercive warnings threatening account suspension within hours.
2. **Electricity Disconnection Scam**: False power cut threats directing users to call personal mobile numbers.
3. **Fake UPI Refund & Cashback**: Collect request tricks falsely claiming to credit money into the account.
4. **Lottery & Advance-Fee Fraud**: KBC/Lucky draw prize notifications demanding registration charges.
5. **Fake Customer Support & Remote Access**: Instructions to install AnyDesk or TeamViewer to steal screen credentials.
6. **OTP & UPI PIN Theft**: Direct attempts to solicit two-factor authentication secrets or card CVVs.
7. **Fake Government Subsidy Schemes**: Unauthorized portals offering PM Yojana funds upon fee payment.
8. **Legitimate Notifications**: Genuine bank transaction debits, utility reminders, and official login alerts with negative advisory safety warnings (*"NEVER share OTP"*).

---

## 🛡️ Safety & Ethical Commitments

1. **No External Link Execution**: All submitted URLs and QR codes are analyzed statically via string parsing, brand edit distance, and entropy heuristics. We never ping, resolve, or execute target links.
2. **PII Masking**: All 10-digit phone numbers, credit card numbers, account numbers, and OTPs are stripped before storage into the database.
3. **Transparent Heuristic Score**: Every safety report explicitly states that the score is a heuristic risk indicator, NOT a statistical certainty. A `SAFE` verdict denotes that "no strong scam patterns were found".
4. **Helpline Integration**: Prominent guidance directs compromised users to dial national helpline **1930** and visit **cybercrime.gov.in**.

---

## 📚 Documentation Links

- [Evaluator 3-Minute Walkthrough Script](docs/DEMO_SCRIPT.md)
- [NLP Model Training & Evaluation Report](docs/MODEL_REPORT.md)
- [Engineering Architectural Decisions (DECISIONS.md)](DECISIONS.md)
- [Development Plan & Milestones (PLAN.md)](PLAN.md)
