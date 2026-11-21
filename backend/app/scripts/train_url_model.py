import os
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

def train_url_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    external_dir = os.path.join(base_dir, "data", "external")
    model_save_path = os.path.join(base_dir, "data", "url_model.pkl")

    openphish_path = os.path.join(external_dir, "openphish_feed.txt")
    benign_path = os.path.join(external_dir, "benign_domains.csv")

    phishing_urls = []
    if os.path.exists(openphish_path):
        with open(openphish_path, "r", encoding="utf-8") as f:
            phishing_urls = [line.strip() for line in f if line.strip() and line.startswith("http")]

    benign_domains = []
    if os.path.exists(benign_path):
        df_b = pd.read_csv(benign_path)
        benign_domains = [f"https://{dom}" for dom in df_b["domain"].dropna().tolist()]

    # Generate synthetic typosquats and attack patterns for Indian brands
    adversarial_phishing = []
    for entity in OFFICIAL_ENTITIES:
        brand = entity["brand"]
        for off in entity["domains"]:
            off_stem = off.split(".")[0]
            adversarial_phishing.append(f"http://{off}.verify-login-update.xyz/auth")
            adversarial_phishing.append(f"https://{off}.security-alert.top/session")
            adversarial_phishing.append(f"http://{brand}-kyc-verification.online/login")
            adversarial_phishing.append(f"https://{brand}-refund-claim.site/portal")
            adversarial_phishing.append(f"http://{off_stem}i.co.in/banking")
            adversarial_phishing.append(f"https://online-{brand}.biz/auth")
            adversarial_phishing.append(f"http://192.168.{random.randint(1,254)}.{random.randint(1,254)}/{brand}/login")
            adversarial_phishing.append(f"http://{brand}-discom-bill.xyz/pay")

    # Add official domains to benign
    official_benign = []
    for entity in OFFICIAL_ENTITIES:
        for dom in entity["domains"]:
            official_benign.append(f"https://{dom}")
            official_benign.append(f"https://retail.{dom}/portal")
            official_benign.append(f"https://corporate.{dom}/netbanking")

    all_phish = list(set(phishing_urls + adversarial_phishing))
    all_benign = list(set(benign_domains + official_benign))

    records = []
    for u in all_phish:
        ext = tldextract.extract(u)
        reg = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
        records.append({"url": u, "label": 1, "domain": reg})

    for u in all_benign:
        ext = tldextract.extract(u)
        reg = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
        records.append({"url": u, "label": 0, "domain": reg})

    df = pd.DataFrame(records).sample(frac=1.0, random_state=42).reset_index(drop=True)
    print(f"URL Training Dataset: {len(df)} samples ({len(all_phish)} phishing, {len(all_benign)} benign).")

    # Domain-disjoint split using GroupShuffleSplit
    gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
    train_idx, val_idx = next(gss.split(df, groups=df["domain"]))

    train_df = df.iloc[train_idx]
    val_df = df.iloc[val_idx]

    char_vec = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=12000,
        sublinear_tf=True
    )
    lexical = URLLexicalFeatures()

    union = FeatureUnion([
        ("char", char_vec),
        ("lexical", lexical)
    ])

    base_lr = LogisticRegression(
        C=2.0,
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

    print("Fitting Calibrated URL Phishing Pipeline...")
    pipeline.fit(train_df["url"], train_df["label"])

    val_preds = pipeline.predict(val_df["url"])
    val_probs = pipeline.predict_proba(val_df["url"])[:, 1]
    acc = accuracy_score(val_df["label"], val_preds)
    report = classification_report(val_df["label"], val_preds, target_names=["Benign", "Phishing"], digits=4)

    print(f"\nValidation (Domain-Disjoint) Accuracy: {acc * 100:.2f}%")
    print("Validation Classification Report:\n", report)

    # Save model
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump(pipeline, model_save_path)
    print(f"\nSaved trained static URL model to {model_save_path}")

if __name__ == "__main__":
    train_url_model()
