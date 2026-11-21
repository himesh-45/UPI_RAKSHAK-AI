import re
from typing import Dict, Any, List

# Script Unicode boundaries
DEVANAGARI_RANGE = re.compile(r'[\u0900-\u097F]')
TELUGU_RANGE = re.compile(r'[\u0C00-\u0C7F]')

# Common character 3-gram and 4-gram profiles for colloquial Indian Latin texts
HINGLISH_CHAR_NGRAMS = {
    "kar", "kare", "karo", "aap", "aapka", "kya", "hai", "hain", "nah", "nahi",
    "bhej", "tur", "turan", "rant", "paise", "rupay", "khata", "band", "liye",
    "wala", "wali", "kisi", "saath", "apna", "gaya", "aaya", "hoga", "raha",
    "rahi", "dekh", "batao", "bataye", "bijli", "vibh", "vibhag", "sampar"
}

ROMAN_TELUGU_CHAR_NGRAMS = {
    "mee", "meeku", "chey", "cheya", "yandi", "vach", "vachi", "chindi", "dabb",
    "dabbul", "kott", "kottan", "undal", "aagad", "leka", "pothe", "chesu",
    "raval", "chuda", "ippud", "ippude", "vent", "ventan", "kinda", "gurin",
    "telusu", "chala", "chesi", "padat", "padath", "avvaku", "evarik",
    "katt", "katta", "kattaledu", "roju", "chesth", "chestharu", "ledu", "kaadu",
    "undhi", "undi", "pamp", "pampin", "choodu", "chusth", "avuthundi"
}

ENGLISH_COMMON_WORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it",
    "for", "not", "on", "with", "he", "as", "you", "do", "at", "this",
    "but", "his", "by", "from", "they", "we", "say", "her", "she", "or",
    "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "dear", "customer", "account", "transaction", "amount", "credited", "debited"
}

class NgramLanguageDetector:
    """
    Multilingual language and script detector for English, Hindi, and Telugu,
    including transliterated / Romanized vernacular scripts (Hinglish, Romanized Telugu).
    """

    def detect(self, text: str) -> Dict[str, Any]:
        if not text or not text.strip():
            return {
                "language": "en",
                "script": "Latin",
                "sub_type": "standard_en",
                "confidence": 1.0
            }

        # 1. Native script detection by Unicode code points
        devanagari_chars = len(DEVANAGARI_RANGE.findall(text))
        telugu_chars = len(TELUGU_RANGE.findall(text))
        total_chars = max(1, len(text.replace(" ", "")))

        dev_ratio = devanagari_chars / total_chars
        tel_ratio = telugu_chars / total_chars

        if tel_ratio > 0.15 or telugu_chars >= 4:
            return {
                "language": "te",
                "script": "Telugu",
                "sub_type": "native_telugu",
                "confidence": min(1.0, 0.7 + tel_ratio)
            }

        if dev_ratio > 0.15 or devanagari_chars >= 4:
            return {
                "language": "hi",
                "script": "Devanagari",
                "sub_type": "native_hindi",
                "confidence": min(1.0, 0.7 + dev_ratio)
            }

        # 2. Latin script transliteration analysis (Hinglish vs Romanized Telugu vs English)
        words = re.findall(r'[a-zA-Z]{2,}', text.lower())
        if not words:
            return {
                "language": "en",
                "script": "Latin",
                "sub_type": "standard_en",
                "confidence": 0.5
            }

        text_lower = " " + text.lower() + " "
        
        # Calculate matching densities
        hinglish_score = sum(1 for ng in HINGLISH_CHAR_NGRAMS if ng in text_lower)
        roman_te_score = sum(1 for ng in ROMAN_TELUGU_CHAR_NGRAMS if ng in text_lower)
        english_score = sum(1 for w in words if w in ENGLISH_COMMON_WORDS)

        # Distinguish transliterated Indic from English
        if roman_te_score >= 2 and roman_te_score > hinglish_score:
            conf = min(0.95, 0.6 + 0.1 * roman_te_score)
            return {
                "language": "te",
                "script": "Latin",
                "sub_type": "romanized_telugu",
                "confidence": round(conf, 3)
            }

        if hinglish_score >= 2 and hinglish_score > roman_te_score:
            conf = min(0.95, 0.6 + 0.1 * hinglish_score)
            return {
                "language": "hi",
                "script": "Latin",
                "sub_type": "hinglish",
                "confidence": round(conf, 3)
            }

        return {
            "language": "en",
            "script": "Latin",
            "sub_type": "standard_en",
            "confidence": 0.90 if english_score > 0 else 0.75
        }

    detect_language = detect

language_detector = NgramLanguageDetector()
