import os
import joblib
from typing import Dict, Any, Tuple
from ..core.normalizer import text_normalizer
from ..core.language_detector import language_detector

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
        det = language_detector.detect(text)
        return det["language"]

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predicts scam category and confidence with text normalization and calibration.
        """
        det_meta = language_detector.detect(text)
        lang = det_meta["language"]

        normalized_text = text_normalizer.normalize(text)
        obfuscation_info = text_normalizer.analyze_obfuscation(text)
        
        if self.model is None:
            # Fallback if model not loaded
            return {
                "category": "legitimate",
                "confidence": 0.5,
                "language": lang,
                "language_meta": det_meta,
                "obfuscation_info": obfuscation_info,
                "probabilities": {"legitimate": 0.5}
            }

        try:
            probs = self.model.predict_proba([normalized_text])[0]
            classes = self.model.classes_
            prob_dict = {cls: float(prob) for cls, prob in zip(classes, probs)}
            best_cat = max(prob_dict, key=prob_dict.get)
            best_prob = prob_dict[best_cat]

            return {
                "category": best_cat,
                "confidence": round(best_prob, 4),
                "language": lang,
                "language_meta": det_meta,
                "normalized_text": normalized_text,
                "obfuscation_info": obfuscation_info,
                "probabilities": prob_dict
            }
        except Exception as e:
            print(f"[NLPClassifier Error] {e}")
            return {
                "category": "legitimate",
                "confidence": 0.5,
                "language": lang,
                "language_meta": det_meta,
                "obfuscation_info": obfuscation_info,
                "probabilities": {"legitimate": 0.5}
            }

nlp_classifier = NLPClassifier()
