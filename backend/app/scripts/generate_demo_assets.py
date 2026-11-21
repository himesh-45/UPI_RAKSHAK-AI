import os
import json
import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_demo_assets():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # backend/app
    backend_assets_dir = os.path.join(base_dir, "data", "demo_assets")
    root_dir = os.path.dirname(os.path.dirname(base_dir)) # workspace root
    frontend_assets_dir = os.path.join(root_dir, "frontend", "public", "demo_assets")
    
    os.makedirs(backend_assets_dir, exist_ok=True)
    os.makedirs(frontend_assets_dir, exist_ok=True)

    # 1. Generate QR Code Images
    qr_specs = [
        {
            "filename": "qr_fake_cashback.png",
            "data": "upi://pay?pa=scammer891@okhdfcbank&pn=GPay%20Cashback%20Reward&am=2999.00&cu=INR&tn=UPI%20Cashback%20Claim",
            "title": "Fake GPay Cashback QR (Deceptive collect lure)"
        },
        {
            "filename": "qr_electricity_scam.png",
            "data": "upi://pay?pa=officer994@ybl&pn=Electricity%20Bill%20Office&am=4850.00&cu=INR&tn=Power%20Disconnection%20Cancellation",
            "title": "Electricity Bill Threat QR (Impersonated VPA)"
        },
        {
            "filename": "qr_phishing_link.png",
            "data": "http://sbi-kyc-update-portal.top/auth-verify",
            "title": "Phishing Link QR Code (Typosquatted domain)"
        },
        {
            "filename": "qr_safe_merchant.png",
            "data": "upi://pay?pa=irctc@icici&pn=IRCTC%20Official&am=420.00&cu=INR&tn=Train%20Ticket%20Booking",
            "title": "Safe Merchant QR (Verified IRCTC)"
        }
    ]

    for spec in qr_specs:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(spec["data"])
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        path1 = os.path.join(backend_assets_dir, spec["filename"])
        path2 = os.path.join(frontend_assets_dir, spec["filename"])
        img.save(path1)
        img.save(path2)
        print(f"Generated QR: {spec['filename']}")

    # 2. Generate Screenshot Images with text
    def create_mock_screenshot(filename: str, title: str, sender: str, message: str, bg_color="#0f172a", card_color="#1e293b", text_color="#f8fafc"):
        width, height = 650, 360
        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Draw card container
        draw.rounded_rectangle([30, 30, width - 30, height - 30], radius=16, fill=card_color, outline="#334155", width=2)
        
        # Draw header bar
        draw.rounded_rectangle([30, 30, width - 30, 90], radius=16, fill="#334155")
        draw.text((50, 48), f"SIMULATED SMS PREVIEW — {title}", fill="#94a3b8")
        draw.text((50, 110), f"Sender: {sender}", fill="#38bdf8")

        # Word wrap message lines
        words = message.split()
        lines = []
        current = ""
        for w in words:
            if len(current + " " + w) < 48:
                current += (" " if current else "") + w
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)

        y = 150
        for line in lines:
            draw.text((50, y), line, fill=text_color)
            y += 28

        # Draw footer notice
        draw.text((50, height - 60), "[FICTIONAL DEMO SAMPLE - FOR FRAUD TESTING ONLY]", fill="#ef4444")

        path1 = os.path.join(backend_assets_dir, filename)
        path2 = os.path.join(frontend_assets_dir, filename)
        img.save(path1)
        img.save(path2)
        print(f"Generated Screenshot: {filename}")

    create_mock_screenshot(
        "screenshot_sbi_kyc.png",
        "Fake Bank KYC Phishing",
        "VM-SBIBNK",
        "Dear customer, your SBI account will be BLOCKED tonight due to pending KYC. Click immediately to update: http://sbi-kyc-verify.top/login"
    )

    create_mock_screenshot(
        "screenshot_kbc_lottery.png",
        "KBC Lottery Scam",
        "+91-98765-XXXXX",
        "KBC Jio Lucky Draw: Congratulations! Your mobile number won 25 Lakh Rupees. Call Lottery Manager at +91-98765-22110 to claim prize."
    )

    create_mock_screenshot(
        "screenshot_electricity_scam.png",
        "Electricity Cut Threat",
        "VK-TNEBPW",
        "Dear Consumer, electricity power will be disconnected tonight at 9:30 PM due to unpaid bill of Rs. 4,850. Pay immediately at http://bill-pay.biz"
    )

    create_mock_screenshot(
        "screenshot_safe_bank_alert.png",
        "Genuine Bank Debit SMS",
        "AD-HDFCBK",
        "HDFC Bank: Rs. 1,450.00 debited from a/c 4821 on 21-Nov-2026. Bal: Rs. 24,190.00. NEVER share your OTP or PIN with anyone."
    )

    # 3. Create demo examples JSON registry (16+ examples across categories & languages)
    demo_examples = [
        {
            "id": "ex_classic_otp",
            "type": "text",
            "category": "otp_pin_theft",
            "language": "en",
            "label": "Classic OTP / Block Threat",
            "input": "Your UPI account will be blocked. Click here to verify immediately and enter your OTP: http://sbi-kyc-verify.top/verify",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_collect_cashback",
            "type": "text",
            "category": "fake_upi_refund_cashback",
            "language": "en",
            "label": "Collect Request PIN Scam",
            "input": "Congratulations! You have received a cashback refund of Rs. 3,500 on PhonePe. Enter your UPI PIN to claim money into your account.",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_hindi_electricity",
            "type": "text",
            "category": "electricity_disconnection",
            "language": "hi",
            "label": "Hindi Electricity Threat (हिंदी)",
            "input": "प्रिय उपभोक्ता, आपके बिजली का बिल अपडेट नहीं होने के कारण आज रात 9:30 बजे बिजली काट दी जाएगी। तुरंत हमारे बिजली अधिकारी से संपर्क करें या यहां भुगतान करें: http://bijli-bill-pay.online/auth",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_telugu_kyc",
            "type": "text",
            "category": "fake_bank_kyc",
            "language": "te",
            "label": "Telugu Bank KYC Scam (తెలుగు)",
            "input": "ప్రియమైన వినియోగదారుడా, మీ SBI ఖాతా కేవైసీ పెండింగ్ ఉన్నందున ఈ రాత్రి బ్లాక్ చేయబడుతుంది. వెంటనే నవీకరించండి: http://sbi-kyc-update-portal.top",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_remote_support",
            "type": "text",
            "category": "fake_customer_support",
            "language": "en",
            "label": "AnyDesk Remote Takeover",
            "input": "Dear user, for your pending UPI refund on HDFC, please install AnyDesk app from Play Store and share the 9-digit remote access code with our support officer.",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_kbc_lottery",
            "type": "text",
            "category": "lottery_prize",
            "language": "en",
            "label": "KBC 25 Lakh Lottery",
            "input": "KBC Jio Lucky Draw: Congratulations! Your mobile number won 25 Lakh Rupees in lottery. Deposit registration fee of Rs. 4,999 to claim prize: http://kbc-lucky-claim.xyz",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_fake_pm_yojana",
            "type": "text",
            "category": "fake_govt_scheme",
            "language": "hi",
            "label": "Fake PM Yojana Scheme (Hinglish)",
            "input": "Govt of India update: PM Kisan Yojana ke tahat sabhi nagrik ko Rs. 6,000 mil rahe hain. Abhi form bhare: http://pm-kisan-subsidy.site",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_safe_bank_debit",
            "type": "text",
            "category": "legitimate",
            "language": "en",
            "label": "Genuine Bank Alert (Safe)",
            "input": "HDFC Bank: An amount of Rs. 1,450.00 is debited from account ending 4821 on 21-Nov-2026 for UPI/Swiggy. Available balance: Rs. 24,190.00. NEVER share your OTP or PIN with anyone.",
            "expected_verdict": "SAFE"
        },
        {
            "id": "ex_safe_login_otp",
            "type": "text",
            "category": "legitimate",
            "language": "en",
            "label": "Genuine Login 2FA OTP (Safe)",
            "input": "SBI Security Alert: OTP for login to Internet Banking is 482910. Valid for 10 minutes. Do NOT share OTP or password with anyone, including bank staff.",
            "expected_verdict": "SAFE"
        },
        {
            "id": "ex_safe_utility_bill",
            "type": "text",
            "category": "legitimate",
            "language": "en",
            "label": "Genuine Electricity Bill (Safe)",
            "input": "Dear Customer, your BESCOM electricity bill for account 1092837 is Rs. 1,280. Due date is 28-Nov-2026. Pay safely at official portal https://bescom.karnataka.gov.in",
            "expected_verdict": "SAFE"
        },
        {
            "id": "ex_url_ip_phishing",
            "type": "url",
            "category": "fake_bank_kyc",
            "language": "en",
            "label": "IP-Address Phishing URL",
            "input": "http://103.22.18.9/sbi-netbanking-login/verify",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_url_typosquatting",
            "type": "url",
            "category": "fake_bank_kyc",
            "language": "en",
            "label": "Brand Typosquatting URL",
            "input": "http://sbi-kyc-update-login.top/auth?ref=9182",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_url_safe_official",
            "type": "url",
            "category": "legitimate",
            "language": "en",
            "label": "Official Bank Domain (Safe)",
            "input": "https://www.onlinesbi.sbi",
            "expected_verdict": "SAFE"
        },
        {
            "id": "ex_qr_fake_cashback",
            "type": "image",
            "category": "fake_upi_refund_cashback",
            "language": "en",
            "label": "Fake Cashback QR Image",
            "image_filename": "qr_fake_cashback.png",
            "input": "demo_assets/qr_fake_cashback.png",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_qr_electricity",
            "type": "image",
            "category": "electricity_disconnection",
            "language": "en",
            "label": "Electricity Bill Threat QR Image",
            "image_filename": "qr_electricity_scam.png",
            "input": "demo_assets/qr_electricity_scam.png",
            "expected_verdict": "HIGH RISK"
        },
        {
            "id": "ex_qr_safe_merchant",
            "type": "image",
            "category": "legitimate",
            "language": "en",
            "label": "Safe IRCTC Merchant QR Image",
            "image_filename": "qr_safe_merchant.png",
            "input": "demo_assets/qr_safe_merchant.png",
            "expected_verdict": "SAFE"
        }
    ]

    examples_path1 = os.path.join(base_dir, "data", "demo_examples.json")
    examples_path2 = os.path.join(frontend_assets_dir, "demo_examples.json")

    with open(examples_path1, "w", encoding="utf-8") as f:
        json.dump(demo_examples, f, indent=2, ensure_ascii=False)
    with open(examples_path2, "w", encoding="utf-8") as f:
        json.dump(demo_examples, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(demo_examples)} demo examples in {examples_path1} and {examples_path2}")

if __name__ == "__main__":
    generate_demo_assets()
