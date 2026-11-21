import os
import math
import re
import joblib
import numpy as np
import tldextract
from typing import List, Dict, Any
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV

FREE_HOSTING_DOMAINS = {
    "pages.dev", "vercel.app", "blogspot.com", "weebly.com", "firebaseapp.com",
    "000webhostapp.com", "glitch.me", "netlify.app", "surge.sh", "github.io",
    "wixsite.com", "flazio.com", "godaddysites.com", "webflow.io"
}

SUSPICIOUS_TLD_SET = {
    "xyz", "top", "online", "site", "club", "biz", "info", "work", "link",
    "live", "vip", "tk", "ml", "ga", "cf", "gq", "rest", "fit", "buzz"
}

SECURITY_KEYWORDS = [
    "login", "verify", "kyc", "account", "bank", "update", "auth", "secure",
    "wallet", "claim", "bonus", "bill", "refund", "support", "alert", "confirm",
    "free", "gift", "service", "portal", "security", "customer", "admin"
]

def shannon_entropy(text: str) -> float:
    if not text:
        return 0.0
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1
    ent = 0.0
    for count in freq.values():
        p = count / len(text)
        ent -= p * math.log2(p)
    return ent

class URLLexicalFeatures(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        features = []
        for url in X:
            url_str = str(url).lower()
            ext = tldextract.extract(url_str)
            domain = ext.domain
            suffix = ext.suffix
            subdomain = ext.subdomain
            registered = f"{domain}.{suffix}" if suffix else domain

            url_len = len(url_str)
            host_len = len(registered)
            sub_count = len([p for p in subdomain.split(".") if p]) if subdomain else 0
            hyphen_count = url_str.count("-")
            digit_count = len(re.findall(r'\d', url_str))
            slash_count = url_str.count("/")
            dot_count = url_str.count(".")

            digit_ratio = digit_count / max(1, url_len)
            is_free_host = 1.0 if registered in FREE_HOSTING_DOMAINS else 0.0
            is_susp_tld = 1.0 if suffix in SUSPICIOUS_TLD_SET else 0.0
            kw_count = sum(1.0 for kw in SECURITY_KEYWORDS if kw in url_str)
            entropy = shannon_entropy(domain)
            has_ip = 1.0 if re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', url_str) else 0.0
            has_at = 1.0 if "@" in url_str else 0.0

            features.append([
                url_len / 100.0,
                host_len / 30.0,
                sub_count / 5.0,
                hyphen_count / 5.0,
                digit_ratio,
                slash_count / 10.0,
                dot_count / 5.0,
                is_free_host,
                is_susp_tld,
                kw_count / 3.0,
                entropy / 5.0,
                has_ip,
                has_at
            ])
        return np.array(features)

class TrainedURLClassifier:
    """
    Lightweight, purely static ML model for URL phishing detection.
    Evaluates character n-grams and lexical structure with zero network calls.
    """
    def __init__(self):
        self.model: Any = None
        self._load_model()

    def _load_model(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "data", "url_model.pkl")
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
            except Exception:
                self.model = None

    def predict_phishing_probability(self, url: str) -> float:
        if self.model is None:
            self._load_model()
        if self.model is None:
            return 0.0
        try:
            prob = self.model.predict_proba([url])[0][1]
            return float(prob)
        except Exception:
            return 0.0

url_classifier_model = TrainedURLClassifier()
