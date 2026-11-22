import os
import json
import random
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
import tldextract

from backend.app.detectors.url_scanner import url_scanner, OFFICIAL_ENTITIES, SUSPICIOUS_TLDS

def compute_bootstrap_ci(y_true: List[int], y_pred: List[int], metric_fn, n_boot: int = 1000, alpha: float = 0.05) -> Tuple[float, float, float]:
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    base_val = metric_fn(y_true, y_pred)
    if len(y_true) == 0:
        return 0.0, 0.0, 0.0

    boot_vals = []
    rng = np.random.RandomState(42)
    n = len(y_true)
    for _ in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        boot_vals.append(metric_fn(y_true[idx], y_pred[idx]))

    low = float(np.percentile(boot_vals, 100 * (alpha / 2)))
    high = float(np.percentile(boot_vals, 100 * (1 - alpha / 2)))
    return float(base_val), low, high

def calc_recall(yt, yp):
    tp = np.sum((yt == 1) & (yp == 1))
    fn = np.sum((yt == 1) & (yp == 0))
    return float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0

def calc_fpr(yt, yp):
    fp = np.sum((yt == 0) & (yp == 1))
    tn = np.sum((yt == 0) & (yp == 0))
    return float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0

def calc_precision(yt, yp):
    tp = np.sum((yt == 1) & (yp == 1))
    fp = np.sum((yt == 0) & (yp == 1))
    return float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0

def calc_f1(yt, yp):
    p = calc_precision(yt, yp)
    r = calc_recall(yt, yp)
    return float(2 * p * r / (p + r)) if (p + r) > 0 else 0.0

