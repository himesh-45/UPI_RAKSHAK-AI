"""
Locust load testing scenario for UPI Rakshak AI.
Simulates concurrent consumer, bot, and enterprise traffic across text, URL, and RAG endpoints.
Usage:
    locust -f backend/tests/load/locustfile.py --host=http://localhost:8000
"""

import random
from locust import HttpUser, task, between

SAMPLE_TEXTS = [
    # Scams
    {"text": "URGENT: Your SBI YONO account blocked. Update PAN immediately at http://sbi-kyc-update.top", "language": "en"},
    {"text": "बधाई हो! आपने 25,00,000 की केबीसी लॉटरी जीती है। दावा करने के लिए 9876543210 पर संपर्क करें।", "language": "hi"},
    {"text": "ముంబై క్రైమ్ బ్రాంచ్: మీ పేరుతో ఉన్న కొరియర్ లో మాదకద్రవ్యాలు దొరికాయి. వెంటనే స్కైప్ వీడియో కాల్ కి రండి.", "language": "te"},
    {"text": "Sir I sent 2000 rs by mistake to your Google Pay number please return it back", "language": "en"},
    {"text": "Part-time job: Like 3 YouTube videos and earn Rs 3000 daily. Join Telegram @daily_income_india", "language": "en"},
    # Legitimate
    {"text": "Dear Customer, INR 450.00 debited from SBI A/c XX1234 on 22-Nov-2026 via UPI to ZOMATO. Bal: INR 12,450.00.", "language": "en"},
    {"text": "प्रिय ग्राहक, आपके खाते से 500 रुपये का यूपीआई भुगतान सफल रहा। शेष राशि 4,200 रुपये है।", "language": "hi"},
    {"text": "ప్రియమైన కస్టమర్, మీ అకౌంట్ నుండి రూ. 350 విజయవంతంగా బదిలీ చేయబడింది. ప్రస్తుత బ్యాలెన్స్ రూ. 8,900.", "language": "te"},
]

SAMPLE_URLS = [
    "http://paytm-security-kyc-update.com/login",
    "http://secure-sbi-online-banking-portal.net",
    "https://www.onlinesbi.sbi/portal",
    "https://www.amazon.in/dp/B08N5WRWNW",
    "http://192.168.1.1/admin/login.php",
    "http://g00gle-pay-reward-claim.xyz/claim",
]

SAMPLE_RAG_QUERIES = [
    "What should I do if I sent money to a scammer on Google Pay?",
    "Can police arrest me over a Skype video call?",
    "Do I need to enter UPI PIN to receive money on PhonePe?",
    "How to report cyber fraud on 1930?",
]


class ScamDetectionUser(HttpUser):
    wait_time = between(0.05, 0.2)  # High throughput simulation

    @task(5)
    def test_analyze_text(self):
        sample = random.choice(SAMPLE_TEXTS)
        self.client.post("/api/analyze/text", json=sample, name="/api/analyze/text")

    @task(3)
    def test_analyze_url(self):
        url = random.choice(SAMPLE_URLS)
        self.client.post("/api/analyze/url", json={"url": url}, name="/api/analyze/url")

    @task(2)
    def test_rag_query(self):
        query = random.choice(SAMPLE_RAG_QUERIES)
        self.client.post("/api/rag/query", json={"query": query, "top_k": 3}, name="/api/rag/query")

    @task(1)
    def test_health(self):
        self.client.get("/api/health", name="/api/health")
