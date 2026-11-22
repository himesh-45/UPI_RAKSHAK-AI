"""
High-throughput CPU load test and latency benchmarking tool for UPI Rakshak AI.
Evaluates local inference latency across text, URL, and RAG pipelines without IP rotation.
Measures p50, p90, p95, p99, and requests/second under sustained 50 concurrent clients.
"""

import time
import statistics
import concurrent.futures
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.security import RATE_LIMIT_STORE

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

HARDWARE_INFO = {
    "cpu": "AMD Ryzen AI 5 340 (12 logical cores, AuthenticAMD)",
    "ram": "16 GB RAM (15.2 GB usable)",
    "os": "Windows 11 x86_64",
    "concurrency": 50,
    "ip_rotation": "Disabled (single client IP, 600 req/min rate limit)"
}


def make_single_request(client, url_path, payload):
    t0 = time.perf_counter()
    if url_path == "/api/health":
        resp = client.get(url_path)
    else:
        resp = client.post(url_path, json=payload)
    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000.0
    return elapsed_ms, resp.status_code


def benchmark_endpoint_concurrent(client, endpoint, payload, total_requests=100, num_clients=50):
    url_path = endpoint.split()[0]
    RATE_LIMIT_STORE.clear()  # Fresh rate limit window per endpoint benchmark

    latencies = []
    errors = 0
    start_total = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_clients) as executor:
        futures = [executor.submit(make_single_request, client, url_path, payload) for _ in range(total_requests)]
        for fut in concurrent.futures.as_completed(futures):
            elapsed_ms, status_code = fut.result()
            latencies.append(elapsed_ms)
            if status_code >= 400:
                errors += 1

    total_time = time.perf_counter() - start_total
    latencies.sort()
    n = len(latencies)

    return {
        "endpoint": endpoint,
        "iterations": total_requests,
        "clients": num_clients,
        "total_time_s": total_time,
        "throughput_rps": total_requests / total_time if total_time > 0 else 0,
        "p50_ms": statistics.median(latencies),
        "p90_ms": latencies[int(n * 0.90)],
        "p95_ms": latencies[int(n * 0.95)],
        "p99_ms": latencies[int(n * 0.99)],
        "min_ms": min(latencies),
        "max_ms": max(latencies),
        "mean_ms": statistics.mean(latencies),
        "errors": errors,
    }


def run_concurrent_load_test(num_clients=50, requests_per_endpoint=100):
    client = TestClient(app)
    # Warm up models
    client.post("/api/analyze/text", json={**SAMPLE_TEXTS[0], "save_history": False})
    client.post("/api/analyze/url", json={"url": SAMPLE_URLS[0]})
    client.post("/api/assistant/chat", json=SAMPLE_RAG_QUERIES[0])

    print("=" * 82)
    print("UPI RAKSHAK AI — LOAD TEST BENCHMARK (50 CONCURRENT CLIENTS)")
    print("=" * 82)
    print(f"Hardware:    CPU: {HARDWARE_INFO['cpu']}")
    print(f"Memory:      RAM: {HARDWARE_INFO['ram']}")
    print(f"Concurrency: {num_clients} concurrent clients (Single IP, No Header Spoofing)")
    print(f"Rate Limit:  600 requests/minute (Default environment config)")
    print("=" * 82)

    results = {}
    endpoints = [
        ("/api/analyze/text (pure CPU inference)", {**SAMPLE_TEXTS[0], "save_history": False}, 100),
        ("/api/analyze/text (with DB audit log)", {**SAMPLE_TEXTS[0], "save_history": True}, 80),
        ("/api/analyze/url", {"url": SAMPLE_URLS[0]}, 100),
        ("/api/assistant/chat (RAG + Template)", SAMPLE_RAG_QUERIES[0], 100),
        ("/api/health", None, 100),
    ]

    for ep, payload, iters in endpoints:
        print(f"Benchmarking {ep} across {iters} requests with {num_clients} clients...")
        metrics = benchmark_endpoint_concurrent(client, ep, payload, total_requests=iters, num_clients=num_clients)
        results[ep] = metrics

    return results


def main():
    results = run_concurrent_load_test(num_clients=50, requests_per_endpoint=100)
    print("\n" + "=" * 82)
    print("UPI RAKSHAK AI — LATENCY & THROUGHPUT BENCHMARK RESULTS")
    print("=" * 82)
    print(f"{'Endpoint':<36} | {'p50 (ms)':<9} | {'p95 (ms)':<9} | {'p99 (ms)':<9} | {'Req/Sec':<9} | {'Errors'}")
    print("-" * 82)
    for ep, m in results.items():
        print(f"{ep:<36} | {m['p50_ms']:<9.2f} | {m['p95_ms']:<9.2f} | {m['p99_ms']:<9.2f} | {m['throughput_rps']:<9.1f} | {m['errors']}")
    print("=" * 82)


if __name__ == "__main__":
    main()
