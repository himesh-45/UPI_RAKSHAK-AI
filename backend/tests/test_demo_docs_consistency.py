import os
import re
import pytest

DEMO_DOCS = [
    "docs/PITCH_OUTLINE.md",
    "docs/JUDGE_QA.md",
    "docs/DEMO_CHECKLIST.md",
    "docs/DEMO_RECORDING.md",
    "docs/DEMO_SCRIPT.md",
    "docs/DEMO_VIDEO.md",
    "docs/FINAL_STATUS.md",
]

def get_base_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def parse_evaluation_report_metrics():
    base_dir = get_base_dir()
    eval_path = os.path.join(base_dir, "docs", "EVALUATION_REPORT.md")
    assert os.path.exists(eval_path), f"EVALUATION_REPORT.md missing at {eval_path}"

    with open(eval_path, "r", encoding="utf-8") as f:
        eval_text = f.read()

    # Extract Risk Fusion Recall row
    m_recall = re.search(
        r'\|\s*\*\*Risk Fusion Scam Recall\*\*\s*\|\s*[^|]+\|\s*\*\*(\d+\.\d+)%\*\*\s*\(([^)]+)\)\s*\|\s*[^|]+\|\s*\*\*(\d+\.\d+)%\*\*\s*\(([^)]+)\)',
        eval_text
    )
    assert m_recall, "Could not find Risk Fusion Scam Recall in EVALUATION_REPORT.md"
    v1_recall = m_recall.group(1)
    v1_recall_ratio = m_recall.group(2)
    v2_recall = m_recall.group(3)
    v2_recall_ratio = m_recall.group(4)

    # Extract Legitimate FPR row
    m_fpr = re.search(
        r'\|\s*\*\*Legitimate False Positive Rate \(FPR\)\*\*\s*\|\s*[^|]+\|\s*\*\*(\d+\.\d+)%\*\*\s*\(([^)]+)\)\s*\|\s*[^|]+\|\s*\*\*(\d+\.\d+)%\*\*\s*\(([^)]+)\)',
        eval_text
    )
    assert m_fpr, "Could not find Legitimate FPR in EVALUATION_REPORT.md"
    v1_fpr = m_fpr.group(1)
    v1_fpr_ratio = m_fpr.group(2)
    v2_fpr = m_fpr.group(3)
    v2_fpr_ratio = m_fpr.group(4)

    # Extract Macro-F1 row
    m_f1 = re.search(
        r'\|\s*\*\*15-Class NLP Macro-F1\*\*\s*\|\s*[^|]+\|\s*\*\*(\d+\.\d+)\*\*',
        eval_text
    )
    assert m_f1, "Could not find 15-Class NLP Macro-F1 in EVALUATION_REPORT.md"
    v1_f1 = m_f1.group(1)

    return {
        "v1_recall": v1_recall,
        "v1_recall_ratio": v1_recall_ratio,
        "v2_recall": v2_recall,
        "v2_recall_ratio": v2_recall_ratio,
        "v1_fpr": v1_fpr,
        "v1_fpr_ratio": v1_fpr_ratio,
        "v2_fpr": v2_fpr,
        "v2_fpr_ratio": v2_fpr_ratio,
        "v1_f1": v1_f1,
    }

