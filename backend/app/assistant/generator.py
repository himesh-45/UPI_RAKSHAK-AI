"""
Grounded Answer Generator & Multi-Layer Safety Guardrails.

Provides swappable backends:
- template: deterministic, offline, fast, reviewed knowledge formatting (default).
- api: Anthropic / Gemini LLM API with PII masking, 15s timeout, circuit breaker,
       daily rate cap, and strict groundedness validation.
- ollama: local offline model endpoint.

Multi-Layer Guardrails:
1. PII Pre-Masking (Redacts phone numbers, bank accounts, OTP codes, names).
2. Prompt Injection & Jailbreak Defense (Refuses deceptive/phishing creation).
3. Groundedness & Whitelist Enforcement (Strips unverified URLs/phone numbers).
4. Verdict Purity (Forbids synthetic LLM verdicts outside deterministic detectors).
5. Mandatory Safety Disclaimer.
6. Graceful Template Fallback on any error, timeout, or policy violation.
"""

import os
import re
import json
import time
import datetime
from typing import List, Dict, Any, Optional, Tuple
from ..config import settings
from .templates import (
    format_how_to_response,
    format_emergency_response,
    format_small_talk_response,
    format_unclear_response,
    format_low_confidence_fallback,
    format_threat_analysis_response,
    format_out_of_scope_response
)

# Canonical Statutory Allowlist for URLs and Phone Numbers
WHITELISTED_DOMAINS = {
    "cybercrime.gov.in",
    "rbi.org.in",
    "npci.org.in",
    "sancharsaathi.gov.in",
    "ceir.sancharsaathi.gov.in",
    "tafcop.sancharsaathi.gov.in",
    "cms.rbi.org.in",
    "scores.sebi.gov.in",
    "digisaathi.info",
    "sbi.co.in",
    "onlinesbi.sbi",
    "hdfcbank.com",
    "icicibank.com",
    "axisbank.com",
    "pnbindia.in",
    "canarabank.com",
    "bankofbaroda.in",
    "unionbankofindia.co.in",
    "indusind.com",
    "kotak.com",
    "whatsapp.com",
    "telegram.org",
    "upirakshak.ai"
}

WHITELISTED_PHONE_NUMBERS = {
    "1930", "14431", "18008913333", "18001234", "18002100", "1800112211",
    "18004253800", "18002584455", "18001080", "18001021661", "18002095577",
    "1800222244", "18002082244", "18004250018", "18005700", "18005000",
    "18001802222", "18001032222", "18002090061", "18602677777"
}

# Prompt Injection & Malicious Jailbreak Keywords
INJECTION_PATTERNS = [
    r"(?i)\b(?:ignore|disregard)\s+(?:all\s+)?(?:previous\s+|prior\s+|safety\s+)?(?:safety|instructions|rules|prompts|guidelines|constraints)\b",
    r"(?i)\b(?:system\s+prompt|developer\s+mode|dan\s+mode|jailbreak|root\s+admin)\b",
    r"(?i)\b(?:from now on you are|you are now|act as|pretend to be|roleplay as|evilrakshak)\b",
    r"(?i)\b(?:write|generate|create|draft|make|give|provide)\b.*\b(?:phishing|scam|fraudulent|deceptive|fake|spyware|malicious|lottery|kbc|cashback|collect\s+request|digital\s+arrest)\b",
    r"(?i)\b(?:write|draft|create|give)\b.*\b(?:script|dialogue)\b.*\b(?:cbi|police|digital\s+arrest|arrest|officer)\b",
    r"(?i)\b(?:set\s+up|create|make|host|build)\b.*\b(?:fake|phishing)\b.*\b(?:website|portal|support|login|page)\b",
    r"(?i)\b(?:how\s+to\s+scam|how\s+to\s+defraud|how\s+to\s+trick|how\s+to\s+steal\s+otp|drain\s+a\s+bank|social\s+engineering\s+tricks)\b",
    r"(?i)\b(?:bypass|evade)\s+(?:all\s+)?(?:detector|security|rakshak|filters?|telecom|scrubbing)\b",
    r"(?i)\b(?:dump\s+internal\s+api\s+keys|output\s+all\s+internal\s+rules|unrestricted\s+coding\s+assistant|bypass\s+all\s+safety\s+rules|exploit\s+payload)\b",
    r"(?:पिछले\s+सभी\s+नियम|डेवलपर\s+मोड|सिस्टम\s+प्रॉम्प्ट|फर्जी\s+बिजली|पैन\s+कार्ड\s+अपडेट\s+मैसेज|ओटीपी\s+मांगने|पैसे\s+ऐंठने|लोगों\s+को\s+फंसाएं|स्क्रिप्ट\s+लिखें)",
    r"(?:సిస్టమ్\s+ప్రాంప్ట్|దాటవేయవచ్చో|నకిలీ.*మెసేజ్\s+రాయండి|మోసం\s+చేయడానికి|కాల్\s+స్క్రిప్ట్\s+రాయండి|ఫ్రాడ్\s+మెసేజ్|డబ్బులు\s+ఎలా\s+కాజేయాలి|పోలీసు\s+స్క్రిప్ట్\s+రాయండి|స్క్రిప్ట్\s+రాయండి|భయపెట్టే)"
]


