import os
import json
import random

# Completely independent target definitions (NOT importing OFFICIAL_ENTITIES or detector brand list)
INDEPENDENT_TARGET_BRANDS = [
    {"target": "sbi", "domain": "sbi.co.in"},
    {"target": "hdfc", "domain": "hdfcbank.com"},
    {"target": "icici", "domain": "icicibank.com"},
    {"target": "axis", "domain": "axisbank.com"},
    {"target": "pnb", "domain": "pnbindia.in"},
    {"target": "kotak", "domain": "kotak.com"},
    {"target": "bob", "domain": "bankofbaroda.in"},
    {"target": "canara", "domain": "canarabank.com"},
    {"target": "paytm", "domain": "paytm.com"},
    {"target": "phonepe", "domain": "phonepe.com"},
    {"target": "gpay", "domain": "pay.google.com"},
    {"target": "bhim", "domain": "bhimupi.org.in"},
    {"target": "cred", "domain": "cred.club"},
    {"target": "mobikwik", "domain": "mobikwik.com"},
    {"target": "airtel", "domain": "airtel.in"},
    {"target": "jio", "domain": "jio.com"},
    {"target": "uidai", "domain": "uidai.gov.in"},
    {"target": "incometax", "domain": "incometax.gov.in"},
    {"target": "irctc", "domain": "irctc.co.in"},
    {"target": "epfindia", "domain": "epfindia.gov.in"},
    {"target": "bescom", "domain": "bescom.karnataka.gov.in"},
    {"target": "tsspdcl", "domain": "tssouthernpower.com"},
    {"target": "uppcl", "domain": "upenergy.in"},
    {"target": "amazon", "domain": "amazon.in"},
    {"target": "flipkart", "domain": "flipkart.com"},
    {"target": "bluedart", "domain": "bluedart.com"},
    {"target": "fedex", "domain": "fedex.com"},
    {"target": "indiapost", "domain": "indiapost.gov.in"},
    {"target": "delhivery", "domain": "delhivery.com"}
]

# Distinct mutation engines:
# 1. Homoglyphs (Cyrillic visually identical unicode characters)
HOMOGLYPH_MAP = {
    'a': '\u0430',  # cyrillic small letter a
    'e': '\u0435',  # cyrillic small letter ie
    'i': '\u0456',  # cyrillic small letter byelorussian-ukrainian i
    'o': '\u043e',  # cyrillic small letter o
    'p': '\u0440',  # cyrillic small letter er
    'c': '\u0441',  # cyrillic small letter es
    'y': '\u0443',  # cyrillic small letter u (looks like y)
    'x': '\u0445',  # cyrillic small letter ha
}

# Keyboard adjacency typos (QWERTY distance)
ADJACENT_KEYS = {
    'a': ['s', 'q', 'z'], 'b': ['v', 'g', 'h', 'n'], 'c': ['x', 'd', 'v'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'], 'e': ['w', 'r', 'd', 's'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'], 'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'], 'i': ['u', 'o', 'k', 'j'],
    'k': ['j', 'i', 'o', 'l', 'm'], 'l': ['k', 'o', 'p'],
    'm': ['n', 'j', 'k'], 'n': ['b', 'h', 'j', 'm'], 'o': ['i', 'p', 'k', 'l'],
    'p': ['o', 'l'], 'r': ['e', 't', 'f', 'd'], 's': ['a', 'w', 'e', 'd', 'x', 'z'],
    't': ['r', 'y', 'g', 'f'], 'u': ['y', 'i', 'j', 'h'], 'v': ['c', 'f', 'g', 'b'],
    'w': ['q', 'e', 's'], 'y': ['t', 'u', 'h', 'g']
}

ABUSE_TLDS = ["xyz", "top", "online", "site", "club", "biz", "live", "cc", "monster", "cfd", "buzz", "rest"]

def mutate_homoglyph(text: str) -> str:
    res = list(text)
    mutated = False
    for i, ch in enumerate(res):
        if ch in HOMOGLYPH_MAP and random.random() < 0.6:
            res[i] = HOMOGLYPH_MAP[ch]
            mutated = True
    if not mutated:
        for i, ch in enumerate(res):
            if ch in HOMOGLYPH_MAP:
                res[i] = HOMOGLYPH_MAP[ch]
                break
    return "".join(res)

def mutate_keyboard_slip(text: str) -> str:
    if len(text) < 2:
        return text + "s"
    idx = random.randint(0, len(text) - 1)
    ch = text[idx]
    if ch in ADJACENT_KEYS and ADJACENT_KEYS[ch]:
        slip = random.choice(ADJACENT_KEYS[ch])
        return text[:idx] + slip + text[idx+1:]
    return text + "i"

