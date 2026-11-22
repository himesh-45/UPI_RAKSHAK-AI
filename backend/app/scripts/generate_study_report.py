#!/usr/bin/env python3
"""
UPI Rakshak AI — User Study Analysis Report Generator
Processes anonymous responses from the /study experiment harness and generates
docs/USER_STUDY_REPORT.md comparing pre-tool intuition vs post-tool decision outcomes.
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Tuple
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from backend.app.models.db_models import StudyResponse

def bootstrap_acc_ci(correct_arr: np.ndarray, n_bootstraps: int = 1000, alpha: float = 0.05, seed: int = 42) -> Tuple[float, float, float]:
    rng = np.random.RandomState(seed)
    n = len(correct_arr)
    if n == 0:
        return 0.0, 0.0, 0.0
    scores = []
    base_acc = float(np.mean(correct_arr))
    for _ in range(n_bootstraps):
        idx = rng.randint(0, n, size=n)
        scores.append(np.mean(correct_arr[idx]))
    scores = np.sort(scores)
    low_idx = max(0, int((alpha / 2.0) * n_bootstraps))
    high_idx = min(n_bootstraps - 1, int((1.0 - alpha / 2.0) * n_bootstraps))
    return base_acc, float(scores[low_idx]), float(scores[high_idx])

def generate_report(output_path: str = "docs/USER_STUDY_REPORT.md"):
    print("=" * 65)
    print("  UPI RAKSHAK AI — USER STUDY STATISTICAL REPORT GENERATOR")
    print("=" * 65)

    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        responses = db.query(StudyResponse).all()
    finally:
        db.close()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not responses:
        print("[Notice] No participant responses recorded in database yet.")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# UPI Rakshak AI — Empirical User Study Report\n\n")
            f.write("> [!NOTE]\n")
            f.write("> **Status**: Study Harness Active (0 Participant Responses Recorded).\n")
            f.write("> The study protocol and web harness are deployed at `/study`.\n")
            f.write("> In strict adherence to our anti-fabrication rules, zero artificial responses have been synthesized.\n\n")
            f.write("---\n\n")
            f.write("## 1. Study Methodology & Experimental Design\n\n")
            f.write("- **Protocol**: Within-subjects randomized trial comparing human fraud detection accuracy before vs after evidence disclosure.\n")
            f.write("- **Sample Size Target**: 30+ independent human participants (300+ total decision trials across en, hi, te).\n")
            f.write("- **Phased Evaluation Protocol**:\n")
            f.write("  1. **Phase 1 (Pre-Tool Baseline)**: Participant evaluates randomized payment communication (Scam vs Genuine) and indicates confidence (1-5).\n")
            f.write("  2. **Phase 2 (Evidence Disclosure)**: System displays multi-layer verdict, risk score, and top 3 evidence points.\n")
            f.write("  3. **Phase 3 (Post-Tool Decision Impact)**: Participant reports if evidence altered their decision, provides revised verdict, and rates explanation clarity.\n")
            f.write("- **Admin Export**: Responses can be exported via `GET /api/study/export` (authorized admin endpoint) or evaluated programmatically with `make study-report`.\n")
        print(f"Report written to: {output_path}")
        return

    # Process live responses
    data = []
    for r in responses:
        revised_is_scam = (r.user_revised_guess.lower() == "scam") if r.user_revised_guess else (r.user_guess.lower() == "scam")
        user_revised_correct = (revised_is_scam == r.ground_truth_is_scam)
        data.append({
            "session_id": r.session_id,
            "item_id": r.item_id,
            "language": r.language,
            "user_initial_correct": 1 if r.user_initial_correct else 0,
            "user_revised_correct": 1 if user_revised_correct else 0,
            "tool_correct": 1 if r.tool_correct else 0,
            "would_change": r.would_change_decision,
            "confidence": r.user_confidence,
            "clarity": r.explanation_clarity or 5
        })

    df = pd.DataFrame(data)
    total_sessions = df["session_id"].nunique()
    total_trials = len(df)

    # Compute metrics
    init_acc, init_low, init_high = bootstrap_acc_ci(df["user_initial_correct"].values)
    post_acc, post_low, post_high = bootstrap_acc_ci(df["user_revised_correct"].values)
    tool_acc, tool_low, tool_high = bootstrap_acc_ci(df["tool_correct"].values)
    avg_clarity = df["clarity"].mean()

    # Per language breakdown
    lang_stats = {}
    for lang, group in df.groupby("language"):
        l_init, _, _ = bootstrap_acc_ci(group["user_initial_correct"].values)
        l_post, _, _ = bootstrap_acc_ci(group["user_revised_correct"].values)
        lang_stats[lang] = {
            "trials": len(group),
            "pre_acc": l_init,
            "post_acc": l_post,
            "delta": (l_post - l_init) * 100.0
        }

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# UPI Rakshak AI — Empirical User Study Report\n\n")
        f.write(f"> **Participants**: `{total_sessions}` | **Total Decision Trials**: `{total_trials}`\n\n")
        f.write("## 1. Human Decision Impact: Before vs After Evidence Disclosure\n\n")
        f.write("| Evaluation Stage | Accuracy (95% CI) | Relative Improvement |\n")
        f.write("| :--- | :---: | :---: |\n")
        f.write(f"| **Pre-Tool Human Baseline** | **{init_acc * 100:.2f}%** [{init_low * 100:.2f}%, {init_high * 100:.2f}%] | Reference Baseline |\n")
        f.write(f"| **Post-Tool Human Accuracy** | **{post_acc * 100:.2f}%** [{post_low * 100:.2f}%, {post_high * 100:.2f}%] | **+{(post_acc - init_acc) * 100:.2f}%** |\n")
        f.write(f"| **Standalone Tool Accuracy** | **{tool_acc * 100:.2f}%** [{tool_low * 100:.2f}%, {tool_high * 100:.2f}%] | Diagnostic Upper Bound |\n\n")

        f.write(f"**Mean Explanation Clarity Rating**: `{avg_clarity:.2f} / 5.0`\n\n")

        f.write("## 2. Per-Language User Accuracy Breakdown\n\n")
        f.write("| Language | Trials | Pre-Tool Accuracy | Post-Tool Accuracy | Delta |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: |\n")
        for lang, st in lang_stats.items():
            f.write(f"| **{lang}** | {st['trials']} | {st['pre_acc'] * 100:.2f}% | {st['post_acc'] * 100:.2f}% | +{st['delta']:.2f}% |\n")

    print(f"Generated user study report: {output_path}")

if __name__ == "__main__":
    generate_report()
