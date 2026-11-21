import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import label_binarize

from backend.app.core.normalizer import text_normalizer
from backend.app.core.feature_extractor import EngineeredTextFeatures
from backend.app.core.hierarchical_classifier import HierarchicalScamClassifier

def compute_multiclass_brier(y_true, y_prob, classes: List[str]) -> float:
    y_onehot = label_binarize(y_true, classes=classes)
    return float(np.mean(np.sum((y_prob - y_onehot) ** 2, axis=1)))

def compute_multiclass_ece(y_true, y_prob, classes: List[str], n_bins: int = 10) -> float:
    class_map = {cls: idx for idx, cls in enumerate(classes)}
    y_true_indices = np.array([class_map[y] for y in y_true])
    confidences = np.max(y_prob, axis=1)
    predictions = np.argmax(y_prob, axis=1)
    accuracies = (predictions == y_true_indices)

    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        in_bin = (confidences > bin_boundaries[i]) & (confidences <= bin_boundaries[i + 1])
        prop_in_bin = np.mean(in_bin)
        if prop_in_bin > 0:
            accuracy_in_bin = np.mean(accuracies[in_bin])
            avg_confidence_in_bin = np.mean(confidences[in_bin])
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
    return float(ece)

def build_feature_union():
    word_vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        min_df=2,
        max_features=18000,
        sublinear_tf=True
    )
    char_vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=25000,
        sublinear_tf=True
    )
    eng_features = EngineeredTextFeatures()

    return FeatureUnion([
        ("word", word_vectorizer),
        ("char", char_vectorizer),
        ("domain", eng_features)
    ])

