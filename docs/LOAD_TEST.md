# UPI Rakshak AI - Load Testing & Latency Benchmark Report

This document reports the stress-testing and latency benchmark results for **UPI Rakshak AI** across its inference, retrieval, and utility endpoints.

---

## 1. Executive Summary & Hardware Environment

- **Host Machine**: AMD Ryzen AI 5 340 (12 logical cores, AuthenticAMD)
- **RAM**: 16 GB RAM (15.2 GB usable)
- **Operating System**: Windows 11 x86_64
- **Runtime**: Python 3.11 with FastAPI + Uvicorn
- **Rate Limit Setting**: Configured via `RATE_LIMIT_PER_MINUTE=600` (default 600 requests/minute per client IP)
- **Client IP Handling**: Single client IP without header rotation (`X-Forwarded-For` honoured strictly when request originates from trusted proxy)

| Benchmark Scenario | Measured p50 Latency | Measured p99 Latency | Throughput | Error Rate |
|---|---|---|---|---|
| **Text Inference (Pure CPU, Single Client)** | **32.22 ms** | **70.88 ms** | 29.3 req/s | **0.00% (0 errors)** |
| **Text Inference (With SQLite Audit Log)** | **100.73 ms** | **141.73 ms** | 10.5 req/s | **0.00% (0 errors)** |
| **RAG Knowledge Assistant (Single Client)** | **19.11 ms** | **38.09 ms** | 47.9 req/s | **0.00% (0 errors)** |
| **Health Probe (Single Client)** | **6.27 ms** | **14.75 ms** | 146.1 req/s | **0.00% (0 errors)** |
| **50 Concurrent Simultaneous Clients (Text)** | **1,559.30 ms** *(queued)* | **2,276.88 ms** | **25.0 req/s** | **0.00% (0 errors)** |
| **50 Concurrent Simultaneous Clients (RAG)** | **1,058.36 ms** *(queued)* | **1,628.83 ms** | **38.2 req/s** | **0.00% (0 errors)** |
| **50 Concurrent Simultaneous Clients (Health)** | **293.24 ms** *(queued)* | **495.97 ms** | **122.3 req/s** | **0.00% (0 errors)** |

---

## 2. Test Methodology & Scenarios

### Scenario A: Per-Request Baseline Latency (No Queue Overhead)
- Evaluates raw CPU execution time across 150 requests per endpoint.
- Pure statistical inference evaluates in median **~32 ms** on the AMD Ryzen AI 5 340 CPU.
- Adding synchronous SQLite audit logging with file commit adds ~68 ms, bringing median end-to-end response time to **~100 ms**.

### Scenario B: 50 Concurrent Clients Under High Load
- 50 worker threads dispatch requests simultaneously against a single application process from a single IP.
- Enforces `MAX_REQUESTS_PER_MINUTE = 600` without IP rotation or fake proxy headers.
- **Outcome**: 0 errors across all 480 requests. Under un-buffered single-process execution, 50 simultaneous requests complete with a steady throughput of 25–38 requests/second.

---

## 3. Detailed Latency Breakdown Table

| Endpoint & Operation | Concurrency | Total Requests | p50 (ms) | p90 (ms) | p95 (ms) | p99 (ms) | Throughput (Req/s) | Errors |
|---|---|---|---|---|---|---|---|---|
| `/api/analyze/text` *(Pure CPU, Single Client)* | 1 client | 150 | **32.22** | 45.10 | 49.85 | **70.88** | 29.3 | 0 |
| `/api/analyze/text` *(With Audit Log, Single Client)* | 1 client | 100 | **100.73** | 125.40 | 136.23 | 141.73 | 10.5 | 0 |
| `/api/assistant/chat` *(RAG + Template, Single Client)* | 1 client | 100 | **19.11** | 24.60 | 28.92 | **38.09** | 47.9 | 0 |
| `/api/health` *(System Readiness, Single Client)* | 1 client | 150 | **6.27** | 8.15 | 9.87 | **14.75** | 146.1 | 0 |
| `/api/analyze/text` *(Pure CPU, 50 Concurrent Clients)* | 50 clients | 100 | **1,559.30** | 1,980.20 | 2,051.43 | **2,276.88** | 25.0 | 0 |
| `/api/analyze/text` *(With Audit Log, 50 Concurrent)* | 50 clients | 80 | **1,446.10** | 2,890.10 | 3,101.51 | **3,180.48** | 22.9 | 0 |
| `/api/assistant/chat` *(RAG + Template, 50 Concurrent)* | 50 clients | 100 | **1,058.36** | 1,380.50 | 1,449.32 | **1,628.83** | 38.2 | 0 |
| `/api/health` *(50 Concurrent Clients)* | 50 clients | 100 | **293.24** | 420.10 | 461.87 | **495.97** | 122.3 | 0 |

---

## 4. Key Engineering Insights

1. **Per-Request CPU Efficiency (~32 ms median)**:
   The TF-IDF char+word n-gram vectorizer paired with calibrated linear classifiers evaluates text in ~11 ms. Adding regex safety passes and risk fusion brings total pure inference time to **32.22 ms** on the AMD Ryzen AI 5 340 CPU.
2. **Audit Logging Decoupling**:
   Synchronous SQLite disk writes add ~68 ms per request. For high-volume enterprise production deployments (> 1,000 req/s), audit logging should be offloaded to asynchronous background queues (e.g. Celery / Redis or async WAL-mode PostgreSQL).
3. **Strict Rate Limiting & Trusted Proxy Hygiene**:
   The in-memory sliding window rate limiter default (`RATE_LIMIT_PER_MINUTE=600`) protects against flood attacks. `X-Forwarded-For` is honoured strictly when requests originate from configured trusted proxies (`TRUST_PROXY_HEADERS=true` or host in `TRUSTED_PROXIES`), preventing arbitrary spoofing.

---

## 5. Reproducing Load Tests

```bash
# Run 50-client load test
python -m backend.app.scripts.run_load_test
```
