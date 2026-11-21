from sklearn.base import BaseEstimator, TransformerMixin
from scipy.sparse import csr_matrix
from .normalizer import text_normalizer

# Domain keywords for engineered features
URGENCY_WORDS = [
    "blocked", "suspended", "disconnected", "tonight", "immediately", "urgent",
    "24 hours", "closed", "hold", "कट", "ब्लॉक", "నిలిపివేయబడుతుంది", "బ్లాక్"
]
CREDENTIAL_WORDS = [
    "otp", "pin", "cvv", "password", "netbanking", "passcode", "पिन", "ओटीपी", "పిన్", "ఓటీపీ"
]
COLLECT_WORDS = [
    "collect", "approve", "receive", "scratch", "cashback", "refund", "कलेक्ट", "रिफंड", "కలెక్ట్", "రీఫండ్"
]
REMOTE_WORDS = [
    "anydesk", "teamviewer", "quicksupport", "rustdesk", "ultraviewer", "स्क्रीन", "స్క్రీన్"
]
MONEY_WORDS = [
    "rs", "inr", "lakh", "crore", "won", "prize", "lottery", "रुपये", "రూపాయలు"
]

class EngineeredTextFeatures(BaseEstimator, TransformerMixin):
    """
    Extracts dense domain-specific fraud indicators and linguistic signals.
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        rows = []
        for raw_text in X:
            text = str(raw_text).lower()
            obf = text_normalizer.analyze_obfuscation(str(raw_text))

            length_norm = min(1.0, len(text) / 300.0)
            digits = sum(c.isdigit() for c in text)
            digit_ratio = min(1.0, digits / max(1, len(text)))
            has_url = 1.0 if ("http" in text or "www." in text or ".top" in text or ".xyz" in text) else 0.0
            has_phone = 1.0 if any(c.isdigit() for c in text) and digits >= 10 else 0.0

            has_urgency = 1.0 if any(w in text for w in URGENCY_WORDS) else 0.0
            has_cred = 1.0 if any(w in text for w in CREDENTIAL_WORDS) else 0.0
            has_collect = 1.0 if any(w in text for w in COLLECT_WORDS) else 0.0
            has_remote = 1.0 if any(w in text for w in REMOTE_WORDS) else 0.0
            has_money = 1.0 if any(w in text for w in MONEY_WORDS) else 0.0
            is_obf = 1.0 if obf["is_obfuscated"] else 0.0

            rows.append([
                length_norm,
                digit_ratio,
                has_url,
                has_phone,
                has_urgency,
                has_cred,
                has_collect,
                has_remote,
                has_money,
                is_obf
            ])

        return csr_matrix(rows)
