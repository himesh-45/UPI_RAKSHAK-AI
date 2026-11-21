import os
import re
import joblib
from typing import Dict, Any, Tuple

# Unicode script ranges
DEVANAGARI_REGEX = re.compile(r'[\u0900-\u097F]')
TELUGU_REGEX = re.compile(r'[\u0C00-\u0C7F]')

# Romanized keyword sets
HINGLISH_KEYWORDS = {
    "aapka", "kare", "karo", "turant", "paise", "aaya", "hoga", "rupaye",
    "band", "khata", "bheje", "dekh", "liye", "batao", "bijli", "gaya"
}
ROMAN_TELUGU_KEYWORDS = {
    "meeku", "cheyandi", "vachindi", "dabbulu", "kinda", "chudandi",
    "aagadaniki", "lekapothe", "undalante", "kottandi", "ravali", "chesukondi"
}

class NLPClassifier:
    def __init__(self, model_path: str = None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, "data", "nlp_scam_model.pkl")
        
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception as e:
                print(f"[Warning] Failed to load NLP model from {self.model_path}: {e}")
                self.model = None
        else:
            print(f"[Warning] Model file not found at {self.model_path}")

    def detect_language(self, text: str) -> str:
        """
        Detects primary language: en, hi, te (including Hinglish and Romanized Telugu).
        """
        if not text:
            return "en"

        # Check native scripts first
        devanagari_count = len(DEVANAGARI_REGEX.findall(text))
        telugu_count = len(TELUGU_REGEX.findall(text))

        if telugu_count >= 3:
            return "te"
        if devanagari_count >= 3:
            return "hi"

        # Check Romanized patterns
        words = set(re.findall(r'\b[a-zA-Z]{3,}\b', text.lower()))
        hinglish_hits = len(words.intersection(HINGLISH_KEYWORDS))
        telugu_hits = len(words.intersection(ROMAN_TELUGU_KEYWORDS))

        if telugu_hits > hinglish_hits and telugu_hits >= 1:
            return "te"
        if hinglish_hits >= 1:
            return "hi"

        return "en"

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predicts scam category and confidence.
        """
        lang = self.detect_language(text)
        
        if self.model is None:
            # Fallback if model not loaded
            return {
                "category": "legitimate",
                "confidence": 0.5,
                "language": lang,
                "probabilities": {"legitimate": 0.5}
            }

        try:
            probs = self.model.predict_proba([text])[0]
            classes = self.model.classes_
            prob_dict = {cls: float(prob) for cls, prob in zip(classes, probs)}
            best_cat = max(prob_dict, key=prob_dict.get)
            best_prob = prob_dict[best_cat]

            return {
                "category": best_cat,
                "confidence": round(best_prob, 4),
                "language": lang,
                "probabilities": prob_dict
            }
        except Exception as e:
            print(f"[NLPClassifier Error] {e}")
            return {
                "category": "legitimate",
                "confidence": 0.5,
                "language": lang,
                "probabilities": {"legitimate": 0.5}
            }

# Global singleton
nlp_classifier = NLPClassifier()
