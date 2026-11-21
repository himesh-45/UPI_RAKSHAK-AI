import re
import unicodedata
from typing import Dict, Any, Tuple

# Cyrillic & Greek homoglyphs mapped to ASCII equivalents
HOMOGLYPH_MAP = {
    # Cyrillic lowercase
    'а': 'a', 'с': 'c', 'е': 'e', 'о': 'o', 'р': 'p', 'х': 'x', 'у': 'y',
    'і': 'i', 'ј': 'j', 'ѕ': 's', 'ԁ': 'd', 'ԛ': 'q', 'ԝ': 'w',
    # Cyrillic uppercase
    'А': 'A', 'В': 'B', 'С': 'C', 'Е': 'E', 'Н': 'H', 'І': 'I', 'Ј': 'J',
    'К': 'K', 'М': 'M', 'О': 'O', 'Р': 'P', 'Ѕ': 'S', 'Т': 'T', 'Х': 'X',
    # Greek
    'α': 'a', 'ο': 'o', 'ν': 'v', 'ρ': 'p', 'τ': 't', 'κ': 'k', 'ι': 'i',
}

# Invisible / Zero-width characters regex
ZERO_WIDTH_REGEX = re.compile(r'[\u200B-\u200D\uFEFF\u00A0\u200E\u200F\u202A-\u202E\u2060\u180E]')

# Spaced acronym patterns (e.g., "O T P", "P.I.N", "K - Y - C")
SPACED_ACRONYMS = [
    (re.compile(r'(?i)\bO[\s._\-~]+T[\s._\-~]+P\b'), "OTP"),
    (re.compile(r'(?i)\bP[\s._\-~]+I[\s._\-~]+N\b'), "PIN"),
    (re.compile(r'(?i)\bK[\s._\-~]+Y[\s._\-~]+C\b'), "KYC"),
    (re.compile(r'(?i)\bC[\s._\-~]+V[\s._\-~]+V\b'), "CVV"),
    (re.compile(r'(?i)\bU[\s._\-~]+P[\s._\-~]+I\b'), "UPI"),
    (re.compile(r'(?i)\bA[\s._\-~]+P[\s._\-~]+K\b'), "APK"),
]

# Common leetspeak words targeted in scams
LEETSPEAK_VOCAB = {
    "cl1ck": "click",
    "cl!ck": "click",
    "c1ick": "click",
    "v3rify": "verify",
    "ver!fy": "verify",
    "upd4te": "update",
    "upd@te": "update",
    "bl0ck": "block",
    "bl0cked": "blocked",
    "p4y": "pay",
    "p@y": "pay",
    "b1ll": "bill",
    "r3fund": "refund",
    "c4shb4ck": "cashback",
    "c@shback": "cashback",
    "l0tt3ry": "lottery",
    "l0ttery": "lottery",
    "rew4rd": "reward",
    "rew@rd": "reward",
    "urgent1y": "urgently",
    "0tp": "otp",
    "p1n": "pin",
    "cvv2": "cvv",
    "anyd3sk": "anydesk",
}

class TextNormalizer:
    """
    Robust text preprocessor for scam detection.
    Normalizes Unicode (NFKC), strips zero-width/bidi characters,
    unmasks homoglyphs, and de-obfuscates spaced acronyms and leetspeak.
    """

    def normalize(self, text: str) -> str:
        if not text:
            return ""

        # 1. NFKC Unicode normalization (composes standard characters, normalizes full-width digits/latin)
        norm = unicodedata.normalize("NFKC", text)

        # 2. Strip zero-width, invisible, and bidirectional override characters
        norm = ZERO_WIDTH_REGEX.sub("", norm)

        # 3. Replace known Cyrillic/Greek homoglyphs
        chars = [HOMOGLYPH_MAP.get(c, c) for c in norm]
        norm = "".join(chars)

        # 4. De-obfuscate spaced acronyms ("O T P" -> "OTP", "K Y C" -> "KYC")
        for pattern, replacement in SPACED_ACRONYMS:
            norm = pattern.sub(replacement, norm)

        # 5. Token-level leetspeak de-obfuscation
        tokens = re.split(r'(\s+|[.,!?:;/\(\)\[\]{}])', norm)
        cleaned_tokens = []
        for token in tokens:
            lower_tok = token.lower()
            if lower_tok in LEETSPEAK_VOCAB:
                # Maintain case if possible
                replacement = LEETSPEAK_VOCAB[lower_tok]
                if token.isupper():
                    token = replacement.upper()
                elif token.istitle():
                    token = replacement.capitalize()
                else:
                    token = replacement
            cleaned_tokens.append(token)

        return "".join(cleaned_tokens)

    def analyze_obfuscation(self, text: str) -> Dict[str, Any]:
        """
        Detects adversarial obfuscation techniques used in the input.
        """
        zero_width_count = len(ZERO_WIDTH_REGEX.findall(text))
        homoglyph_count = sum(1 for c in text if c in HOMOGLYPH_MAP)
        has_spaced_acronym = any(p.search(text) for p, _ in SPACED_ACRONYMS)
        
        words = re.findall(r'\b\w+\b', text.lower())
        leetspeak_hits = [w for w in words if w in LEETSPEAK_VOCAB]

        is_obfuscated = (
            zero_width_count > 0 or
            homoglyph_count >= 2 or
            has_spaced_acronym or
            len(leetspeak_hits) > 0
        )

        return {
            "is_obfuscated": is_obfuscated,
            "zero_width_count": zero_width_count,
            "homoglyph_count": homoglyph_count,
            "has_spaced_acronym": has_spaced_acronym,
            "leetspeak_detected": leetspeak_hits
        }

text_normalizer = TextNormalizer()