def train_and_evaluate():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "synthetic_scam_dataset.csv")
    gold_v1_path = os.path.join(base_dir, "data", "gold_v1.json")
    gold_v2_path = os.path.join(base_dir, "data", "gold_v2.json")
    model_save_path = os.path.join(base_dir, "data", "nlp_scam_model.pkl")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run generate_dataset.py first.")

    print("=" * 65)
    print("  UPI RAKSHAK AI — HIERARCHICAL NLP MODEL TRAINING")
    print("=" * 65)

    df = pd.read_csv(data_path)
    df["norm_text"] = df["text"].apply(text_normalizer.normalize)
    df = df.drop_duplicates(subset=["norm_text", "category"]).reset_index(drop=True)
    print(f"Corpus size after normalization & deduplication: {len(df)} samples.")

    X = df["norm_text"].astype(str)
    y = df["category"]

    # Stratified Group Split by template_id within each category
    train_indices = []
    val_indices = []
    rng = np.random.RandomState(42)

    for cat in sorted(df["category"].unique()):
        cat_df = df[df["category"] == cat]
        unique_templates = list(cat_df["template_id"].unique())
        rng.shuffle(unique_templates)

        if len(unique_templates) > 1:
            split_pt = max(1, int(len(unique_templates) * 0.80))
            train_tpls = set(unique_templates[:split_pt])
            val_tpls = set(unique_templates[split_pt:])
            if not val_tpls:
                val_tpls = {unique_templates[-1]}
                train_tpls.remove(unique_templates[-1])
        else:
            train_tpls = set(unique_templates)
            val_tpls = set(unique_templates)

        train_indices.extend(cat_df[cat_df["template_id"].isin(train_tpls)].index)
        val_indices.extend(cat_df[cat_df["template_id"].isin(val_tpls)].index)

    X_train, X_val = X.iloc[train_indices].reset_index(drop=True), X.iloc[val_indices].reset_index(drop=True)
    y_train, y_val = y.iloc[train_indices].reset_index(drop=True), y.iloc[val_indices].reset_index(drop=True)

    print(f"Stratified Group Split: {len(X_train)} train samples, {len(X_val)} validation samples.")

    # Test Flat Calibrated Pipeline vs Hierarchical
    flat_clf = CalibratedClassifierCV(
        estimator=LogisticRegression(
            C=3.0,
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        ),
        method="sigmoid",
        cv=3
    )
    flat_pipeline = Pipeline([
        ("features", build_feature_union()),
        ("clf", flat_clf)
    ])

    print("\nFitting Flat Calibrated NLP Pipeline...")
    flat_pipeline.fit(X_train, y_train)

    print("\n[Flat Model Validation Evaluation]")
    val_preds = flat_pipeline.predict(X_val)
    val_probs = flat_pipeline.predict_proba(X_val)
    classes = list(flat_pipeline.classes_)

    val_acc = accuracy_score(y_val, val_preds)
    val_report = classification_report(y_val, val_preds, digits=4, zero_division=0)
    print(f"  Validation Accuracy:    {val_acc * 100:.2f}%")
    print("\nValidation Classification Report:\n", val_report)

    # Load Gold v1
    with open(gold_v1_path, "r", encoding="utf-8") as f:
        gold_v1_data = json.load(f)
    g1_df = pd.DataFrame(gold_v1_data)
    g1_df["norm_text"] = g1_df["text"].apply(text_normalizer.normalize)
    g1_X = g1_df["norm_text"]
    g1_y = g1_df["category"]

    # Load Gold v2
    with open(gold_v2_path, "r", encoding="utf-8") as f:
        gold_v2_data = json.load(f)
    g2_df = pd.DataFrame(gold_v2_data)
    g2_df["norm_text"] = g2_df["text"].apply(text_normalizer.normalize)
    g2_X = g2_df["norm_text"]
    g2_y = g2_df["category"]

    # Evaluate Flat on Gold v1
    g1_preds = flat_pipeline.predict(g1_X)
    g1_probs = flat_pipeline.predict_proba(g1_X)
    g1_report_dict = classification_report(g1_y, g1_preds, output_dict=True, zero_division=0)
    g1_macro_f1 = g1_report_dict["macro avg"]["f1-score"]
    g1_ece = compute_multiclass_ece(g1_y, g1_probs, classes)

    g1_is_scam = (g1_y != "legitimate").astype(int)
    g1_pred_scam = (pd.Series(g1_preds) != "legitimate").astype(int)
    tp1 = int(((g1_is_scam == 1) & (g1_pred_scam == 1)).sum())
    fn1 = int(((g1_is_scam == 1) & (g1_pred_scam == 0)).sum())
    tn1 = int(((g1_is_scam == 0) & (g1_pred_scam == 0)).sum())
    fp1 = int(((g1_is_scam == 0) & (g1_pred_scam == 1)).sum())
    recall1 = tp1 / (tp1 + fn1) if (tp1 + fn1) > 0 else 0.0
    fpr1 = fp1 / (fp1 + tn1) if (fp1 + tn1) > 0 else 0.0

    print("\n" + "=" * 65)
    print("  FLAT MODEL ON FROZEN GOLD SET v1")
    print("=" * 65)
    print(f"  Gold v1 15-Class Macro-F1: {g1_macro_f1:.4f}")
    print(f"  Gold v1 Binary Scam Recall: {recall1 * 100:.2f}% ({tp1}/{tp1 + fn1})")
    print(f"  Gold v1 Legitimate FPR:    {fpr1 * 100:.2f}% ({fp1}/{fp1 + tn1})")
    print(f"  Gold v1 ECE:               {g1_ece:.4f}")
    print("\nGold v1 Classification Report:\n", classification_report(g1_y, g1_preds, digits=4, zero_division=0))

    # Evaluate Flat on Gold v2
    g2_preds = flat_pipeline.predict(g2_X)
    g2_probs = flat_pipeline.predict_proba(g2_X)
    g2_report_dict = classification_report(g2_y, g2_preds, output_dict=True, zero_division=0)
    g2_macro_f1 = g2_report_dict["macro avg"]["f1-score"]
    g2_ece = compute_multiclass_ece(g2_y, g2_probs, classes)

    g2_is_scam = (g2_y != "legitimate").astype(int)
    g2_pred_scam = (pd.Series(g2_preds) != "legitimate").astype(int)
    tp2 = int(((g2_is_scam == 1) & (g2_pred_scam == 1)).sum())
    fn2 = int(((g2_is_scam == 1) & (g2_pred_scam == 0)).sum())
    tn2 = int(((g2_is_scam == 0) & (g2_pred_scam == 0)).sum())
    fp2 = int(((g2_is_scam == 0) & (g2_pred_scam == 1)).sum())
    recall2 = tp2 / (tp2 + fn2) if (tp2 + fn2) > 0 else 0.0
    fpr2 = fp2 / (fp2 + tn2) if (fp2 + tn2) > 0 else 0.0

    print("\n" + "=" * 65)
    print("  FLAT MODEL ON NEW GOLD SET v2")
    print("=" * 65)
    print(f"  Gold v2 15-Class Macro-F1: {g2_macro_f1:.4f}")
    print(f"  Gold v2 Binary Scam Recall: {recall2 * 100:.2f}% ({tp2}/{tp2 + fn2})")
    print(f"  Gold v2 Legitimate FPR:    {fpr2 * 100:.2f}% ({fp2}/{fp2 + tn2})")
    print(f"  Gold v2 ECE:               {g2_ece:.4f}")
    print("\nGold v2 Classification Report:\n", classification_report(g2_y, g2_preds, digits=4, zero_division=0))

    # Save flat pipeline
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump(flat_pipeline, model_save_path)
    print(f"\nSuccessfully saved trained Flat Calibrated Model to {model_save_path}")

if __name__ == "__main__":
    train_and_evaluate()
