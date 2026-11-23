import os
from typing import Dict, Any, Optional, List
from ..config import settings
from ..models.schemas import AssistantChatRequest, AssistantChatResponse, SafetyReport, RAGCitation
from ..detectors.nlp_classifier import nlp_classifier
from ..detectors.rule_engine import rule_engine
from ..detectors.url_scanner import url_scanner
from ..fusion.risk_engine import risk_engine
from ..rag.retriever import rag_retriever
from .intent import (
    intent_classifier,
    INTENT_ANALYZE,
    INTENT_HELP,
    INTENT_HOW_TO,
    INTENT_EMERGENCY,
    INTENT_GREETING,
    INTENT_SMALL_TALK,
    INTENT_OUT_OF_SCOPE,
    INTENT_UNCLEAR
)
from .tools import (
    analyze_text,
    analyze_url,
    check_upi_id,
    check_call_script,
    lookup_community_reports,
    retrieve_kb
)
from .templates import (
    format_how_to_response,
    format_emergency_response,
    format_small_talk_response,
    format_unclear_response,
    format_low_confidence_fallback,
    format_threat_analysis_response,
    format_out_of_scope_response
)

class AssistantService:
    """
    Multilingual Safety Assistant Service.
    Intent-guided conversational core with offline deterministic templates,
    knowledge base retrieval, and strict non-hallucination guardrails.
    """

    def analyze_and_respond(self, req: AssistantChatRequest) -> AssistantChatResponse:
        message = req.message.strip()
        requested_lang = req.language

        # Detect language of message if not explicitly specified
        detected_lang = nlp_classifier.detect_language(message)
        effective_lang = requested_lang if requested_lang in ["en", "hi", "te"] else detected_lang

        # 1. Intent Classification
        intent_res = intent_classifier.classify(message, history=req.history)
        intent = intent_res.intent

        # ----------------------------------------------------------------------
        # CASE 1: HOW_TO / HELP PROCEDURAL INQUIRIES
        # ----------------------------------------------------------------------
        if intent in [INTENT_HELP, INTENT_HOW_TO, "HOW_TO", "HELP"]:
            citations = retrieve_kb(message, language=effective_lang, top_k=2)

            # Strict low-confidence check: if retrieval score < 0.16, never hallucinate
            if not citations or citations[0].get("relevance_score", 0.0) < 0.16:
                reply_text = format_low_confidence_fallback(effective_lang)
                rag_citations = []
                actions = ["Call 1930 Cyber Helpline", "Visit cybercrime.gov.in"]
            else:
                top_chunk = citations[0]
                reply_text = format_how_to_response(top_chunk, effective_lang)
                rag_citations = [
                    RAGCitation(
                        title=c["title"],
                        content=c["content"],
                        source=c["source"],
                        actionable_guidance=c.get("actionable_guidance", "")
                    ) for c in citations
                ]
                actions = top_chunk.get("steps", [])

            quick_replies = [
                "What should I prepare?",
                "How to file on cybercrime.gov.in?",
                "Check a suspicious message"
            ] if effective_lang == "en" else (
                [
                    "मुझे क्या दस्तावेज चाहिए?",
                    "1930 पर कॉल कैसे करें?",
                    "संदिग्ध मैसेज चेक करें"
                ] if effective_lang == "hi" else [
                    "ఏ వివరాలు సిద్ధం చేసుకోవాలి?",
                    "1930 కు ఎలా కాల్ చేయాలి?",
                    "అనుమానాస్పద మెసేజ్ తనిఖీ చేయండి"
                ]
            )

            action_buttons = [
                {"label": "🌐 cybercrime.gov.in", "action": "open_url", "url": "https://cybercrime.gov.in"},
                {"label": "🚨 Emergency Steps", "action": "trigger_emergency"},
                {"label": "🔍 Check a Message", "action": "prompt_analyze"}
            ]

            return AssistantChatResponse(
                reply=reply_text,
                language=effective_lang,
                verdict=None,       # Strict: Never show verdict for HOW_TO
                risk_score=None,    # Strict: Never show score for HOW_TO
                citations=rag_citations,
                recommended_actions=actions,
                intent=intent,
                quick_replies=quick_replies,
                action_buttons=action_buttons
            )

        # ----------------------------------------------------------------------
        # CASE 2: EMERGENCY (Money Lost / Active Fraud)
        # ----------------------------------------------------------------------
        elif intent == INTENT_EMERGENCY:
            reply_text = format_emergency_response(effective_lang)
            citations = retrieve_kb("lost money golden hour 1930 helpline freeze bank account", language=effective_lang, top_k=1)
            rag_citations = [
                RAGCitation(
                    title=c["title"],
                    content=c["content"],
                    source=c["source"],
                    actionable_guidance=c.get("actionable_guidance", "")
                ) for c in citations
            ]

            actions = [
                "Call your bank emergency desk immediately to freeze account and cards.",
                "Dial 1930 national helpline within the Golden Hour.",
                "Block UPI ID in payment apps.",
                "Lodge formal complaint at cybercrime.gov.in."
            ]

            quick_replies = [
                "How to freeze bank account?",
                "What to prepare for 1930?",
                "Check a suspicious message"
            ] if effective_lang == "en" else (
                [
                    "बैंक खाता कैसे ब्लॉक करें?",
                    "1930 के लिए क्या जरूरी है?",
                    "संदिग्ध मैसेज चेक करें"
                ] if effective_lang == "hi" else [
                    "బ్యాంక్ ఖాతా ఎలా ఫ్రీజ్ చేయాలి?",
                    "1930 కు ఏ వివరాలు చెప్పాలి?",
                    "అనుమానాస్పద మెసేజ్ చూడండి"
                ]
            )

            action_buttons = [
                {"label": "🚨 Dial 1930 Helpline", "action": "dial_1930"},
                {"label": "🌐 cybercrime.gov.in", "action": "open_url", "url": "https://cybercrime.gov.in"},
                {"label": "🔍 Check a Message", "action": "prompt_analyze"}
            ]

            return AssistantChatResponse(
                reply=reply_text,
                language=effective_lang,
                verdict=None,       # Strict: Never show verdict for EMERGENCY
                risk_score=None,    # Strict: Never show score for EMERGENCY
                citations=rag_citations,
                recommended_actions=actions,
                intent=intent,
                quick_replies=quick_replies,
                action_buttons=action_buttons
            )

        # ----------------------------------------------------------------------
        # CASE 3: GREETING / SMALL_TALK (Greetings, Thanks, Chit-Chat)
        # ----------------------------------------------------------------------
        elif intent in [INTENT_GREETING, INTENT_SMALL_TALK, "GREETING", "SMALL_TALK"]:
            reply_text = format_small_talk_response(effective_lang)
            quick_replies = [
                "Check a suspicious message",
                "How to report to 1930?",
                "What is digital arrest?"
            ] if effective_lang == "en" else (
                [
                    "संदिग्ध मैसेज चेक करें",
                    "1930 पर रिपोर्ट कैसे करें?",
                    "डिजिटल अरेस्ट क्या है?"
                ] if effective_lang == "hi" else [
                    "అనుమానాస్పద సందేశాన్ని తనిఖీ చేయండి",
                    "1930 కు ఎలా ఫిర్యాదు చేయాలి?",
                    "డిజిటల్ అరెస్ట్ అంటే ఏమిటి?"
                ]
            )

            action_buttons = [
                {"label": "🔍 Check a Message", "action": "prompt_analyze"},
                {"label": "💡 Reporting Guide", "action": "prompt_help"}
            ]

            return AssistantChatResponse(
                reply=reply_text,
                language=effective_lang,
                verdict=None,       # Strict: Never show verdict for GREETING
                risk_score=None,    # Strict: Never show score for GREETING
                citations=[],
                recommended_actions=[],
                intent=intent,
                quick_replies=quick_replies,
                action_buttons=action_buttons
            )

        # ----------------------------------------------------------------------
        # CASE 3b: OUT_OF_SCOPE (Non-Cybersecurity, Trivia, Coding, Recipes)
        # ----------------------------------------------------------------------
        elif intent == INTENT_OUT_OF_SCOPE:
            reply_text = format_out_of_scope_response(effective_lang)
            quick_replies = [
                "Check a suspicious message",
                "How to report to 1930?",
                "What is digital arrest?"
            ] if effective_lang == "en" else (
                [
                    "संदिग्ध मैसेज चेक करें",
                    "1930 पर रिपोर्ट कैसे करें?",
                    "डिजिटल अरेस्ट क्या है?"
                ] if effective_lang == "hi" else [
                    "అనుమానాస్పద సందేశాన్ని తనిఖీ చేయండి",
                    "1930 కు ఎలా ఫిర్యాదు చేయాలి?",
                    "డిజిటల్ అరెస్ట్ అంటే ఏమిటి?"
                ]
            )

            action_buttons = [
                {"label": "🔍 Check a Message", "action": "prompt_analyze"},
                {"label": "💡 Safety Guidelines", "action": "prompt_help"}
            ]

            return AssistantChatResponse(
                reply=reply_text,
                language=effective_lang,
                verdict=None,       # Strict: Never show verdict for OUT_OF_SCOPE
                risk_score=None,    # Strict: Never show score for OUT_OF_SCOPE
                citations=[],
                recommended_actions=[],
                intent=intent,
                quick_replies=quick_replies,
                action_buttons=action_buttons
            )

        # ----------------------------------------------------------------------
        # CASE 4: UNCLEAR (Ambiguous / Low-Confidence Queries)
        # ----------------------------------------------------------------------
        elif intent == INTENT_UNCLEAR:
            reply_text = format_unclear_response(effective_lang)
            quick_replies = [
                "Check a suspicious message",
                "Get cyber reporting help"
            ] if effective_lang == "en" else (
                [
                    "संदिग्ध मैसेज चेक करें",
                    "साइबर रिपोर्टिंग सहायता"
                ] if effective_lang == "hi" else [
                    "అనుమానాస్పద సందేశం పరిశీలించండి",
                    "సైబర్ ఫిర్యాదు సహాయం"
                ]
            )

            action_buttons = [
                {"label": "🔍 Check a Message", "action": "prompt_analyze"},
                {"label": "💡 Get Help", "action": "prompt_help"}
            ]

            return AssistantChatResponse(
                reply=reply_text,
                language=effective_lang,
                verdict=None,       # Strict: Never show verdict for UNCLEAR
                risk_score=None,    # Strict: Never show score for UNCLEAR
                citations=[],
                recommended_actions=[],
                intent=intent,
                quick_replies=quick_replies,
                action_buttons=action_buttons
            )

        # ----------------------------------------------------------------------
        # CASE 5: ANALYZE (Pasted Message, URL, QR, Threat Artifact)
        # ----------------------------------------------------------------------
        else:
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

            # 3. Format response cleanly without raw ### artifacts
            reply_text = format_threat_analysis_response(report, effective_lang)

            quick_replies = [
                "What should I prepare?",
                "How to file on cybercrime.gov.in?",
                "Check another message"
            ] if effective_lang == "en" else (
                [
                    "मुझे क्या करना चाहिए?",
                    "1930 पर रिपोर्ट कैसे करें?",
                    "दूसरा मैसेज चेक करें"
                ] if effective_lang == "hi" else [
                    "నేను ఏం చేయాలి?",
                    "1930 కు ఎలా ఫిర్యాదు చేయాలి?",
                    "మరో మెసేజ్ తనిఖీ చేయండి"
                ]
            )

            action_buttons = [
                {"label": "📋 Report this scam", "action": "report_scam"},
                {"label": "🚨 Emergency Steps", "action": "trigger_emergency"},
                {"label": "🔍 Check Another Message", "action": "prompt_analyze"}
            ]
            if report.verdict == "HIGH RISK":
                action_buttons.insert(0, {"label": "🚨 Dial 1930 Helpline", "action": "dial_1930"})

            return AssistantChatResponse(
                reply=reply_text,
                language=effective_lang,
                verdict=report.verdict,
                risk_score=report.risk_score,
                citations=report.citations,
                recommended_actions=report.recommended_actions,
                intent=intent,
                quick_replies=quick_replies,
                action_buttons=action_buttons
            )

assistant_service = AssistantService()
