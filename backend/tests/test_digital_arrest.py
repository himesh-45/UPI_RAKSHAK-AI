import json
import os
import pytest
from backend.app.detectors.digital_arrest_checker import digital_arrest_checker

TESTSET_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "app", "data", "digital_arrest_testset.json"
)

@pytest.fixture(scope="module")
def digital_arrest_data():
    with open(TESTSET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def test_digital_arrest_benchmark_recall_and_fpr(digital_arrest_data):
    """
    Evaluates DigitalArrestChecker on the frozen 102-sample benchmark set
    (65 scams, 37 legitimate).
    Quality Gates:
    - Scam Recall >= 95.0%
    - Legitimate FPR <= 3.0%
    """
    scams = [item for item in digital_arrest_data if item["is_scam"]]
    legit = [item for item in digital_arrest_data if not item["is_scam"]]

    scams_flagged = 0
    scam_failures = []
    for s in scams:
        res = digital_arrest_checker.evaluate(s["text"])
        if res["is_digital_arrest"]:
            scams_flagged += 1
        else:
            scam_failures.append((s["id"], s["lang"], s["text"][:80]))

    scam_recall = (scams_flagged / len(scams)) * 100.0

    legit_flagged = 0
    legit_failures = []
    for l in legit:
        res = digital_arrest_checker.evaluate(l["text"])
        if res["is_digital_arrest"]:
            legit_flagged += 1
            legit_failures.append((l["id"], l["lang"], l["text"][:80]))

    legit_fpr = (legit_flagged / len(legit)) * 100.0

    print(f"\n--- Digital Arrest Benchmark Results ---")
    print(f"Scam Recall:    {scams_flagged}/{len(scams)} ({scam_recall:.2f}%) [Gate: >= 95.0%]")
    print(f"Legitimate FPR: {legit_flagged}/{len(legit)} ({legit_fpr:.2f}%) [Gate: <= 3.0%]")

    if scam_failures:
        print(f"Missed Scams ({len(scam_failures)}): {scam_failures[:5]}")
    if legit_failures:
        print(f"False Alarms ({len(legit_failures)}): {legit_failures}")

    assert scam_recall >= 95.0, f"Scam recall {scam_recall:.2f}% below 95% target"
    assert legit_fpr <= 3.0, f"Legitimate false positive rate {legit_fpr:.2f}% exceeds 3% target"

def test_tactic_extraction_and_legal_truth():
    script = (
        "This is Inspector Sharma from Central Bureau of Investigation (CBI). "
        "A FedEx parcel with 200g of MDMA drugs was seized at Mumbai airport. "
        "You are placed under digital arrest. Stay on this Skype video call and transfer "
        "verification deposit to RBI escrow account."
    )
    res = digital_arrest_checker.evaluate(script)
    assert res["is_digital_arrest"] is True
    assert res["severity"] == "CRITICAL"
    assert res["tactic_count"] >= 3
    assert any("Impersonation" in t for t in res["coercion_tactics"])
    assert any("Contraband" in t for t in res["coercion_tactics"])
    assert any("Confinement" in t for t in res["coercion_tactics"])
    assert "CrPC" in res["legal_truth"] or "Indian Law" in res["legal_truth"]
    assert len(res["emergency_advice"]) >= 3

def test_awareness_and_negation_handling():
    awareness_text = (
        "Delhi Police Public Safety Notice: Beware of digital arrest scam calls! "
        "Cyber criminals posing as CBI or police threaten video arrest. Real law enforcement "
        "never conducts arrests over Skype or WhatsApp. Call helpline 1930 immediately."
    )
    res = digital_arrest_checker.evaluate(awareness_text)
    assert res["is_digital_arrest"] is False
    assert res["severity"] != "CRITICAL"
    assert "awareness" in res["coercion_tactics"][0].lower() or res["tactic_count"] == 0

def test_multilingual_hindi_and_telugu_recall():
    hindi_scam = "सीबीआई मुख्यालय: मनी लॉन्ड्रिंग के मामले में आपके खिलाफ गैर-जमानती गिरफ्तारी वारंट है। तुरंत स्काइप वीडियो कॉल चालू करें।"
    h_res = digital_arrest_checker.evaluate(hindi_scam)
    assert h_res["is_digital_arrest"] is True
    assert h_res["severity"] in ["CRITICAL", "HIGH"]

    telugu_scam = "ఇది ముంబై క్రైమ్ బ్రాంచ్. మీ ఫెడెక్స్ పార్శిల్ లో ఎండీఎంఏ డ్రగ్స్ దొరికాయి. మిమ్మల్ని డిజిటల్ అరెస్ట్ చేస్తున్నాము. స్కైప్ లోనే ఉండండి."
    t_res = digital_arrest_checker.evaluate(telugu_scam)
    assert t_res["is_digital_arrest"] is True
    assert t_res["severity"] in ["CRITICAL", "HIGH"]
