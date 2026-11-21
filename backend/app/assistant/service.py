import os
from typing import Dict, Any, Optional
from ..config import settings
from ..models.schemas import AssistantChatRequest, AssistantChatResponse, SafetyReport
from ..detectors.nlp_classifier import nlp_classifier
from ..detectors.rule_engine import rule_engine
from ..detectors.url_scanner import url_scanner
from ..fusion.risk_engine import risk_engine
from .templates import format_assistant_response

class AssistantService:
    """
    Multilingual Safety Assistant Service.
    Evidence-grounded explanations with offline deterministic templates
    and optional pluggable LLM fallback.
    """

    def analyze_and_respond(self, req: AssistantChatRequest) -> AssistantChatResponse:
        message = req.message.strip()
        requested_lang = req.language

        # Detect language of message if not explicitly specified
        detected_lang = nlp_classifier.detect_language(message)
        effective_lang = requested_lang if requested_lang in ["en", "hi", "te"] else detected_lang

        # 1. Run through Multi-Layer Detectors
        nlp_res = nlp_classifier.predict(message)
        rule_res = rule_engine.evaluate(message)
        url_res = url_scanner.scan_all_urls(message)

        # 2. Risk Fusion
        report: SafetyReport = risk_engine.fuse(
            input_type="text",
            text=message,
            nlp_result=nlp_res,
            rule_result=rule_res,
            url_results=url_res,
            language_override=effective_lang
        )

        # 3. Optional LLM hook (if API key present, otherwise offline deterministic templates)
        reply_text = self._try_llm_explanation(report, message, effective_lang)
        if not reply_text:
            reply_text = format_assistant_response(report, message, effective_lang)

        return AssistantChatResponse(
            reply=reply_text,
            language=effective_lang,
            verdict=report.verdict,
            risk_score=report.risk_score,
            citations=report.citations,
            recommended_actions=report.recommended_actions
        )

    def _try_llm_explanation(self, report: SafetyReport, user_query: str, lang: str) -> Optional[str]:
        """
        Pluggable LLM explanation layer.
        Gracefully returns None if no external API key is set or if provider fails.
        """
        # Fully offline by default when keys are not configured
        if not settings.GEMINI_API_KEY and not settings.ANTHROPIC_API_KEY:
            return None

        # If key is configured, optional enhancement:
        try:
            if settings.GEMINI_API_KEY:
                # Pluggable Google Gemini hook
                import httpx
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
                prompt = (
                    f"Explain this digital fraud safety report to the user in '{lang}' language. "
                    f"Verdict: {report.verdict}, Score: {report.risk_score}/100, Category: {report.detected_category}. "
                    f"Evidence: {[e.signal for e in report.evidence]}. "
                    f"Actions: {report.recommended_actions}. "
                    "Be grounded strictly in the evidence provided. Include 1930 helpline guidance."
                )
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                with httpx.Client(timeout=4.0) as client:
                    resp = client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"[LLM Service Notice] Falling back to offline template engine: {e}")

        return None

assistant_service = AssistantService()