def test_demo_docs_do_not_contain_stale_metrics():
    """Assert that demo docs contain no stale, uncalibrated, or superseded benchmark numbers."""
    base_dir = get_base_dir()
    metrics = parse_evaluation_report_metrics()

    stale_patterns = [
        (re.compile(r'96\.4(?:3)?%'), f"Stale Gold v1 recall (current: {metrics['v1_recall']}%)"),
        (re.compile(r'189/196'), f"Stale Gold v1 ratio (current: {metrics['v1_recall_ratio']})"),
        (re.compile(r'187/196'), f"Stale Gold v1 ratio (current: {metrics['v1_recall_ratio']})"),
        (re.compile(r'190/196'), f"Stale Gold v1 ratio (current: {metrics['v1_recall_ratio']})"),
        (re.compile(r'173\s+samples'), "Stale Gold v2 sample count (current: 243 samples)"),
        (re.compile(r'35\s+legitimate'), "Stale Gold v2 legitimate count (current: 105 samples)"),
        (re.compile(r'0/35'), f"Stale Gold v2 FPR ratio (current: {metrics['v2_fpr_ratio']})"),
    ]
    if metrics['v2_recall'] != '97.83':
        stale_patterns.append((re.compile(r'97\.8(?:3)?%'), f"Stale Gold v2 recall (current: {metrics['v2_recall']}%)"))

    violations = []
    for rel_path in DEMO_DOCS:
        full_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(full_path):
            continue
        with open(full_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                for pat, msg in stale_patterns:
                    if pat.search(line):
                        violations.append(f"{rel_path}:{line_no} contains '{pat.pattern}': {msg}")

    assert not violations, "Found stale benchmark metrics in demo documents:\n" + "\n".join(violations)

def test_demo_docs_agree_with_evaluation_report():
    """Assert that whenever Gold v1 or Gold v2 recall is quoted in demo docs, it matches EVALUATION_REPORT.md."""
    base_dir = get_base_dir()
    metrics = parse_evaluation_report_metrics()

    target_docs = ["docs/PITCH_OUTLINE.md", "docs/JUDGE_QA.md", "docs/DEMO_RECORDING.md", "docs/FINAL_STATUS.md"]

    patterns = [
        (re.compile(r'Gold\s*v1\s*Scam\s*Recall:\s*\*\*(\d+\.\d+)%\*\*', re.I), metrics["v1_recall"], "Gold v1 recall"),
        (re.compile(r'Gold\s*v2\s*Scam\s*Recall:\s*\*\*(\d+\.\d+)%\*\*', re.I), metrics["v2_recall"], "Gold v2 recall"),
        (re.compile(r'(\d+\.\d+)%\s*recall\s*on\s*frozen\s*benchmarks', re.I), metrics["v1_recall"], "Gold v1 recall"),
        (re.compile(r'(\d+\.\d+)%\s*on\s*messy\s*human\s*wording', re.I), metrics["v2_recall"], "Gold v2 recall"),
        (re.compile(r'\*\*(\d+\.\d+)%\s*Risk\s*Fusion\s*Recall\*\*\s*\(\s*Gold\s*v1', re.I), metrics["v1_recall"], "Gold v1 recall"),
        (re.compile(r'\*\*(\d+\.\d+)%\s*Recall\*\*\s*\(\s*Gold\s*v2', re.I), metrics["v2_recall"], "Gold v2 recall"),
        (re.compile(rf'(\d+\.\d+)%\s*recall\s*\(\s*Gold\s*v1:\s*{re.escape(metrics["v1_recall_ratio"])}\)', re.I), metrics["v1_recall"], "Gold v1 recall"),
        (re.compile(rf'(\d+\.\d+)%\s*\(\s*Gold\s*v2:\s*{re.escape(metrics["v2_recall_ratio"])}\)', re.I), metrics["v2_recall"], "Gold v2 recall"),
        (re.compile(rf'\*\*(\d+\.\d+)%\*\*\s*\({re.escape(metrics["v1_recall_ratio"])}\s*Gold\s*v1\)', re.I), metrics["v1_recall"], "Gold v1 recall"),
        (re.compile(rf'\*\*(\d+\.\d+)%\*\*\s*\({re.escape(metrics["v2_recall_ratio"])}\s*Gold\s*v2\)', re.I), metrics["v2_recall"], "Gold v2 recall"),
        (re.compile(r'\*\*(\d+\.\d+)%\*\*\s*\(0/110\s*on\s*Gold\s*v1\)', re.I), metrics["v1_fpr"], "Gold v1 FPR"),
        (re.compile(rf'\*\*(\d+\.\d+)%\*\*\s*\({re.escape(metrics["v2_fpr_ratio"])}\s*on\s*expanded\s*Gold\s*v2\)', re.I), metrics["v2_fpr"], "Gold v2 FPR"),
        (re.compile(r'\*\*(\d+\.\d+)%\s*False\s*Positive\s*Rate\*\*\s*on\s*Gold\s*v1', re.I), metrics["v1_fpr"], "Gold v1 FPR"),
        (re.compile(r'\*\*(\d+\.\d+)%\s*False\s*Positive\s*Rate\*\*\s*on\s*Gold\s*v2', re.I), metrics["v2_fpr"], "Gold v2 FPR"),
        (re.compile(r'(\d+\.\d+)%\s*on\s*Gold\s*v1\s*\(0/110\)', re.I), metrics["v1_fpr"], "Gold v1 FPR"),
        (re.compile(rf'(\d+\.\d+)%\s*on\s*Gold\s*v2\s*\({re.escape(metrics["v2_fpr_ratio"])}\)', re.I), metrics["v2_fpr"], "Gold v2 FPR"),
    ]

    for rel_path in target_docs:
        full_path = os.path.join(base_dir, rel_path)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        for pat, expected_val, label in patterns:
            for m in pat.finditer(content):
                val = m.group(1)
                assert val == expected_val, (
                    f"{rel_path}: Quoted {label} {val}% disagrees with EVALUATION_REPORT.md ({expected_val}%)"
                )
