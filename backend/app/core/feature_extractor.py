from sklearn.base import BaseEstimator, TransformerMixin
from scipy.sparse import csr_matrix
from .normalizer import text_normalizer

# Domain keywords for engineered features
URGENCY_WORDS = [
    "blocked", "suspended", "disconnected", "tonight", "immediately", "urgent",
    "24 hours", "closed", "hold", "कट", "काट", "काट दी जाएगी", "ब्लॉक", "నిలిపివేయబడుతుంది", "బ్లాక్"
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

UTILITY_WORDS = [
    "electricity", "power", "meter", "bijli", "बिजली", "కరెంట్", "విద్యుత్", "बिल", "bill", "substation", "linesman"
]

ADVISORY_NEGATIONS = [
    "never share", "do not share", "don't share", "not share", "kisi ko na",
    "share na kare", "evariki cheppavaddu", "share cheyavoddu", "bank never",
    "never calls", "never disclose", "do not disclose", "never ask", "not disclose"
]

BANK_ALERT_MARKERS = [
    "debited", "credited", "avail bal", "balance", "bal:", "a/c", "acct",
    "salary", "transaction successful", "ref no", "utr", "upi ref"
]

class EngineeredTextFeatures(BaseEstimator, TransformerMixin):
    """
    Extracts dense domain-specific fraud indicators, advisory negations, and linguistic signals.
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
            has_utility = 1.0 if any(w in text for w in UTILITY_WORDS) else 0.0
            has_advisory = 1.0 if any(neg in text for neg in ADVISORY_NEGATIONS) else 0.0
            raw_cred = any(w in text for w in CREDENTIAL_WORDS)
            has_cred_demand = 1.0 if (raw_cred and not has_advisory) else 0.0
            has_collect = 1.0 if any(w in text for w in COLLECT_WORDS) else 0.0
            has_remote = 1.0 if any(w in text for w in REMOTE_WORDS) else 0.0
            has_money = 1.0 if any(w in text for w in MONEY_WORDS) else 0.0
            has_bank_marker = 1.0 if any(bm in text for bm in BANK_ALERT_MARKERS) else 0.0
            is_obf = 1.0 if obf["is_obfuscated"] else 0.0

            rows.append([
                length_norm,
                digit_ratio,
                has_url,
                has_phone,
                has_urgency,
                has_utility,
                has_cred_demand,
                has_advisory,
                has_collect,
                has_remote,
                has_money,
                has_bank_marker,
                is_obf
            ])

        return csr_matrix(rows)