def mutate_omission_or_double(text: str) -> str:
    if len(text) > 3 and random.random() < 0.5:
        # omit character
        idx = random.randint(1, len(text) - 2)
        return text[:idx] + text[idx+1:]
    else:
        # double character
        idx = random.randint(0, len(text) - 1)
        return text[:idx] + text[idx] + text[idx:]

# 100+ Hand-written authentic lookalikes matching actual Indian cyber scam campaigns
HANDWRITTEN_LOOKALIKES = [
    # Banking Phishing URLs
    "http://sbi-kyc-pan-update.top/login.php",
    "https://onlinesbi-retail-banking.xyz/session/login",
    "http://sbi-rewards-redeem-cash.site/claim",
    "https://sbi-verification-notice.online/auth",
    "http://statebank-kyc-mandate.biz/update",
    "https://hdfc-netbanking-rewards.xyz/claim-points",
    "http://hdfcbank-kyc-alert.top/verify.html",
    "https://hdfc-creditcard-unblock.online/secure",
    "http://netbanking-hdfc-portal.club/auth",
    "https://hdfc-fastag-recharge.site/pay",
    "http://icicibank-pan-link.top/form.php",
    "https://icici-rewards-cashback.xyz/portal",
    "http://imobile-pay-update.online/auth",
    "https://icicibank-security-check.biz/login",
    "http://axis-bank-kyc-verify.top/index.html",
    "https://axis-netbanking-session.xyz/login",
    "http://axis-credit-limit-upgrade.site/apply",
    "https://pnb-one-kyc-update.online/auth",
    "http://pnbindia-account-unblock.top/verify",
    "https://kotak-811-kyc-verification.xyz/kyc",
    "http://kotak-netbanking-login.site/portal",
    "https://canara-ai1-app-update.top/download.php",
    "http://bankofbaroda-bobworld-kyc.online/verify",
    "https://unionbank-of-india-kyc.xyz/auth",
    "http://idfcfirst-netbanking-login.top/account",
    "https://indusind-exclusive-rewards.site/claim",
    "http://yesbank-netbanking-update.online/login",

    # UPI & Payment Apps Phishing URLs
    "http://paytm-kyc-agent-support.online/auth",
    "https://paytm-gold-cashback-offer.xyz/claim",
    "http://paytmbank-fastag-wallet.top/recharge",
    "https://paytm-merchant-qr-settlement.site/pay",
    "http://phonepe-rewards-festive-cashback.xyz/accept",
    "https://phonepe-refund-desk-portal.top/collect",
    "http://phonepe-kyc-verification-help.online/auth",
    "https://phonepe-merchant-support.club/login",
    "http://gpay-scratch-card-cashback.site/redeem",
    "https://googlepay-festive-bonus.top/claim",
    "http://gpay-failed-transaction-refund.online/portal",
    "https://bhim-upi-reward-verification.xyz/claim",
    "http://cred-club-festive-cashback.link/redeem",
    "https://cred-coins-cash-conversion.top/wallet",
    "http://mobikwik-supercash-conversion.online/pay",
    "https://airtel-bank-kyc-biometric.xyz/update",
    "http://jio-payments-bank-kyc.top/verify",
    "https://ippb-postbank-kyc-update.online/login",

    # Electricity & Disconnection Scams
    "http://bescom-bill-disconnection.site/pay-now",
    "https://bescom-power-emergency-help.top/bill",
    "http://tsspdcl-electricity-officer.online/settle",
    "https://tsspdcl-bill-update-desk.xyz/pay",
    "http://uppcl-bijli-bill-payment.top/update",
    "https://uppcl-urgent-power-bill.site/notice",
    "http://tneb-electricity-suspension.online/pay",
    "https://msedcl-mahadiscom-urgent.xyz/bill",
    "http://tatapower-mumbai-disconnection.top/pay",
    "https://bses-yamuna-bill-clearance.site/auth",
    "http://adani-electricity-bill-helpline.online/clear",
    "https://pspcl-punjab-power-bill.top/settle",

    # Government Schemes & Portals Phishing
    "http://pmkisan-gov-status.live/beneficiary-list",
    "https://pmkisan-16th-kist-verify.top/claim",
    "http://uidai-aadhar-pan-link.xyz/verify",
    "https://aadhaar-biometric-lock-update.site/auth",
    "http://epfo-claim-status-pf.online/passbook",
    "https://epfindia-uan-kyc-update.top/login",
    "http://incometax-refund-approval.xyz/form",
    "https://incometax-tds-refund-portal.top/claim",
    "http://parivahan-echallan-payment.online/fine",
    "https://echallan-parivahan-traffic.top/pay",
    "http://ayushman-card-free-download.site/apply",
    "https://pm-awas-yojana-grant.online/register",
    "http://ladli-behna-kist-status.xyz/claim",

    # Courier, Customs & Postal Scams (incl. Digital Arrest links)
    "http://indiapost-parcel-delivery.club/track",
    "https://indiapost-redelivery-charge.top/pay",
    "http://speedpost-customs-clearance.online/fee",
    "https://bluedart-tracking-failed-delivery.site/update",
    "http://bluedart-courier-address-fix.xyz/reschedule",
    "https://delhivery-package-address-update.top/pin",
    "http://delhivery-customs-clearance.online/pay",
    "https://fedex-customs-narcotics-inquiry.xyz/case-notice",
    "http://fedex-parcel-hold-clearance.top/duty",
    "https://dhl-customs-airport-penalty.site/clear",
    "http://mumbai-customs-digital-case.online/summons",

    # E-Commerce & Marketplace Scams
    "http://flipkart-bigbillion-lucky-winner.top/claim",
    "https://flipkart-customer-support-refund.xyz/portal",
    "http://amazon-prime-festive-cashback.site/win",
    "https://amazonpay-order-cancellation-refund.top/auth",
    "http://olx-army-officer-qr-payment.online/verify",
    "https://meesho-lucky-draw-car-prize.xyz/register",

    # Job & Task Investment Scams
    "http://telegram-vip-task-earning.club/join",
    "https://youtube-video-like-daily-income.top/register",
    "http://crypto-arbitrage-multiplier.online/invest",
    "https://amazon-review-merchant-job.xyz/deposit",
    "http://global-tasks-daily-payout.site/dashboard",

    # Direct IP Phishing & Port Tricks
    "http://192.168.1.105/phonepe/reward/claim",
    "http://172.16.20.44:8080/sbi-netbanking/auth",
    "http://10.0.0.15/hdfc/login.php",
    "http://192.168.0.22/bescom/bill-pay",
    "http://123.45.67.89/kbc-lottery/winner",

    # Additional Real-World Scams (Telecom, KYC & Refunds)
    "http://airtel-thanks-vip-rewards.xyz/claim",
    "https://jio-5g-welcome-activation.top/sim",
    "http://vi-vodafone-kyc-verification.online/auth",
    "https://bsnl-broadband-bill-overdue.site/pay",
    "http://speedpost-tracking-consignment.top/status",
    "https://swiggy-refund-resolution.xyz/collect",
    "http://zomato-gold-free-membership.club/activate",
    "https://uber-trip-refund-support.online/claim",
    "http://ola-money-wallet-unblock.site/kyc",
    "https://bookmyshow-voucher-cashback.top/win"
]

