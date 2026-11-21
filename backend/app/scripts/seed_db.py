import os
import json
import random
import secrets
import datetime
from sqlalchemy.orm import Session
from ..database import SessionLocal, Base, engine
from ..models.db_models import User, AnalysisHistory, ThreatReport
from ..core.auth import get_password_hash
from ..config import settings

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Seed or Update Admin User
        admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                email=settings.ADMIN_EMAIL,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD)
            )
            db.add(admin)
            db.commit()
            print(f"Admin user registered: {settings.ADMIN_EMAIL}")
        else:
            admin.hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
            db.commit()

        # Check existing simulated records
        existing_sim = db.query(AnalysisHistory).filter(AnalysisHistory.is_simulated == True).count()
        if existing_sim > 0:
            print(f"Database already contains {existing_sim} simulated records. Skipping seed.")
            return

        print("Seeding simulated demo data into SQLite...")

        CATEGORIES_SAMPLE = [
            ("fake_bank_kyc", "HIGH RISK", (75, 95), "Dear customer, your SBI a/c will be BLOCKED tonight due to pending KYC. Click http://sbi-kyc-verify.top", "en"),
            ("fake_bank_kyc", "HIGH RISK", (78, 92), "ప్రియమైన కస్టమర్, మీ HDFC బ్యాంక్ ఖాతా కేవైసీ నిలిపివేయబడింది. నవీకరించండి http://hdfc-kyc.top", "te"),
            ("electricity_disconnection", "HIGH RISK", (75, 90), "बिजली विभाग: आज रात 9:30 बजे बिजली काट दी जाएगी। तुरंत संपर्क करें: +91-98765-XXXXX", "hi"),
            ("electricity_disconnection", "HIGH RISK", (70, 88), "BESCOM Consumer Alert: Electricity power disconnected tonight at 9:30 PM due to unpaid bill. Pay at http://bescom-pay.site", "en"),
            ("fake_upi_refund_cashback", "HIGH RISK", (80, 98), "Congratulations! Received cashback refund of Rs. 3,500. Enter UPI PIN to claim into account.", "en"),
            ("fake_upi_refund_cashback", "HIGH RISK", (82, 95), "PhonePe రివార్డ్: రూ. 2,999 క్యాష్‌బ్యాక్ పొందడానికి కలెక్ట్ రిక్వెస్ట్ అంగీకరించి పిన్ కొట్టండి.", "te"),
            ("lottery_prize", "HIGH RISK", (75, 90), "KBC All India Lucky Draw: Congratulations! Won 25 Lakhs. Contact lottery officer at +91-98765-XXXXX", "en"),
            ("lottery_prize", "HIGH RISK", (72, 85), "बधाई हो! आपके नंबर पर 15 लाख की लॉटरी निकली है। रजिस्ट्रेशन शुल्क जमा करें: http://kbc-draw.xyz", "hi"),
            ("fake_customer_support", "HIGH RISK", (80, 95), "Dear user, for your pending refund, install AnyDesk app and share 9-digit code with support officer.", "en"),
            ("fake_customer_support", "HIGH RISK", (78, 90), "कस्टमर केयर: रिफंड के लिए प्ले स्टोर से TeamViewer डाउनलोड करें और कोड साझा करें।", "hi"),
            ("otp_pin_theft", "HIGH RISK", (85, 100), "Urgent: Card debited for Rs. 49,999. Share OTP received on phone immediately with bank executive to cancel.", "en"),
            ("otp_pin_theft", "HIGH RISK", (85, 98), "లావాదేవీ రద్దు చేయడానికి మీ మొబైల్‌కు వచ్చిన రహస్య OTP ని వెంటనే చెప్పండి.", "te"),
            ("fake_govt_scheme", "HIGH RISK", (70, 85), "Govt scheme: Rs. 6,000 direct benefit transfer approved. Register within 24 hours: http://pm-subsidy.site", "en"),
            ("fake_govt_scheme", "SUSPICIOUS", (45, 65), "पीएम आवास योजना नई लिस्ट जारी। अपना नाम देखने के लिए क्लिक करें: http://yojana-update.online", "hi"),
            ("fake_bank_kyc", "SUSPICIOUS", (40, 60), "Notice: Debit card status update pending. Please review your account settings at official branch.", "en"),
            ("electricity_disconnection", "SUSPICIOUS", (42, 65), "Electricity bill due reminder: Bill overdue for account 492019. Kindly clear payment before cut-off date.", "en"),
            ("legitimate", "SAFE", (0, 15), "HDFC Bank: Rs. 1,450.00 debited from account 4821 for Swiggy. NEVER share your OTP or PIN with anyone.", "en"),
            ("legitimate", "SAFE", (0, 10), "SBI Alert: OTP for login is 482910. Valid for 10 minutes. Do NOT share OTP with anyone including bank staff.", "en"),
            ("legitimate", "SAFE", (0, 20), "Dear Customer, BESCOM electricity bill for a/c 1092837 is Rs. 1,280. Due date is 28-Nov-2026. Pay safely at official office.", "en"),
            ("legitimate", "SAFE", (0, 15), "మీ ఖాతా నుండి రూ. 1,200 UPI ద్వారా చెల్లించబడింది. మీ OTP లేదా PIN ఎవరితోనూ పంచుకోవద్దు.", "te"),
            ("legitimate", "SAFE", (0, 12), "आपके खाते से 1,500 रुपये की राशि काटी गई है। अपना ओटीपी या पिन किसी से साझा न करें।", "hi")
        ]

        now = datetime.datetime.utcnow()

        # Seed 90 analyses spread over past 7 days
        for i in range(90):
            cat, verdict, score_range, sample_text, lang = random.choice(CATEGORIES_SAMPLE)
            score = random.randint(score_range[0], score_range[1])
            input_type = random.choice(["text", "text", "url", "image"])
            days_ago = random.randint(0, 6)
            hours_ago = random.randint(1, 23)
            created_at = now - datetime.timedelta(days=days_ago, hours=hours_ago)

            evidence_items = []
            if verdict == "HIGH RISK":
                evidence_items.append({"signal": "Credential Theft Attempt: Explicit instruction to share credentials or PIN", "source_module": "RULE_SAFETY_LAYER", "weight": 40.0, "severity": "CRITICAL"})
                evidence_items.append({"signal": "Artificial Urgency & Threat: Coercive ultimatum threatening immediate block", "source_module": "RULE_SAFETY_LAYER", "weight": 25.0, "severity": "HIGH"})
                evidence_items.append({"signal": f"NLP Classifier: Categorized as '{cat}' with high confidence", "source_module": "NLP_CLASSIFIER", "weight": 40.0, "severity": "HIGH"})
            elif verdict == "SUSPICIOUS":
                evidence_items.append({"signal": "High-Risk Top-Level Domain in URL (.top/.online)", "source_module": "URL_SCANNER", "weight": 25.0, "severity": "HIGH"})
                evidence_items.append({"signal": "Coercive phrasing regarding account status", "source_module": "RULE_SAFETY_LAYER", "weight": 20.0, "severity": "MEDIUM"})
            else:
                evidence_items.append({"signal": "Verified Official Safety Advisory: Message explicitly warns NEVER to share OTP", "source_module": "RULE_SAFETY_LAYER", "weight": -30.0, "severity": "INFO"})

            actions = [
                "Do NOT share your OTP, UPI PIN, or CVV with anyone.",
                "In case of financial fraud, dial national helpline 1930 immediately."
            ]

            rec = AnalysisHistory(
                input_type=input_type,
                raw_input_masked=sample_text,
                verdict=verdict,
                risk_score=score,
                detected_category=cat,
                language=lang,
                evidence_json=json.dumps(evidence_items),
                actions_json=json.dumps(actions),
                is_simulated=True,  # Clearly marked as simulated
                created_at=created_at
            )
            db.add(rec)

        # Seed 15 Threat Reports
        for j in range(15):
            cat, _, _, sample_text, lang = random.choice(CATEGORIES_SAMPLE)
            tr = ThreatReport(
                input_type="text",
                suspicious_content_masked=sample_text,
                scam_category=cat,
                reporter_comments="Received this fake threat on my smartphone. Reporting for community defense.",
                reporter_contact_masked="98******10",
                is_simulated=True,
                status=random.choice(["PENDING_REVIEW", "VERIFIED_SCAM", "VERIFIED_SCAM"]),
                created_at=now - datetime.timedelta(days=random.randint(0, 5))
            )
            db.add(tr)

        db.commit()
        print(f"Successfully seeded 90 simulated analyses and 15 simulated threat reports!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
