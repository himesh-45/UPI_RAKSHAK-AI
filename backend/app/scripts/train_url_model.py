import os
import json
import random
import joblib
import pandas as pd
import numpy as np
import tldextract
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, accuracy_score

from backend.app.detectors.url_classifier_model import URLLexicalFeatures
from backend.app.detectors.url_scanner import OFFICIAL_ENTITIES, SUSPICIOUS_TLDS

def get_registered_domain(url: str) -> str:
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain

def train_url_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    external_dir = os.path.join(base_dir, "data", "external")
    model_save_path = os.path.join(base_dir, "data", "url_model.pkl")
    train_domains_path = os.path.join(base_dir, "data", "url_model_train_domains.json")
    test_domains_path = os.path.join(base_dir, "data", "url_model_test_domains.json")

    openphish_path = os.path.join(external_dir, "openphish_feed.txt")
    benign_path = os.path.join(external_dir, "benign_domains.csv")
    adversarial_testset_path = os.path.join(external_dir, "adversarial_url_testset.json")

    # 1. Load OpenPhish feed (chronological order: first 200 train, last 100 holdout test)
    phishing_urls = []
    if os.path.exists(openphish_path):
        with open(openphish_path, "r", encoding="utf-8") as f:
            phishing_urls = [line.strip() for line in f if line.strip() and line.startswith("http")]

    # Holdout last 100 OpenPhish URLs as chronological holdout test
    openphish_train = phishing_urls[:200]
    openphish_holdout_test = phishing_urls[200:]

    # 2. Load Benign domains (first 750 train, last 250 holdout test)
    benign_domains = []
    if os.path.exists(benign_path):
        df_b = pd.read_csv(benign_path)
        benign_domains = [f"https://{dom}" for dom in df_b["domain"].dropna().tolist()]

    benign_train = benign_domains[:750]
    benign_test = benign_domains[750:]

    # 3. Load independent adversarial testset to explicitly protect its domains from training
    protected_test_domains = set()
    if os.path.exists(adversarial_testset_path):
        with open(adversarial_testset_path, "r", encoding="utf-8") as f:
            adv_testset = json.load(f)
            for item in adv_testset:
                protected_test_domains.add(get_registered_domain(item["url"]))

    for u in openphish_holdout_test:
        protected_test_domains.add(get_registered_domain(u))

    for u in benign_test:
        protected_test_domains.add(get_registered_domain(u))

    print(f"Total protected test domains to strictly exclude from training: {len(protected_test_domains)}")

    # 4. Generate training synthetic phishing URLs (excluding any protected test domain)
    training_phishing = list(openphish_train)
    training_benign = list(benign_train)

    # Add official domains to training benign ONLY if not in protected test domains
    for entity in OFFICIAL_ENTITIES:
        for dom in entity["domains"]:
            reg = get_registered_domain(dom)
            if reg not in protected_test_domains:
                training_benign.append(f"https://{dom}")
                training_benign.append(f"https://retail.{dom}/portal")
                training_benign.append(f"https://corporate.{dom}/netbanking")

    # Add training synthetic patterns
    random.seed(42)
    for entity in OFFICIAL_ENTITIES:
        brand = entity["brand"]
        for off in entity["domains"]:
            reg_off = get_registered_domain(off)
            tld = "xyz" if "xyz" not in protected_test_domains else "top"
            cand_urls = [
                f"http://{off}.verify-login-update.xyz/auth",
                f"https://{off}.security-alert.top/session",
                f"http://{brand}-kyc-verification.online/login",
                f"https://{brand}-refund-claim.site/portal",
                f"http://online-{brand}.biz/auth",
                f"http://192.168.{random.randint(1,254)}.{random.randint(1,254)}/{brand}/login",
                f"http://{brand}-discom-bill.xyz/pay"
            ]
            for u in cand_urls:
                if get_registered_domain(u) not in protected_test_domains:
                    training_phishing.append(u)

    # 5. Build Training Records with strict domain tagging
    records = []
    train_domain_set = set()

    for u in training_phishing:
        reg = get_registered_domain(u)
        if reg not in protected_test_domains:
            records.append({"url": u, "label": 1, "domain": reg})
            train_domain_set.add(reg)

    for u in training_benign:
        reg = get_registered_domain(u)
        if reg not in protected_test_domains:
            records.append({"url": u, "label": 0, "domain": reg})
            train_domain_set.add(reg)

    df_train = pd.DataFrame(records).sample(frac=1.0, random_state=42).reset_index(drop=True)

    # Double check strict disjointness
    overlap = train_domain_set.intersection(protected_test_domains)
    assert len(overlap) == 0, f"LEAKAGE DETECTED! Overlapping domains: {overlap}"
    print(f"Domain-Disjoint verification passed: 0 overlapping domains between train and test!")
    print(f"URL Training Dataset: {len(df_train)} samples across {len(train_domain_set)} unique registered domains.")

    # 6. Train FeatureUnion + Calibrated Classifier
    char_vec = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=15000,
        sublinear_tf=True
    )
    lexical = URLLexicalFeatures()

    union = FeatureUnion([
        ("char", char_vec),
        ("lexical", lexical)
    ])

    base_lr = LogisticRegression(
        C=2.5,
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )

    clf = CalibratedClassifierCV(
        estimator=base_lr,
        method="sigmoid",
        cv=3
    )

    pipeline = Pipeline([
        ("features", union),
        ("clf", clf)
    ])

    print("Fitting Calibrated URL Phishing Pipeline on domain-disjoint training set...")
    pipeline.fit(df_train["url"], df_train["label"])

    # 7. Evaluate on holdout OpenPhish test + Benign test
    holdout_phish_eval = [u for u in openphish_holdout_test if get_registered_domain(u) in protected_test_domains]
    holdout_benign_eval = [u for u in benign_test if get_registered_domain(u) in protected_test_domains]

    eval_urls = holdout_phish_eval + holdout_benign_eval
    eval_labels = [1] * len(holdout_phish_eval) + [0] * len(holdout_benign_eval)

    preds = pipeline.predict(eval_urls)
    acc = accuracy_score(eval_labels, preds)
    rep = classification_report(eval_labels, preds, target_names=["Benign", "Phishing"], digits=4)
    print(f"\nDisjoint Holdout Test Accuracy: {acc * 100:.2f}%")
    print(rep)

    # 8. Save Model and Domain lists
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump(pipeline, model_save_path)
    print(f"Saved trained static URL model to {model_save_path}")

    with open(train_domains_path, "w", encoding="utf-8") as f:
        json.dump(sorted(list(train_domain_set)), f, indent=2)

    with open(test_domains_path, "w", encoding="utf-8") as f:
        json.dump(sorted(list(protected_test_domains)), f, indent=2)

    print(f"Saved {len(train_domain_set)} training domains and {len(protected_test_domains)} test domains.")

if __name__ == "__main__":
    train_url_model()
