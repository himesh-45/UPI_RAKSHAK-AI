"""
Assistant Tools Layer for UPI Rakshak AI.
Plain Python functions that the conversational safety assistant orchestrates to
produce verified verdicts, evidence signals, and factual guidance.
All verdicts and scores originate from deterministic detectors, NEVER from LLM vibes.
"""

from typing import Dict, Any, List, Optional
from ..detectors.nlp_classifier import nlp_classifier
from ..detectors.rule_engine import rule_engine
from ..detectors.url_scanner import url_scanner
from ..fusion.risk_engine import risk_engine
from ..core.vpa_verifier import vpa_verifier
from ..core.community_reputation import lookup_community_reputation
from ..rag.retriever import rag_retriever


def analyze_text(text: str, language: str = "en") -> Dict[str, Any]:
    """
    Analyzes suspicious SMS, chat, or pasted payment message using multi-detector risk fusion.
    """
    clean_text = (text or "").strip()
    if not clean_text:
        return {
            "verdict": "SAFE",
            "risk_score": 0,
            "detected_category": "unknown",
            "evidence": [],
            "recommended_actions": [],
            "citations": []
        }

    nlp_res = nlp_classifier.predict(clean_text)
    rule_res = rule_engine.evaluate(clean_text)
    url_res = url_scanner.scan_all_urls(clean_text)

    report = risk_engine.fuse(
        input_type="text",
        text=clean_text,
        nlp_result=nlp_res,
        rule_result=rule_res,
        url_results=url_res,
        language_override=language
    )

    return {
        "verdict": report.verdict,
        "risk_score": report.risk_score,
        "detected_category": report.detected_category,
        "plain_language_explanation": report.plain_language_explanation,
        "evidence": [e.dict() if hasattr(e, "dict") else e for e in report.evidence],
        "recommended_actions": report.recommended_actions,
        "citations": [c.dict() if hasattr(c, "dict") else c for c in report.citations],
        "highlight_spans": [h.dict() if hasattr(h, "dict") else h for h in getattr(report, "highlight_spans", [])],
        "confidence": report.confidence
    }


def analyze_url(url: str) -> Dict[str, Any]:
    """
    Performs pure static, zero-network security analysis on suspicious URL or domain.
    Never executes HTTP requests or DNS resolution.
    """
    clean_url = (url or "").strip()
    if not clean_url:
        return {
            "url": "",
            "is_suspicious": False,
            "risk_level": "SAFE",
            "risk_score": 0,
            "reasons": []
        }

    scan_res = url_scanner.analyze_url(clean_url)
    return scan_res


def check_upi_id(vpa: str, payee_name: Optional[str] = "", amount: Optional[float] = None) -> Dict[str, Any]:
    """
    Validates a UPI Virtual Payment Address (VPA), detects brand spoofing, and evaluates collect-request risk.
    """
    clean_vpa = (vpa or "").strip()
    res = vpa_verifier.analyze(
        vpa=clean_vpa,
        payee_name=payee_name or "",
        amount=amount,
        is_collect=False
    )
    return {
        "vpa": res.vpa,
        "is_valid_format": res.is_valid_format,
        "handle": res.handle,
        "provider": res.provider,
        "psp_name": res.provider,
        "risk_score": res.risk_score,
        "verdict": res.verdict,
        "reasons": res.reasons,
        "warning_notice": res.warning_notice,
        "is_suspicious": res.risk_score >= 35
    }


def check_call_script(script: str, language: str = "en") -> Dict[str, Any]:
    """
    Analyzes phone scam / digital arrest / remote-access coercion transcripts.
    Identifies high-pressure tactics, fake law enforcement intimidation, and OTP demands.
    """
    clean_script = (script or "").strip()
    if not clean_script:
        return {
            "verdict": "SAFE",
            "risk_score": 0,
            "flagged_tactics": [],
            "immediate_advice": "No call transcript provided.",
            "evidence": []
        }

    # Evaluate using text analysis engine
    analysis = analyze_text(clean_script, language=language)

    tactics = []
    lower_text = clean_script.lower()

    if any(k in lower_text for k in ["digital arrest", "video call", "skype", "cbi officer", "police station", "customs narcotics"]):
        tactics.append("Fake Law Enforcement / Digital Arrest Intimidation")
    if any(k in lower_text for k in ["anydesk", "teamviewer", "quicksupport", "rustdesk", "screen share"]):
        tactics.append("Remote Access Trojan Installation Coercion")
    if any(k in lower_text for k in ["transfer money for verification", "rbi secret account", "clearance fee", "bail deposit"]):
        tactics.append("Extortion Money Transfer Request")
    if any(k in lower_text for k in ["do not disconnect", "stay on line", "isolate yourself", "do not tell anyone"]):
        tactics.append("Psychological Isolation & Pressure Tactic")
    if any(k in lower_text for k in ["otp", "pin", "cvv", "password"]):
        tactics.append("Credential Extraction Demand")

    immediate_advice = (
        "1. Disconnect the call immediately.\n"
        "2. Genuine Indian Police, CBI, ED, and Supreme Court NEVER issue arrest warrants over WhatsApp video calls.\n"
        "3. Never download AnyDesk, TeamViewer or RustDesk at a caller's request.\n"
        "4. Call the National Cybercrime Helpline at 1930."
    )

    # If intimidation tactics are detected, ensure high risk score
    score = analysis.get("risk_score", 0)
    if tactics:
        score = max(score, 88)
        verdict = "HIGH RISK"
    else:
        verdict = analysis.get("verdict", "SAFE")

    return {
        "verdict": verdict,
        "risk_score": score,
        "flagged_tactics": tactics,
        "immediate_advice": immediate_advice,
        "evidence": analysis.get("evidence", [])
    }


def lookup_community_reports(entity_type: str, entity_value: str) -> Dict[str, Any]:
    """
    Queries community-reported threat intelligence for VPAs, phone numbers, and domains.
    """
    return lookup_community_reputation(entity_type, entity_value)


def retrieve_kb(query: str, language: str = "en", top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Retrieves grounded safety guidance chunks from the RAG knowledge base.
    """
    chunks = rag_retriever.retrieve(query, top_k=top_k)
    return chunks
