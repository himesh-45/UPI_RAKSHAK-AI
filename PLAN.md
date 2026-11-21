# UPI Rakshak AI — Development Plan & Architecture

## System Architecture

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

## Folder Structure
- `backend/`
  - `app/`
    - `main.py`: FastAPI application setup, CORS, error handling, rate limiting.
    - `config.py`: Environment configuration, risk thresholds, feature flags.
    - `database.py`: SQLite engine & session management.
    - `models/`: Database models (analyses, threat reports, admin user) and Pydantic schemas.
    - `core/`: Sensitive data masking, password hashing, JWT tokens, sanitization.
    - `detectors/`: NLP classifier, rule-based safety layer, static URL scanner, QR decoder & UPI pay parser, OCR pipeline.
    - `fusion/`: Risk fusion engine combining signals into 0–100 score and verdict.
    - `rag/`: Verified safety knowledge base JSON and offline TF-IDF/cosine retriever.
    - `assistant/`: Multilingual template-based generator (en/hi/te) and pluggable LLM fallback.
    - `routes/`: Endpoints for analyze (text, url, image), assistant, reports, dashboard, history, auth.
    - `scripts/`: Synthetic dataset generation (3,000+ samples), model training, demo asset generation, database seeding.
  - `tests/`: 40+ unit and integration tests covering all detectors, fusion, API routes, masking, and RAG.
  - `requirements.txt`: Python package dependencies.
- `frontend/`
  - `src/`: React 18, Vite, Tailwind CSS, Lucide icons, Recharts, i18n dictionary.
  - `public/`: Demo sample assets (QR codes, screenshots).
- `docs/`
  - `MODEL_REPORT.md`: Training metrics, class breakdown, synthetic data notice, confusion matrix.
  - `DEMO_SCRIPT.md`: Step-by-step 3-minute demo script for evaluators.
- `docker-compose.yml`, `Dockerfile`s, `run.sh`, `run.bat`, `README.md`, `DECISIONS.md`.

## Milestones & Phased Execution
1. **Phase 0 – Plan**: Write PLAN.md and DECISIONS.md.
2. **Phase 1 – Scaffold**: Setup virtual environment, backend skeleton, frontend skeleton, end-to-end health check.
3. **Phase 2 – Dataset & NLP**: Multilingual synthetic dataset (3,000+ items across 8 classes and 3 languages), train TF-IDF model, implement rule-based safety layer, write test suite.
4. **Phase 3 – URL Scanner**: Static URL scanner, Indian bank/UPI brand list, Levenshtein edit distance, shortener & homoglyph checks, unit tests.
5. **Phase 4 – OCR & QR Module**: Image preprocessing, QR code decoding (`upi://pay` parameter validation: pa, pn, am, cu, tn), OCR text extraction with fallbacks, test suite.
6. **Phase 5 – RAG Knowledge Base**: Curate factual verified safety knowledge base (UPI architecture, PIN-less receiving, reporting to 1930/cybercrime.gov.in), offline retriever, test suite.
7. **Phase 6 – Risk Fusion Engine**: Signal fusion, hard overrides (e.g. OTP + urgency => HIGH RISK), verdict thresholds, report formatting with disclaimer, test suite.
8. **Phase 7 – Multilingual Assistant & Voice**: Chat assistant with en/hi/te support, deterministic templates + optional LLM hook, Web Speech API integration in UI.
9. **Phase 8 – Dashboard & Auth**: Admin JWT auth, historical audit logging with PII masking, threat reporting endpoint, simulated + live data separation in analytics.
10. **Phase 9 – UI Polish**: Responsive modern theme, sample chips, color-coded score gauge, dark/light mode toggle, accessibility & privacy notices.
11. **Phase 10 – Packaging & Verification**: Dockerfile, docker-compose, run scripts, comprehensive test execution (40+ passing tests), MODEL_REPORT.md, DEMO_SCRIPT.md, end-to-end walkthrough verification.
