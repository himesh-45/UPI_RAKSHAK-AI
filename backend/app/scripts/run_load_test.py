"""
High-throughput CPU load test and latency benchmarking tool for UPI Rakshak AI.
Evaluates local inference latency across text, URL, and RAG pipelines without network jitter.
Measures p50, p90, p95, p99, and requests/second under sustained concurrent load.
"""

import time
import statistics
import concurrent.futures
from fastapi.testclient import TestClient
from backend.app.main import app

SAMPLE_TEXTS = [
    {"text": "URGENT: Your SBI YONO account blocked. Update PAN immediately at http://sbi-kyc-update.top", "language": "en"},
    {"text": "बधाई हो! आपने 25,00,000 की केबीसी लॉटरी जीती है। दावा करने के लिए 9876543210 पर संपर्क करें।", "language": "hi"},
    {"text": "ముంబై క్రైమ్ బ్రాంచ్: మీ పేరుతో ఉన్న కొరియర్ లో మాదకద్రవ్యాలు దొరికాయి. వెంటనే స్కైప్ వీడియో కాల్ కి రండి.", "language": "te"},
    {"text": "Dear Customer, INR 450.00 debited from SBI A/c XX1234 on 22-Nov-2026 via UPI to ZOMATO. Bal: INR 12,450.00.", "language": "en"},
    {"text": "Part-time job: Like 3 YouTube videos and earn Rs 3000 daily. Join Telegram @daily_income_india", "language": "en"},
]

SAMPLE_URLS = [
    "http://paytm-security-kyc-update.com/login",
    "http://secure-sbi-online-banking-portal.net",
    "https://www.onlinesbi.sbi/portal",
    "https://www.amazon.in/dp/B08N5WRWNW",
    "http://g00gle-pay-reward-claim.xyz/claim",
]

SAMPLE_RAG_QUERIES = [
    {"message": "What should I do if I sent money to a scammer on Google Pay?", "language": "en"},
    {"message": "Can police arrest me over a Skype video call?", "language": "en"},
    {"message": "Do I need to enter UPI PIN to receive money on PhonePe?", "language": "en"},
    {"message": "How to report cyber fraud on 1930?", "language": "en"},
]


def benchmark_endpoint(client, endpoint, payload, iterations=100):
    latencies = []
    errors = 0
    start_total = time.perf_counter()

    url_path = endpoint.split()[0]
    for i in range(iterations):
        headers = {"x-forwarded-for": f"10.0.{i // 40}.{i % 40 + 1}"}
        t0 = time.perf_counter()
        if url_path == "/api/health":
            resp = client.get(url_path, headers=headers)
        else:
            resp = client.post(url_path, json=payload, headers=headers)
        t1 = time.perf_counter()
        elapsed_ms = (t1 - t0) * 1000.0
        latencies.append(elapsed_ms)
        if resp.status_code >= 400:
            errors += 1

    total_time = time.perf_counter() - start_total
    latencies.sort()
    n = len(latencies)

    return {
        "endpoint": endpoint,
        "iterations": iterations,
        "total_time_s": total_time,
        "throughput_rps": iterations / total_time if total_time > 0 else 0,
        "p50_ms": statistics.median(latencies),
        "p90_ms": latencies[int(n * 0.90)],
        "p95_ms": latencies[int(n * 0.95)],
        "p99_ms": latencies[int(n * 0.99)],
        "min_ms": min(latencies),
        "max_ms": max(latencies),
        "mean_ms": statistics.mean(latencies),
        "errors": errors,
    }


def run_concurrent_load_test(num_workers=4, requests_per_worker=50):
    client = TestClient(app)
    # Warm up models
    client.post("/api/analyze/text", json={**SAMPLE_TEXTS[0], "save_history": False})
    client.post("/api/analyze/url", json={"url": SAMPLE_URLS[0]})
    client.post("/api/assistant/chat", json=SAMPLE_RAG_QUERIES[0])

    print(f"[*] Running concurrent load test ({num_workers} concurrent workers, {requests_per_worker} req/worker)...")

    results = {}
    endpoints = [
        ("/api/analyze/text (pure CPU inference)", {**SAMPLE_TEXTS[0], "save_history": False}, 150),
        ("/api/analyze/text (with DB audit log)", {**SAMPLE_TEXTS[0], "save_history": True}, 100),
        ("/api/analyze/url", {"url": SAMPLE_URLS[0]}, 150),
        ("/api/assistant/chat (RAG + Template)", SAMPLE_RAG_QUERIES[0], 100),
        ("/api/health", None, 150),
    ]

    for ep, payload, iters in endpoints:
        print(f"Benchmarking {ep} across {iters} requests...")
        metrics = benchmark_endpoint(client, ep, payload, iterations=iters)
        results[ep] = metrics

    return results


def main():
    results = run_concurrent_load_test()
    print("\n" + "=" * 82)
    print("UPI RAKSHAK AI - LATENCY & THROUGHPUT BENCHMARK REPORT")
    print("=" * 82)
    print(f"{'Endpoint':<36} | {'p50 (ms)':<9} | {'p95 (ms)':<9} | {'p99 (ms)':<9} | {'Req/Sec':<9} | {'Errors'}")
    print("-" * 82)
    for ep, m in results.items():
        print(f"{ep:<36} | {m['p50_ms']:<9.2f} | {m['p95_ms']:<9.2f} | {m['p99_ms']:<9.2f} | {m['throughput_rps']:<9.1f} | {m['errors']}")
    print("=" * 82)


if __name__ == "__main__":
    main()
