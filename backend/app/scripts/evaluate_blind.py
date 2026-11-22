#!/usr/bin/env python3
"""
UPI Rakshak AI — Gold v3 Blind Evaluation Harness
Executes a single, non-tuning evaluation pass over an external labeled dataset
and generates docs/BLIND_EVALUATION.md with bootstrap confidence intervals.
"""

import os
import sys
import json
import time
import argparse
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from sklearn.metrics import classification_report, precision_recall_fscore_support

from backend.app.detectors.nlp_classifier import nlp_classifier
from backend.app.detectors.rule_engine import rule_engine
from backend.app.detectors.url_scanner import url_scanner
from backend.app.fusion.risk_engine import risk_engine

def bootstrap_ci(y_true, y_pred, metric_fn, n_bootstraps: int = 1000, alpha: float = 0.05, seed: int = 42):
    rng = np.random.RandomState(seed)
    n = len(y_true)
    if n == 0:
        return 0.0, 0.0, 0.0
    scores = []
    base_score = float(metric_fn(y_true, y_pred))
    for _ in range(n_bootstraps):
        idx = rng.randint(0, n, size=n)
        scores.append(metric_fn(y_true[idx], y_pred[idx]))
    scores = np.sort(scores)
    low_idx = max(0, int((alpha / 2.0) * n_bootstraps))
    high_idx = min(n_bootstraps - 1, int((1.0 - alpha / 2.0) * n_bootstraps))
    return base_score, float(scores[low_idx]), float(scores[high_idx])