class UsageTracker:
    """Tracks daily API calls and circuit-breaker status in-memory."""
    def __init__(self):
        self.today = datetime.date.today().isoformat()
        self.call_count = 0
        self.consecutive_failures = 0
        self.circuit_open_until = 0.0

    def record_call(self) -> bool:
        """Returns True if within daily cap and circuit is closed."""
        current_date = datetime.date.today().isoformat()
        if current_date != self.today:
            self.today = current_date
            self.call_count = 0
            self.consecutive_failures = 0
            self.circuit_open_until = 0.0

        daily_cap = getattr(settings, "ASSISTANT_DAILY_CAP", 1000)
        if self.call_count >= daily_cap:
            return False

        if time.time() < self.circuit_open_until:
            return False

        self.call_count += 1
        return True

    def record_success(self):
        self.consecutive_failures = 0
        self.circuit_open_until = 0.0

    def record_failure(self):
        self.consecutive_failures += 1
        if self.consecutive_failures >= 3:
            # Trip circuit breaker for 60 seconds
            self.circuit_open_until = time.time() + 60.0


tracker = UsageTracker()


class GuardrailEngine:
    """Multi-layer PII masking, injection defense, groundedness checking, and verdict purity."""

    @staticmethod
    def mask_pii(text: str) -> str:
        """Redacts phone numbers, bank accounts, and OTPs before sending to LLM."""
        # 1. Mask 11-18 digit account numbers first with word boundaries
        masked = re.sub(r"\b\d{11,18}\b", "[ACCOUNT]", text)

        # 2. Mask 10-digit Indian phone numbers with word boundaries
        masked = re.sub(r"(?:\+91[\-\s]?)?\b[6-9]\d{9}\b", "[PHONE]", masked)

        # 3. Mask OTPs / PINs in context
        masked = re.sub(r"(?i)(?:otp|pin|code)\s*(?:is|:|=)?\s*(\d{4,6})", r"OTP [OTP]", masked)

        # 4. Mask names in self-identifying phrases
        masked = re.sub(r"(?i)\b(?:my\s+name\s+is|i\s+am)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", r"my name is [NAME]", masked)

        return masked

    @staticmethod
    def detect_prompt_injection(text: str) -> bool:
        """Returns True if prompt injection, jailbreak, or malicious scam generation is detected."""
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text):
                return True
        return False

    @staticmethod
    def sanitize_and_ground_urls_phones(
        generated_text: str,
        retrieved_citations: List[Dict[str, Any]],
        language: str = "en"
    ) -> str:
        """
        Enforces groundedness: strips any URL or phone number not in statutory allowlist
        or retrieved chunks, and appends the official portal verification notice.
        """
        # Collect dynamic allowed domains from retrieved citations
        allowed_domains = set(WHITELISTED_DOMAINS)
        for cit in retrieved_citations:
            link = cit.get("official_source_link") or cit.get("official_url") or ""
            match = re.search(r"https?://(?:www\.)?([^/\s]+)", link)
            if match:
                allowed_domains.add(match.group(1).lower())

        modified = False

        # Find all URLs in generated text
        def url_replacer(match):
            nonlocal modified
            full_url = match.group(0)
            domain_match = re.search(r"https?://(?:www\.)?([^/\s:]+)", full_url)
            if not domain_match:
                modified = True
                return ""
            domain = domain_match.group(1).lower()
            if any(domain == d or domain.endswith("." + d) for d in allowed_domains):
                return full_url
            else:
                modified = True
                return ""

        grounded_text = re.sub(r"https?://[^\s)\]]+", url_replacer, generated_text)

        # Find phone numbers (excluding 1930 and allowed hotlines)
        def phone_replacer(match):
            nonlocal modified
            digits = re.sub(r"\D", "", match.group(0))
            if digits in WHITELISTED_PHONE_NUMBERS:
                return match.group(0)
            modified = True
            return ""

        grounded_text = re.sub(r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b", phone_replacer, grounded_text)

        if modified:
            if language == "hi":
                grounded_text += "\n\n*आधिकारिक पोर्टल पर पुष्टि करें: https://cybercrime.gov.in*"
            elif language == "te":
                grounded_text += "\n\n*అధికారిక పోర్టల్‌లో ధృవీకరించండి: https://cybercrime.gov.in*"
            else:
                grounded_text += "\n\n*Verify on the official site: https://cybercrime.gov.in*"

        return grounded_text

    @staticmethod
    def enforce_verdict_purity(text: str, intent: str) -> str:
        """Ensures language models never output synthetic threat verdicts for non-ANALYZE intents."""
        if intent != "ANALYZE":
            # Strip synthetic verdict lines
            text = re.sub(r"(?i)\bverdict\s*:\s*(?:safe|suspicious|high\s+risk)\b", "", text)
            text = re.sub(r"(?i)\brisk\s+(?:score|level)\s*:\s*\d+/\d+\b", "", text)
            text = re.sub(r"(?i)\b(safe|suspicious|high\s+risk)\s+verdict\b", "", text)
        return text

    @staticmethod
    def attach_safety_disclaimer(text: str, language: str = "en") -> str:
        """Appends mandatory AI safety transparency disclaimer."""
        if language == "hi":
            disclaimer = "\n\n*उत्तर सत्यापित सुरक्षा दिशानिर्देशों से एआई द्वारा तैयार किए गए हैं और गलतियाँ हो सकती हैं।*"
        elif language == "te":
            disclaimer = "\n\n*సమాధానాలు సమీక్షించిన భద్రతా మార్గదర్శకాల నుండి AI ద్వారా రూపొందించబడ్డాయి మరియు పొరపాట్లు ఉండవచ్చు.*"
        else:
            disclaimer = "\n\n*Answers are generated with AI from reviewed safety guidance and can make mistakes.*"
        return text.strip() + disclaimer


class AnswerGenerator:
    """Swappable multi-backend response generator with resilient guardrails."""

    def __init__(self):
        self.guardrails = GuardrailEngine()

    def generate(
        self,
        intent: str,
        user_message: str,
        citations: List[Dict[str, Any]],
        language: str = "en",
        history: Optional[List[Dict[str, str]]] = None,
        safety_report: Optional[Any] = None
    ) -> Tuple[str, List[str]]:
        """
        Generates a verified, grounded assistant response across template, api, or ollama backends.
        Returns (reply_text, actionable_steps).
        """
        # 1. Prompt Injection and Malicious Request Guardrail
        if self.guardrails.detect_prompt_injection(user_message):
            if language == "hi":
                refusal = (
                    "मैं केवल धोखाधड़ी से बचाव और शिकायत दर्ज करने में सहायता कर सकता हूँ। "
                    "मैं भ्रामक संदेश तैयार नहीं कर सकता या सुरक्षा नियमों को दरकिनार नहीं कर सकता।"
                )
            elif language == "te":
                refusal = (
                    "నేను సైబర్ మోసాల నివారణ మరియు ఫిర్యాదుల మార్గదర్శకత్వంలో మాత్రమే సహాయపడగలను. "
                    "మోసపూరిత సందేశాలను సృష్టించలేను లేదా భద్రతా నిబంధనలను దాటవేయలేను."
                )
            else:
                refusal = (
                    "I can only help protect against fraud and guide on reporting it. "
                    "I cannot generate deceptive messages or bypass security controls."
                )
            return refusal, ["Call 1930 Cyber Helpline", "Visit cybercrime.gov.in"]

        backend = os.getenv("ASSISTANT_BACKEND", "template").lower()

        # Deterministic / Offline / Template Backend
        if backend == "template" or not citations or intent in ["EMERGENCY", "GREETING", "OUT_OF_SCOPE", "UNCLEAR", "ANALYZE"]:
            return self._generate_template_response(intent, user_message, citations, language, safety_report)

        # External API Backend (Anthropic or Gemini)
        if backend == "api":
            try:
                if not tracker.record_call():
                    # Daily cap exceeded or circuit breaker open -> fallback to template
                    return self._generate_template_response(intent, user_message, citations, language, safety_report)

                api_key = os.getenv("ASSISTANT_API_KEY") or os.getenv("ANTHROPIC_API_KEY") or os.getenv("GEMINI_API_KEY")
                if not api_key:
                    return self._generate_template_response(intent, user_message, citations, language, safety_report)

                response_text = self._call_external_api(user_message, citations, language, history, api_key)
                tracker.record_success()

                # Run Post-Generation Guardrails
                clean_text = self.guardrails.sanitize_and_ground_urls_phones(response_text, citations, language)
                clean_text = self.guardrails.enforce_verdict_purity(clean_text, intent)
                clean_text = self.guardrails.attach_safety_disclaimer(clean_text, language)

                steps = citations[0].get("steps") if citations else ["Call 1930 Cyber Helpline", "Visit cybercrime.gov.in"]
                return clean_text, (steps or [])

            except Exception as e:
                tracker.record_failure()
                # On timeout, network failure, or API error: transparent fallback to template
                return self._generate_template_response(intent, user_message, citations, language, safety_report)

        # Default fallback
        return self._generate_template_response(intent, user_message, citations, language, safety_report)

    def _generate_template_response(
        self,
        intent: str,
        user_message: str,
        citations: List[Dict[str, Any]],
        language: str,
        safety_report: Optional[Any]
    ) -> Tuple[str, List[str]]:
        """Produces 100% deterministic, reviewed, offline-capable responses."""
        if intent == "EMERGENCY":
            return format_emergency_response(language), [
                "Call 1930 immediately",
                "Freeze bank account / UPI",
                "File on cybercrime.gov.in"
            ]

        if intent in ["GREETING", "SMALL_TALK"]:
            return format_small_talk_response(user_message, language), [
                "Check a suspicious message",
                "How to report on 1930"
            ]

        if intent == "OUT_OF_SCOPE":
            return format_out_of_scope_response(language), [
                "Check a suspicious message",
                "Learn about UPI safety"
            ]

        if intent == "UNCLEAR":
            return format_unclear_response(language), [
                "Check a suspicious message",
                "Get help with 1930 reporting"
            ]

        if intent == "ANALYZE":
            if safety_report:
                return format_threat_analysis_response(safety_report, language), [
                    "Report scammer on 1930",
                    "Block contact / UPI handle"
                ]
            return "Analysis complete.", []

        # HOW_TO / HELP
        if not citations:
            return format_low_confidence_fallback(language), [
                "Call 1930 Cyber Helpline",
                "Visit cybercrime.gov.in"
            ]

        top_chunk = citations[0]
        text = format_how_to_response(top_chunk, language)
        steps = top_chunk.get("steps") or [
            "Prepare 12-digit transaction UTR number",
            "Call 1930 helpline immediately",
            "Submit evidence on cybercrime.gov.in"
        ]
        return text, steps

    def _call_external_api(
        self,
        user_message: str,
        citations: List[Dict[str, Any]],
        language: str,
        history: Optional[List[Dict[str, str]]],
        api_key: str
    ) -> str:
        """Calls external LLM via official SDK or REST client with PII redaction and 15s timeout."""
        import urllib.request
        import urllib.error

        # PII Pre-Masking
        masked_query = self.guardrails.mask_pii(user_message)

        # Contextual History (only last 6 turns, all masked)
        masked_history = []
        if history:
            for turn in history[-6:]:
                masked_history.append({
                    "role": turn.get("role", "user"),
                    "content": self.guardrails.mask_pii(turn.get("content", ""))
                })

        # Grounding Knowledge Prompt
        grounding_text = "\n\n".join([
            f"Source: {c.get('source')}\nOfficial URL: {c.get('official_source_link')}\nGuidance: {c.get('content')}\nSteps: {c.get('actionable_guidance')}"
            for c in citations[:2]
        ])

        system_prompt = (
            "You are Rakshak, an official AI cybersecurity assistant dedicated to protecting citizens against UPI fraud.\n"
            f"You MUST reply in language: {language}.\n"
            "CRITICAL RULES:\n"
            "1. Ground your response STRICTLY in the reviewed statutory knowledge provided below.\n"
            "2. NEVER invent phone numbers, URLs, or procedures.\n"
            "3. NEVER provide a SAFE, SUSPICIOUS, or HIGH RISK verdict or threat score.\n"
            "4. Provide concise, numbered steps.\n\n"
            f"REVIEWED KNOWLEDGE:\n{grounding_text}"
        )

        provider = getattr(settings, "ASSISTANT_PROVIDER", "anthropic").lower()
        timeout = getattr(settings, "ASSISTANT_TIMEOUT_SECONDS", 15)

        # Anthropic Claude Endpoint
        if provider == "anthropic" or "claude" in getattr(settings, "ASSISTANT_MODEL", "claude").lower():
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            messages = [{"role": "user", "content": f"{system_prompt}\n\nUser Question: {masked_query}"}]
            payload = {
                "model": getattr(settings, "ASSISTANT_MODEL", "claude-3-5-haiku-20241022"),
                "max_tokens": 512,
                "messages": messages
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["content"][0]["text"]

        # Gemini Generative AI Endpoint
        else:
            model = getattr(settings, "ASSISTANT_MODEL", "gemini-1.5-flash")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            headers = {"content-type": "application/json"}
            payload = {
                "contents": [{
                    "parts": [{"text": f"{system_prompt}\n\nUser Question: {masked_query}"}]
                }]
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["candidates"][0]["content"]["parts"][0]["text"]


answer_generator = AnswerGenerator()
