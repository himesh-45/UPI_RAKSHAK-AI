import os
import random
import pandas as pd
from typing import List, Dict, Any
from backend.app.detectors.url_scanner import url_scanner, OFFICIAL_ENTITIES, SUSPICIOUS_TLDS

def evaluate_url_engine():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "external")
    openphish_path = os.path.join(data_dir, "openphish_feed.txt")
    benign_path = os.path.join(data_dir, "benign_domains.csv")

    phish_urls = []
    if os.path.exists(openphish_path):
        with open(openphish_path, "r", encoding="utf-8") as f:
            phish_urls = [line.strip() for line in f if line.strip() and line.startswith("http")]

    benign_domains = []
    if os.path.exists(benign_path):
        df_benign = pd.read_csv(benign_path)
        benign_domains = [f"https://{dom}" for dom in df_benign["domain"].dropna().tolist()]

    # 1. Synthesize 200+ adversarial typosquats, subdomain tricks, homoglyphs
    adversarial_phishing = []
    for entity in OFFICIAL_ENTITIES[:40]:
        brand = entity["brand"]
        off = entity["domains"][0]
        off_stem = off.split(".")[0]

        # Subdomain trick
        adversarial_phishing.append(f"http://{off}.verify-login-update.xyz/auth")
        adversarial_phishing.append(f"https://{off}.security-alert.top/session")
        # Hyphenated brand
        adversarial_phishing.append(f"http://{brand}-kyc-verification.online")
        adversarial_phishing.append(f"https://{brand}-refund-claim.site/login")
        # Typosquat
        adversarial_phishing.append(f"http://{off_stem}i.co.in/banking")
        adversarial_phishing.append(f"https://online-{brand}.biz")
        # Direct IP
        adversarial_phishing.append(f"http://192.168.{random.randint(1,254)}.{random.randint(1,254)}/{brand}/login")

    # Sample balanced sets
    random.seed(42)
    selected_phish = (phish_urls[:150] if phish_urls else []) + adversarial_phishing[:200]
    selected_benign = benign_domains[:len(selected_phish)] if benign_domains else []

    # Add official bank/UPI domains to benign
    for entity in OFFICIAL_ENTITIES:
        for dom in entity["domains"]:
            selected_benign.append(f"https://{dom}")
            selected_benign.append(f"https://retail.{dom}/portal")

    print(f"Testing URL Scanner on {len(selected_phish)} malicious/phishing URLs and {len(selected_benign)} benign/official URLs...")

    # Evaluate Phishing Recall (TP / (TP + FN))
    tp = 0
    fn = 0
    for u in selected_phish:
        res = url_scanner.analyze_url(u)
        if res["is_suspicious"]:
            tp += 1
        else:
            fn += 1

    # Evaluate Benign False Positive Rate (FP / (FP + TN))
    tn = 0
    fp = 0
    for u in selected_benign:
        res = url_scanner.analyze_url(u)
        if res["is_suspicious"]:
            fp += 1
        else:
            tn += 1

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    print("\n--- URL SCANNER BENCHMARK RESULTS ---")
    print(f"Total Evaluated: {tp + tn + fp + fn}")
    print(f"Accuracy:        {accuracy * 100:.2f}%")
    print(f"Precision:       {precision * 100:.2f}%")
    print(f"Recall:          {recall * 100:.2f}% (Phishing detection rate)")
    print(f"FPR:             {fpr * 100:.2f}% (Benign false positive rate)")
    print(f"F1-Score:        {f1:.4f}")

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "fpr": fpr,
        "f1": f1,
        "sample_counts": {"phish": len(selected_phish), "benign": len(selected_benign)}
    }

if __name__ == "__main__":
    evaluate_url_engine()