def evaluate_blind_file(file_path: str, output_md: str = "docs/BLIND_EVALUATION.md"):
    if not file_path or not os.path.exists(file_path):
        print(f"[Notice] Blind evaluation file not provided or does not exist: {file_path}")
        os.makedirs(os.path.dirname(output_md), exist_ok=True)
        with open(output_md, "w", encoding="utf-8") as f:
            f.write("# UPI Rakshak AI — Gold v3 Blind Evaluation Report\n\n")
            f.write("> [!NOTE]\n")
            f.write("> **Status**: Pending External Human Data Collection.\n")
            f.write("> To evaluate an external blind dataset, run:\n")
            f.write("> ```bash\n> make evaluate-blind FILE=path/to/gold_v3.json\n> ```\n\n")
            f.write("See [docs/GOLD_V3.md](GOLD_V3.md) for the external data collection protocol and masking guidelines.\n")
        print(f"Written pending placeholder to {output_md}")
        return

    print("=" * 65)
    print("  UPI RAKSHAK AI — GOLD v3 BLIND BENCHMARK EVALUATION")
    print("=" * 65)
    print(f"Evaluating blind dataset: {file_path}")

    if file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
        data = df.to_dict(orient="records")
    else:
        raise ValueError("Unsupported format. Please supply a JSON or CSV file.")

    if not data:
        print("[Warning] Supplied dataset is empty.")
        return

    true_categories = []
    nlp_pred_categories = []
    fusion_verdicts = []
    fusion_scores = []
    languages = []
    latencies = []
    error_list = []

    for idx, item in enumerate(data):
        text = str(item.get("text", "")).strip()
        true_cat = str(item.get("category", "legitimate")).strip()
        lang_hint = str(item.get("language", "en")).strip()

        if not text:
            continue

        t0 = time.perf_counter()
        nlp_res = nlp_classifier.predict(text)
        rule_res = rule_engine.evaluate(text)
        url_res = url_scanner.scan_all_urls(text)
        report = risk_engine.fuse("text", text, nlp_res, rule_res, url_res)
        latency = (time.perf_counter() - t0) * 1000.0

        pred_cat = nlp_res["category"]
        verdict = report.verdict
        score = report.risk_score

        true_categories.append(true_cat)
        nlp_pred_categories.append(pred_cat)
        fusion_verdicts.append(verdict)
        fusion_scores.append(score)
        languages.append(lang_hint)
        latencies.append(latency)

        is_scam = (true_cat != "legitimate")
        pred_scam = (verdict in ["SUSPICIOUS", "HIGH RISK"])

        if is_scam != pred_scam or true_cat != pred_cat:
            error_list.append({
                "index": idx + 1,
                "text": text[:120] + ("..." if len(text) > 120 else ""),
                "true_category": true_cat,
                "predicted_category": pred_cat,
                "fusion_verdict": verdict,
                "risk_score": score,
                "confidence": nlp_res.get("confidence", 0.0),
                "is_binary_error": (is_scam != pred_scam)
            })

    total_samples = len(true_categories)
    y_true = np.array(true_categories)
    y_pred = np.array(nlp_pred_categories)

    # 1. 15-class Macro-F1
    def macro_f1_fn(yt, yp):
        return classification_report(yt, yp, output_dict=True, zero_division=0)["macro avg"]["f1-score"]
    macro_f1, f1_low, f1_high = bootstrap_ci(y_true, y_pred, macro_f1_fn)

    # 2. Binary Fusion Metrics
    bin_true = (y_true != "legitimate").astype(int)
    bin_pred = np.array([1 if v in ["SUSPICIOUS", "HIGH RISK"] else 0 for v in fusion_verdicts])

    def recall_fn(yt, yp):
        tp = int(((yt == 1) & (yp == 1)).sum())
        fn = int(((yt == 1) & (yp == 0)).sum())
        return (tp / (tp + fn)) if (tp + fn) > 0 else 0.0

    def fpr_fn(yt, yp):
        fp = int(((yt == 0) & (yp == 1)).sum())
        tn = int(((yt == 0) & (yp == 0)).sum())
        return (fp / (fp + tn)) if (fp + tn) > 0 else 0.0

    def prec_fn(yt, yp):
        tp = int(((yt == 1) & (yp == 1)).sum())
        fp = int(((yt == 0) & (yp == 1)).sum())
        return (tp / (tp + fp)) if (tp + fp) > 0 else 0.0

    def f1_bin_fn(yt, yp):
        p = prec_fn(yt, yp)
        r = recall_fn(yt, yp)
        return (2 * p * r / (p + r)) if (p + r) > 0 else 0.0

    rec_base, rec_low, rec_high = bootstrap_ci(bin_true, bin_pred, recall_fn)
    fpr_base, fpr_low, fpr_high = bootstrap_ci(bin_true, bin_pred, fpr_fn)
    prec_base, prec_low, prec_high = bootstrap_ci(bin_true, bin_pred, prec_fn)
    f1b_base, f1b_low, f1b_high = bootstrap_ci(bin_true, bin_pred, f1_bin_fn)

    # 3. Per-Language Breakdown
    lang_breakdown = {}
    for lang in sorted(list(set(languages))):
        mask = (np.array(languages) == lang)
        if mask.sum() == 0:
            continue
        yt_lang = bin_true[mask]
        yp_lang = bin_pred[mask]
        l_rec = recall_fn(yt_lang, yp_lang)
        l_fpr = fpr_fn(yt_lang, yp_lang)
        lang_breakdown[lang] = {
            "count": int(mask.sum()),
            "recall": l_rec,
            "fpr": l_fpr
        }

    # Generate Markdown Report
    os.makedirs(os.path.dirname(output_md), exist_ok=True)
    with open(output_md, "w", encoding="utf-8") as f:
        f.write("# UPI Rakshak AI — Gold v3 Blind Evaluation Report\n\n")
        f.write("> [!IMPORTANT]\n")
        f.write("> **Strict Blind Integrity Standard**:\n")
        f.write("> Evaluated strictly **once** on external user-submitted data. Zero parameter tuning or model retraining.\n")
        f.write(f"> **Source File**: `{os.path.basename(file_path)}` | **Total Samples**: `{total_samples}` | **Evaluation Timestamp**: `{time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}`\n\n")
        f.write("---\n\n")

        f.write("## 1. Executive Summary & Core Blind Metrics\n\n")
        f.write("| Evaluation Metric | Target Benchmark | Measured Value (95% CI) | Status |\n")
        f.write("| :--- | :---: | :---: | :---: |\n")
        f.write(f"| **Risk Fusion Scam Recall** | >= 95.0% | **{rec_base * 100:.2f}%** [{rec_low * 100:.2f}%, {rec_high * 100:.2f}%] | **{'PASSED' if rec_base >= 0.95 else 'FAILED'}** |\n")
        f.write(f"| **Legitimate False Positive Rate (FPR)** | <= 3.0% | **{fpr_base * 100:.2f}%** [{fpr_low * 100:.2f}%, {fpr_high * 100:.2f}%] | **{'PASSED' if fpr_base <= 0.03 else 'FAILED'}** |\n")
        f.write(f"| **Binary Precision** | >= 95.0% | **{prec_base * 100:.2f}%** [{prec_low * 100:.2f}%, {prec_high * 100:.2f}%] | **{'PASSED' if prec_base >= 0.95 else 'FAILED'}** |\n")
        f.write(f"| **Binary F1-Score** | >= 0.9500 | **{f1b_base:.4f}** [{f1b_low:.4f}, {f1b_high:.4f}] | **{'PASSED' if f1b_base >= 0.95 else 'FAILED'}** |\n")
        f.write(f"| **15-Class NLP Macro-F1** | >= 0.8500 | **{macro_f1:.4f}** [{f1_low:.4f}, {f1_high:.4f}] | **{'PASSED' if macro_f1 >= 0.85 else 'FAILED'}** |\n\n")

        f.write("---\n\n")
        f.write("## 2. Per-Language Performance Breakdown\n\n")
        f.write("| Language Code | Sample Count | Scam Recall | Legitimate FPR |\n")
        f.write("| :--- | :---: | :---: | :---: |\n")
        for lang, stats in lang_breakdown.items():
            f.write(f"| **{lang}** | {stats['count']} | {stats['recall'] * 100:.2f}% | {stats['fpr'] * 100:.2f}% |\n")
        f.write("\n---\n\n")

        f.write("## 3. Latency Profile\n\n")
        f.write(f"- **p50 Latency**: `{np.percentile(latencies, 50):.2f} ms`\n")
        f.write(f"- **p95 Latency**: `{np.percentile(latencies, 95):.2f} ms`\n")
        f.write(f"- **Mean Latency**: `{np.mean(latencies):.2f} ms`\n\n")

        f.write("---\n\n")
        f.write("## 4. Comprehensive Error Audit List\n\n")
        if not error_list:
            f.write("No errors detected on this evaluation set.\n")
        else:
            f.write(f"Total Errors Recorded: **{len(error_list)}** (Binary Errors: {sum(1 for e in error_list if e['is_binary_error'])})\n\n")
            f.write("| # | True Category | Predicted Category | Fusion Verdict | Risk Score | Snippet |\n")
            f.write("| :---: | :--- | :--- | :--- | :---: | :--- |\n")
            for err in error_list[:50]:
                f.write(f"| {err['index']} | `{err['true_category']}` | `{err['predicted_category']}` | `{err['fusion_verdict']}` | {err['risk_score']} | {err['text']} |\n")

    print(f"Blind evaluation complete. Generated report at: {output_md}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate a blind external labeled test set.")
    parser.add_argument("--file", "-f", default="", help="Path to blind dataset (JSON or CSV)")
    parser.add_argument("--output", "-o", default="docs/BLIND_EVALUATION.md", help="Output Markdown report path")
    args = parser.parse_args()
    evaluate_blind_file(args.file, args.output)