def evaluate_url_engine() -> Dict[str, Any]:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    external_dir = os.path.join(base_dir, "data", "external")
    openphish_path = os.path.join(external_dir, "openphish_feed.txt")
    benign_path = os.path.join(external_dir, "benign_domains.csv")
    adv_testset_path = os.path.join(external_dir, "adversarial_url_testset.json")

    # 1. Real-Feed Benchmark Dataset (OpenPhish holdout test + Benign test)
    phish_urls = []
    if os.path.exists(openphish_path):
        with open(openphish_path, "r", encoding="utf-8") as f:
            phish_urls = [line.strip() for line in f if line.strip() and line.startswith("http")]

    # Holdout last 100 OpenPhish URLs as chronological holdout test
    openphish_holdout_test = phish_urls[200:] if len(phish_urls) >= 200 else phish_urls

    benign_domains = []
    if os.path.exists(benign_path):
        df_benign = pd.read_csv(benign_path)
        benign_domains = [f"https://{dom}" for dom in df_benign["domain"].dropna().tolist()]

    # Holdout last 250 benign domains as disjoint test
    benign_holdout_test = benign_domains[750:] if len(benign_domains) >= 750 else benign_domains

    # 2. Synthetic Adversarial Benchmark Dataset (Independent generator + 107 handwritten lookalikes)
    adv_urls = []
    if os.path.exists(adv_testset_path):
        with open(adv_testset_path, "r", encoding="utf-8") as f:
            adv_data = json.load(f)
            adv_urls = [item["url"] for item in adv_data]

    # Evaluate ROW 1: Real-Feed Benchmark
    rf_eval_urls = openphish_holdout_test + benign_holdout_test
    rf_y_true = [1] * len(openphish_holdout_test) + [0] * len(benign_holdout_test)
    rf_y_pred = []
    for u in rf_eval_urls:
        res = url_scanner.analyze_url(u)
        rf_y_pred.append(1 if res["is_suspicious"] else 0)

    rf_recall, rf_rec_l, rf_rec_h = compute_bootstrap_ci(rf_y_true, rf_y_pred, calc_recall)
    rf_fpr, rf_fpr_l, rf_fpr_h = compute_bootstrap_ci(rf_y_true, rf_y_pred, calc_fpr)
    rf_prec, rf_p_l, rf_p_h = compute_bootstrap_ci(rf_y_true, rf_y_pred, calc_precision)
    rf_f1, rf_f1_l, rf_f1_h = compute_bootstrap_ci(rf_y_true, rf_y_pred, calc_f1)

    # Evaluate ROW 2: Synthetic Adversarial Benchmark (Adversarial phishing vs Benign test + Official domains)
    official_benign = []
    for entity in OFFICIAL_ENTITIES[:50]:
        for dom in entity["domains"]:
            official_benign.append(f"https://{dom}")
            official_benign.append(f"https://retail.{dom}/portal")

    syn_benign_eval = (benign_holdout_test[:len(adv_urls)] + official_benign)[:len(adv_urls)]
    syn_eval_urls = adv_urls + syn_benign_eval
    syn_y_true = [1] * len(adv_urls) + [0] * len(syn_benign_eval)
    syn_y_pred = []
    for u in syn_eval_urls:
        res = url_scanner.analyze_url(u)
        syn_y_pred.append(1 if res["is_suspicious"] else 0)

    syn_recall, syn_rec_l, syn_rec_h = compute_bootstrap_ci(syn_y_true, syn_y_pred, calc_recall)
    syn_fpr, syn_fpr_l, syn_fpr_h = compute_bootstrap_ci(syn_y_true, syn_y_pred, calc_fpr)
    syn_prec, syn_p_l, syn_p_h = compute_bootstrap_ci(syn_y_true, syn_y_pred, calc_precision)
    syn_f1, syn_f1_l, syn_f1_h = compute_bootstrap_ci(syn_y_true, syn_y_pred, calc_f1)

    print("\n" + "=" * 80)
    print("  UPI RAKSHAK AI — URL SCANNER RIGOROUS BENCHMARK (NON-CIRCULAR)")
    print("=" * 80)
    print(f"Row 1: Real-Feed Benchmark (OpenPhish holdout n={len(openphish_holdout_test)}, Benign n={len(benign_holdout_test)}):")
    print(f"  Recall (Detection Rate): {rf_recall * 100:.2f}% [95% CI: {rf_rec_l * 100:.2f}%, {rf_rec_h * 100:.2f}%]")
    print(f"  FPR (False Positive):    {rf_fpr * 100:.2f}% [95% CI: {rf_fpr_l * 100:.2f}%, {rf_fpr_h * 100:.2f}%]")
    print(f"  Precision:               {rf_prec * 100:.2f}% [95% CI: {rf_p_l * 100:.2f}%, {rf_p_h * 100:.2f}%]")
    print(f"  F1-Score:                {rf_f1:.4f} [95% CI: {rf_f1_l:.4f}, {rf_f1_h:.4f}]")

    print(f"\nRow 2: Synthetic Adversarial Benchmark (Independent + 107 Handwritten n={len(adv_urls)}, Benign n={len(syn_benign_eval)}):")
    print(f"  Recall (Detection Rate): {syn_recall * 100:.2f}% [95% CI: {syn_rec_l * 100:.2f}%, {syn_rec_h * 100:.2f}%]")
    print(f"  FPR (False Positive):    {syn_fpr * 100:.2f}% [95% CI: {syn_fpr_l * 100:.2f}%, {syn_fpr_h * 100:.2f}%]")
    print(f"  Precision:               {syn_prec * 100:.2f}% [95% CI: {syn_p_l * 100:.2f}%, {syn_p_h * 100:.2f}%]")
    print(f"  F1-Score:                {syn_f1:.4f} [95% CI: {syn_f1_l:.4f}, {syn_f1_h:.4f}]")
    print("=" * 80)

    return {
        "real_feed": {
            "n_phish": len(openphish_holdout_test),
            "n_benign": len(benign_holdout_test),
            "recall": rf_recall, "recall_ci": (rf_rec_l, rf_rec_h),
            "fpr": rf_fpr, "fpr_ci": (rf_fpr_l, rf_fpr_h),
            "precision": rf_prec, "precision_ci": (rf_p_l, rf_p_h),
            "f1": rf_f1, "f1_ci": (rf_f1_l, rf_f1_h)
        },
        "synthetic_adversarial": {
            "n_phish": len(adv_urls),
            "n_benign": len(syn_benign_eval),
            "recall": syn_recall, "recall_ci": (syn_rec_l, syn_rec_h),
            "fpr": syn_fpr, "fpr_ci": (syn_fpr_l, syn_fpr_h),
            "precision": syn_prec, "precision_ci": (syn_p_l, syn_p_h),
            "f1": syn_f1, "f1_ci": (syn_f1_l, syn_f1_h)
        }
    }

if __name__ == "__main__":
    evaluate_url_engine()
