import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.base import BaseEstimator, ClassifierMixin

class HierarchicalScamClassifier(BaseEstimator, ClassifierMixin):
    """
    Hierarchical Two-Stage Classifier for Scam Detection and Attribution:
      Stage 1: Calibrated Binary Classifier (Legitimate vs Scam)
      Stage 2: 14-Class Scam Categorizer (Only invoked for confirmed scam patterns)
    Exposes standard scikit-learn API: fit, predict, predict_proba, classes_.
    """
    def __init__(self, binary_pipeline=None, scam_pipeline=None, binary_threshold: float = 0.58):
        self.binary_pipeline = binary_pipeline
        self.scam_pipeline = scam_pipeline
        self.binary_threshold = binary_threshold
        self.classes_ = None
        self.scam_classes_ = None

    def fit(self, X, y):
        y_arr = np.array(y)
        all_classes = sorted(list(set(y_arr)))
        self.classes_ = np.array(all_classes)

        # Stage 1: Binary targets (0: legitimate, 1: scam)
        is_scam = (y_arr != "legitimate").astype(int)
        print(f"  [Stage 1] Fitting Binary Classifier on {len(X)} samples (Scam: {is_scam.sum()}, Legit: {(is_scam == 0).sum()})...")
        self.binary_pipeline.fit(X, is_scam)

        # Stage 2: Scam-only attribution (14 classes)
        scam_mask = (is_scam == 1)
        X_scams = [X.iloc[i] if hasattr(X, "iloc") else X[i] for i in range(len(X)) if scam_mask[i]]
        y_scams = y_arr[scam_mask]
        self.scam_classes_ = np.array(sorted(list(set(y_scams))))

        print(f"  [Stage 2] Fitting 14-Class Scam Attribution on {len(X_scams)} samples across {len(self.scam_classes_)} categories...")
        self.scam_pipeline.fit(X_scams, y_scams)

        return self

    def predict_proba(self, X):
        # Stage 1 probabilities: shape (N, 2)
        p_bin = self.binary_pipeline.predict_proba(X)
        p_legit = p_bin[:, 0]
        p_scam = p_bin[:, 1]

        # Stage 2 probabilities: shape (N, 14)
        p_scams = self.scam_pipeline.predict_proba(X)

        n_samples = len(X)
        all_classes_list = list(self.classes_)
        scam_classes_list = list(self.scam_classes_)

        full_probs = np.zeros((n_samples, len(all_classes_list)))

        for j, cls_name in enumerate(all_classes_list):
            if cls_name == "legitimate":
                # For legitimate, reflect Stage 1 decision boundary
                full_probs[:, j] = p_legit
            else:
                scam_idx = scam_classes_list.index(cls_name)
                # Joint probability P(Scam) * P(Category | Scam)
                full_probs[:, j] = p_scam * p_scams[:, scam_idx]

        # Boost legitimate if p_scam < binary_threshold
        for i in range(n_samples):
            if p_scam[i] < self.binary_threshold:
                legit_col = all_classes_list.index("legitimate")
                # Ensure legitimate has the highest probability
                full_probs[i, legit_col] = max(full_probs[i, legit_col], 0.55)

        # Normalize rows to sum to 1.0
        row_sums = full_probs.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        full_probs = full_probs / row_sums

        return full_probs

    def predict(self, X):
        p_bin = self.binary_pipeline.predict_proba(X)
        p_scam = p_bin[:, 1]
        is_scam_pred = (p_scam >= self.binary_threshold)

        preds = np.array(["legitimate"] * len(X), dtype=object)
        if is_scam_pred.sum() > 0:
            scam_indices = np.where(is_scam_pred)[0]
            X_scams = [X.iloc[i] if hasattr(X, "iloc") else X[i] for i in scam_indices]
            scam_preds = self.scam_pipeline.predict(X_scams)
            preds[scam_indices] = scam_preds

        return preds
