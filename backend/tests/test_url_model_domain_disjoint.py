import os
import json
import pytest
import tldextract

def get_registered_domain(url: str) -> str:
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain

def test_url_model_domain_disjoint_split():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    train_domains_path = os.path.join(base_dir, "app", "data", "url_model_train_domains.json")
    test_domains_path = os.path.join(base_dir, "app", "data", "url_model_test_domains.json")
    adv_testset_path = os.path.join(base_dir, "app", "data", "external", "adversarial_url_testset.json")

    assert os.path.exists(train_domains_path), f"Train domains file missing at {train_domains_path}"
    assert os.path.exists(test_domains_path), f"Test domains file missing at {test_domains_path}"
    assert os.path.exists(adv_testset_path), f"Adversarial testset missing at {adv_testset_path}"

    with open(train_domains_path, "r", encoding="utf-8") as f:
        train_domains = set(json.load(f))

    with open(test_domains_path, "r", encoding="utf-8") as f:
        test_domains = set(json.load(f))

    with open(adv_testset_path, "r", encoding="utf-8") as f:
        adv_testset = json.load(f)

    # 1. Assert zero intersection between registered train domains and registered test domains
    overlap = train_domains.intersection(test_domains)
    assert len(overlap) == 0, f"Domain leakage detected! Overlapping domains: {overlap}"

    # 2. Assert that no URL in the independent adversarial testset has a registered domain in train_domains
    adv_overlap = set()
    for item in adv_testset:
        reg = get_registered_domain(item["url"])
        if reg in train_domains:
            adv_overlap.add(reg)

    assert len(adv_overlap) == 0, f"Adversarial test URLs found in train domains! Overlap: {adv_overlap}"
    assert len(train_domains) >= 500, f"Expected at least 500 train domains, got {len(train_domains)}"
    assert len(test_domains) >= 200, f"Expected at least 200 test domains, got {len(test_domains)}"
