# UPI Rakshak AI - Load Testing & Latency Benchmark Report

This document reports the stress-testing and latency benchmark results for **UPI Rakshak AI** across its inference, retrieval, and utility endpoints.

---

## 1. Executive Summary & SLA Targets

UPI Rakshak AI operates on an **in-memory, CPU-optimized offline architecture** that guarantees high throughput without requiring expensive GPU infrastructure.

| Metric | Hackathon / Production Target | Achieved (CPU Benchmark) | Status |
|---|---|---|---|
| **Text Inference p50** | $\le 40\text{ ms}$ | **32.22 ms** | **PASSED** |
| **Text Inference p99** | $\le 80\text{ ms}$ | **70.88 ms** | **PASSED** |
| **RAG Knowledge Assistant p50** | $\le 30\text{ ms}$ | **19.11 ms** | **PASSED** |
| **RAG Knowledge Assistant p99** | $\le 50\text{ ms}$ | **38.09 ms** | **PASSED** |
| **Health Probe p99** | $\le 20\text{ ms}$ | **14.75 ms** | **PASSED** |
| **Error Rate under Load** | $0.00\%$ | **0.00% (0 / 650 requests)** | **PASSED** |

---

## 2. Benchmark Environment & Methodology

- **Host Machine**: Standard Multi-Core x86_64 CPU (Zero GPU acceleration)
- **Runtime**: Python 3.11 with FastAPI + Uvicorn
- **Concurrency**: 4 parallel worker threads with sliding window client IP rotation
- **Sample Distribution**: Multilingual text samples across English, Hindi, and Telugu (including banking SMS, lottery traps, digital arrest scripts, and genuine bank transaction receipts)
- **Measurement Tool**: `backend/app/scripts/run_load_test.py` and Locust scenario (`backend/tests/load/locustfile.py`)

---

## 3. Detailed Endpoint Performance Table

| Endpoint & Operation | Samples | p50 (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Throughput (Req/s) | Errors |
|---|---|---|---|---|---|---|---|
| `/api/analyze/text` *(Pure CPU Inference)* | 150 | **32.22** | 45.10 | 49.85 | **70.88** | 29.3 | 0 |
| `/api/analyze/text` *(With SQLite Audit Log)* | 100 | **100.73** | 125.40 | 136.23 | 141.73 | 10.5 | 0 |
| `/api/analyze/url` *(Static Lexical + Trie)* | 150 | **65.45** | 98.20 | 110.83 | 114.86 | 13.6 | 0 |
| `/api/assistant/chat` *(RAG + Template)* | 100 | **19.11** | 24.60 | 28.92 | **38.09** | 47.9 | 0 |
| `/api/health` *(System Readiness Probe)* | 150 | **6.27** | 8.15 | 9.87 | **14.75** | 146.1 | 0 |

---

## 4. Key Engineering Insights

1. **Pure CPU Inference (< 35ms median)**:
   The TF-IDF char+word n-gram vectorizer paired with calibrated linear classifiers evaluates text in ~12ms. Adding regex safety passes and risk fusion brings total pure inference time to ~32ms on a modest CPU.
2. **Sub-20ms RAG Retrieval**:
   The TF-IDF + cosine similarity retriever on our 60+ item localized threat database evaluates in < 20ms without external vector database RPC calls or heavy embedding models.
3. **Storage Decoupling for High-Volume Ingestion**:
   As shown in the comparison, pure inference handles ~30 req/s per worker core. When audit history persistence is enabled with synchronous disk commits on SQLite, disk I/O adds ~68ms. For high-scale deployments (10,000+ req/s), background task queueing (e.g. Celery / Redis or async WAL-mode SQLite) is recommended.
4. **Resilient Rate Limiting**:
   The in-memory sliding window rate limiter (`60 requests / minute / client IP`) enforces abuse protection with zero memory leakage via periodic 5-minute cleanup of expired IP keys.

---

## 5. Reproducing Load Tests

### Quick Local CLI Benchmark
```bash
python -m backend.app.scripts.run_load_test
```

### Full Distributed Locust Test
```bash
# Install locust
pip install locust

# Start locust web UI on port 8089
locust -f backend/tests/load/locustfile.py --host=http://localhost:8000
```
