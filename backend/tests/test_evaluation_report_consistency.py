import os
import re
import pytest

def test_evaluation_report_exists():
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs", "EVALUATION_REPORT.md")
    assert os.path.exists(report_path), f"Report not found at {report_path}"

def test_evaluation_report_gates_consistency():
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs", "EVALUATION_REPORT.md")
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    def check_gate(op: str, target: float, val: float, status: str, gate_name: str):
        if op == ">=":
            cond = (val >= target)
        elif op == "<=":
            cond = (val <= target)
        elif op == "<":
            cond = (val < target)
        elif op == ">":
            cond = (val > target)
        else:
            raise ValueError(f"Unknown op: {op}")

        if status == "PASSED":
            assert cond, f"Gate '{gate_name}' marked PASSED but value {val} does not satisfy {op} {target}"
        elif status == "FAILED":
            assert not cond, f"Gate '{gate_name}' marked FAILED but value {val} satisfies {op} {target}"

    # Table 1: Dual Gold set gates (columns: Gate Name | Target | Measured v1 | Gate v1 | Measured v2 | Gate v2)
    dual_pattern = re.compile(
        r'\|\s*\*\*([^*]+)\*\*\s*\|\s*([<>=!]+)\s*([0-9.]+)%?\s*\|\s*\*\*([0-9.]+)%?\*\*[^\n|]*\|\s*\*\*([A-Z]+)\*\*\s*\|\s*\*\*([0-9.]+)%?\*\*[^\n|]*\|\s*\*\*([A-Z]+)\*\*\s*\|'
    )
    dual_matches = dual_pattern.findall(content)
    assert len(dual_matches) >= 4, f"Expected at least 4 dual gates, found {len(dual_matches)}"

    for name, op, target_str, v1_str, status_v1, v2_str, status_v2 in dual_matches:
        target = float(target_str)
        v1 = float(v1_str)
        v2 = float(v2_str)
        check_gate(op, target, v1, status_v1, f"{name} (Gold v1)")
        check_gate(op, target, v2, status_v2, f"{name} (Gold v2)")

    # Table 2: URL gates (columns: Gate Name | Target | Measured | Gate Status | Dataset)
    url_pattern = re.compile(
        r'\|\s*\*\*([^*]+)\*\*\s*\|\s*([<>=!]+)\s*([0-9.]+)%?\s*\|\s*\*\*([0-9.]+)%?\*\*[^\n|]*\|\s*\*\*([A-Z]+)\*\*\s*\|\s*([^\n|]+)\|'
    )
    url_matches = url_pattern.findall(content)
    assert len(url_matches) >= 4, f"Expected at least 4 URL gates, found {len(url_matches)}"

    for name, op, target_str, val_str, status, dataset in url_matches:
        target = float(target_str)
        val = float(val_str)
        check_gate(op, target, val, status, f"{name} ({dataset.strip()})")

def test_no_contradictory_metric_values():
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs", "EVALUATION_REPORT.md")
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify that fraction counts for Gold v1 scam recall are consistent throughout the document
    scam_recall_fractions = re.findall(r'(\d+)/196', content)
    if scam_recall_fractions:
        assert len(set(scam_recall_fractions)) == 1, (
            f"Contradictory scam recall counts found for Gold v1: {set(scam_recall_fractions)}"
        )

    # Verify that fraction counts for Gold v1 legitimate FPR are consistent
    leg_fpr_fractions = re.findall(r'(\d+)/110', content)
    if leg_fpr_fractions:
        assert len(set(leg_fpr_fractions)) == 1, (
            f"Contradictory legitimate FPR counts found for Gold v1: {set(leg_fpr_fractions)}"
        )

    # Verify that fraction counts for Gold v2 legitimate FPR are consistent
    leg_v2_fpr_fractions = re.findall(r'(\d+)/105', content)
    if leg_v2_fpr_fractions:
        assert len(set(leg_v2_fpr_fractions)) == 1, (
            f"Contradictory legitimate FPR counts found for Gold v2: {set(leg_v2_fpr_fractions)}"
        )