def generate_adversarial_testset(n_synthetic: int = 250):
    samples = []
    
    # 1. Add all 100+ Handwritten Lookalikes
    for url in HANDWRITTEN_LOOKALIKES:
        samples.append({
            "url": url,
            "type": "handwritten_lookalike",
            "is_phishing": True
        })

    # 2. Generate independent synthetic typosquats using the distinct mutation engines
    random.seed(99)
    for i in range(n_synthetic):
        target = random.choice(INDEPENDENT_TARGET_BRANDS)
        brand = target["target"]
        dom = target["domain"]
        stem = dom.split(".")[0]
        tld = random.choice(ABUSE_TLDS)
        mode = random.choice(["homoglyph", "keyboard_slip", "double_omit", "subdomain_nest", "path_masq"])

        if mode == "homoglyph":
            mutated_stem = mutate_homoglyph(stem)
            url = f"https://{mutated_stem}.{tld}/login"
        elif mode == "keyboard_slip":
            mutated_stem = mutate_keyboard_slip(brand)
            url = f"http://{mutated_stem}-verify.{tld}/auth"
        elif mode == "double_omit":
            mutated_stem = mutate_omission_or_double(brand)
            url = f"https://secure-{mutated_stem}.{tld}/session"
        elif mode == "subdomain_nest":
            url = f"http://{dom}.customer-security-portal.{tld}/verify"
        elif mode == "path_masq":
            url = f"http://cloud-auth-verification.{tld}/{dom}/login"

        samples.append({
            "url": url,
            "type": f"synthetic_{mode}",
            "is_phishing": True
        })

    return samples

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base_dir, "data", "external")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "adversarial_url_testset.json")

    testset = generate_adversarial_testset(n_synthetic=250)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(testset, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(testset)} independent adversarial test cases ({len(HANDWRITTEN_LOOKALIKES)} handwritten, {len(testset) - len(HANDWRITTEN_LOOKALIKES)} synthetic).")
    print(f"Saved to: {out_file}")

if __name__ == "__main__":
    main()
