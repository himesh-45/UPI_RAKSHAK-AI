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

    # Find the table in Section 1
    table_pattern = re.compile(
        r'\|\s*\*\*([^*]+)\*\*\s*\|\s*([<>=!]+)\s*([0-9.]+)%?\s*\|\s*\*\*([0-9.]+)%?\*\*[^\n|]*\|\s*(?:[^\n|]*)\|\s*\*\*([A-Z]+)\*\*\s*\|'
    )

    matches = table_pattern.findall(content)
    assert len(matches) >= 5, f"Expected at least 5 programmatic quality gates, found {len(matches)}"

    for name, op, target_str, value_str, status in matches:
        target = float(target_str)
        value = float(value_str)

        # Check gate validity
        if op == ">=":
            condition_met = (value >= target)
        elif op == "<=":
            condition_met = (value <= target)
        elif op == "<":
            condition_met = (value < target)
        elif op == ">":
            condition_met = (value > target)
        else:
            raise ValueError(f"Unknown operator {op} for gate {name}")

        if status == "PASSED":
            assert condition_met, f"Gate '{name}' marked PASSED but value {value} does not satisfy {op} {target}"
        elif status == "FAILED":
            assert not condition_met, f"Gate '{name}' marked FAILED but value {value} satisfies {op} {target}"

def test_no_contradictory_metric_values():
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "docs", "EVALUATION_REPORT.md")
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify that fraction counts for Gold v1 scam recall are consistent throughout the document
    scam_recall_fractions = re.findall(r'(\d+)/196', content)
    if scam_recall_fractions:
        # All occurrences of X/196 must be identical
        assert len(set(scam_recall_fractions)) == 1, (
            f"Contradictory scam recall counts found for Gold v1: {set(scam_recall_fractions)}"
        )

    # Verify that fraction counts for Gold v1 legitimate FPR are consistent
    leg_fpr_fractions = re.findall(r'(\d+)/110', content)
    if leg_fpr_fractions:
        assert len(set(leg_fpr_fractions)) == 1, (
            f"Contradictory legitimate FPR counts found for Gold v1: {set(leg_fpr_fractions)}"
        )

    # Verify that Tranco domain counts are consistent
    tranco_counts = re.findall(r'(\d+)\s+Tranco', content)
    if tranco_counts:
        assert len(set(tranco_counts)) == 1, (
            f"Contradictory Tranco benign URL counts found: {set(tranco_counts)}"
        )
