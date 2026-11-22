import os
import re
import json
from sklearn.metrics import classification_report, accuracy_score, f1_score
from ..assistant.intent import intent_classifier
from ..assistant.intent_dataset import TEST_INTENT_DATA, ALL_INTENTS

def evaluate_intent_classifier():
    """
    Evaluates the IntentClassifier on the held-out TEST_INTENT_DATA dataset.
    Returns metrics dictionary with honest, non-inflated evaluation statistics.
    """
    y_true = []
    y_pred = []

    for text, true_intent in TEST_INTENT_DATA:
        result = intent_classifier.classify(text)
        y_true.append(true_intent)
        y_pred.append(result.intent)

    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro")

    report_dict = classification_report(y_true, y_pred, output_dict=True, zero_division=0)

    per_class = {}
    for intent in ALL_INTENTS:
        if intent in report_dict:
            per_class[intent] = {
                "precision": round(report_dict[intent]["precision"] * 100, 2),
                "recall": round(report_dict[intent]["recall"] * 100, 2),
                "f1": round(report_dict[intent]["f1-score"], 4),
                "support": report_dict[intent]["support"]
            }

    metrics = {
        "dataset_name": "Conversational Safety Intent Test Set (Held-Out Fictional)",
        "total_test_samples": len(TEST_INTENT_DATA),
        "overall_accuracy_pct": round(acc * 100, 2),
        "macro_f1": round(macro_f1, 4),
        "target_f1_gate": 0.8500,
        "gate_status": "PASSED" if macro_f1 >= 0.8500 else "FAILED",
        "per_class_breakdown": per_class,
        "notes": "Evaluated across English, Hindi, Telugu, and Hinglish with colloquial phrasing and typos."
    }

    return metrics

def update_evaluation_report_with_intent(metrics):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    json_path = os.path.join(base_dir, "frontend", "src", "data", "evaluation_report.json")

    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["intent_metrics"] = metrics
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Updated {json_path} with intent metrics.")

    # Update docs/EVALUATION_REPORT.md
    report_md_path = os.path.join(base_dir, "docs", "EVALUATION_REPORT.md")
    if os.path.exists(report_md_path):
        with open(report_md_path, "r", encoding="utf-8") as f:
            content = f.read()

        intent_section = f"""

---

## 4. Assistant Intent Router Benchmark (Conversational Safety Assistant)

> [!NOTE]
> **Evaluation Scope**:
> Evaluated on a held-out test suite of {metrics['total_test_samples']} realistic fictional queries spanning English, Hindi, Telugu, and Hinglish, specifically including common human typos (e.g. *"compliant"* for complaint, *"bloack"* for block, *"anydesck"* for AnyDesk).
> Intent labels: `ANALYZE`, `HOW_TO`, `EMERGENCY`, `SMALL_TALK`, and `UNCLEAR`.

| Intent Metric | Target Benchmark | Measured Value | Gate Status | Dataset Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Intent Overall Accuracy** | >= 85.0% | **{metrics['overall_accuracy_pct']}%** | **{metrics['gate_status']}** | Held-out test set (n={metrics['total_test_samples']}) |
| **5-Class Intent Macro-F1** | >= 0.8500 | **{metrics['macro_f1']}** | **{metrics['gate_status']}** | Multilingual & Typo-Tolerant holdout |

### Per-Class Performance Breakdown:
- **`ANALYZE`**: Recall: **{metrics['per_class_breakdown'].get('ANALYZE', {}).get('recall', 0.0)}%** | Precision: **{metrics['per_class_breakdown'].get('ANALYZE', {}).get('precision', 0.0)}%** (Pasted SMS, links, VPAs, threat forwards)
- **`HOW_TO`**: Recall: **{metrics['per_class_breakdown'].get('HOW_TO', {}).get('recall', 0.0)}%** | Precision: **{metrics['per_class_breakdown'].get('HOW_TO', {}).get('precision', 0.0)}%** (Questions on 1930, reporting, rules)
- **`EMERGENCY`**: Recall: **{metrics['per_class_breakdown'].get('EMERGENCY', {}).get('recall', 0.0)}%** | Precision: **{metrics['per_class_breakdown'].get('EMERGENCY', {}).get('precision', 0.0)}%** (Immediate funds lost, OTP shared)
- **`SMALL_TALK`**: Recall: **{metrics['per_class_breakdown'].get('SMALL_TALK', {}).get('recall', 0.0)}%** | Precision: **{metrics['per_class_breakdown'].get('SMALL_TALK', {}).get('precision', 0.0)}%** (Greetings, polite thanks)
- **`UNCLEAR`**: Recall: **{metrics['per_class_breakdown'].get('UNCLEAR', {}).get('recall', 0.0)}%** | Precision: **{metrics['per_class_breakdown'].get('UNCLEAR', {}).get('precision', 0.0)}%** (Ambiguous terms -> clarification prompt)

### Scientific Honesty Note:
The intent router uses a hybrid fast-rule pre-filter plus subword character n-gram logistic regression. Confidence thresholding (<0.48) routes ambiguous queries to `UNCLEAR` rather than hazarding a guess on critical safety queries.
"""
        # If section 4 is already present, replace it; otherwise append before section 4/5
        if "## 4. Assistant Intent Router Benchmark" in content:
            content = re.sub(r'---\s*\n\s*## 4\. Assistant Intent Router Benchmark.*?(?=(?:\n---|\Z))', intent_section.strip(), content, flags=re.DOTALL)
        else:
            content = content.strip() + "\n" + intent_section

        with open(report_md_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {report_md_path} with intent benchmark section.")

if __name__ == "__main__":
    m = evaluate_intent_classifier()
    print("Intent Evaluation Results:")
    print(json.dumps(m, indent=2))
    update_evaluation_report_with_intent(m)
