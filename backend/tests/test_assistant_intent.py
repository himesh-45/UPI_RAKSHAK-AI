import pytest
from backend.app.assistant.intent import (
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
from backend.app.assistant.intent_dataset import TEST_INTENT_DATA, TRAIN_INTENT_DATA
from backend.app.models.schemas import AssistantChatRequest
from backend.app.assistant.service import assistant_service
from backend.app.channels.core import process_channel_submission

def test_intent_datasets_scale():
    """Validates that training has 300+ samples and test has 150+ samples."""
    assert len(TRAIN_INTENT_DATA) >= 300, f"Expected >= 300 training samples, got {len(TRAIN_INTENT_DATA)}"
    assert len(TEST_INTENT_DATA) >= 150, f"Expected >= 150 test samples, got {len(TEST_INTENT_DATA)}"

def test_intent_test_suite_evaluation_metrics():
    """Validates that intent classifier achieves >= 85% Macro-F1 across the held-out test suite."""
    from backend.app.scripts.evaluate_intent import evaluate_intent_classifier
    metrics = evaluate_intent_classifier()
    assert metrics["overall_accuracy_pct"] >= 85.0, f"Accuracy too low: {metrics['overall_accuracy_pct']}%"
    assert metrics["macro_f1"] >= 0.8500, f"Macro-F1 too low: {metrics['macro_f1']}"

def test_regression_how_to_compliant_to_1930():
    """
    Regression: 'how to compliant to 1930' (with typo 'compliant')
    Must return reporting steps with NO verdict and NO score.
    """
    query = "how to compliant to 1930"
    intent_res = intent_classifier.classify(query)
    assert intent_res.intent == INTENT_HOW_TO

    chat_res = assistant_service.analyze_and_respond(
        AssistantChatRequest(message=query, language="en")
    )
    assert chat_res.verdict is None, "HOW_TO must never return a verdict"
    assert chat_res.risk_score is None, "HOW_TO must never return a risk score"
    assert "1930" in chat_res.reply
    assert ("UTR" in chat_res.reply or "step" in chat_res.reply.lower() or "cybercrime.gov.in" in chat_res.reply)
    assert "Verify on the official site" in chat_res.reply
    assert len(chat_res.action_buttons) > 0

def test_regression_pasted_otp_scam_analyzed():
    """
    Regression: A pasted threat message must still be analyzed with multi-detector risk fusion.
    """
    pasted_scam = "URGENT: Your SBI YONO account will be blocked tonight. Click http://sbi-kyc-verify.top to update PAN immediately."
    intent_res = intent_classifier.classify(pasted_scam)
    assert intent_res.intent == INTENT_ANALYZE

    chat_res = assistant_service.analyze_and_respond(
        AssistantChatRequest(message=pasted_scam, language="en")
    )
    assert chat_res.verdict in ["HIGH RISK", "SUSPICIOUS"]
    assert chat_res.risk_score is not None and chat_res.risk_score >= 70
    assert len(chat_res.citations) > 0

def test_regression_lost_money_triggers_emergency():
    """
    Regression: 'I lost 5000 rupees' must trigger emergency Golden-Hour steps.
    """
    emergency_msg = "I lost 5000 rupees"
    intent_res = intent_classifier.classify(emergency_msg)
    assert intent_res.intent == INTENT_EMERGENCY

    chat_res = assistant_service.analyze_and_respond(
        AssistantChatRequest(message=emergency_msg, language="en")
    )
    assert chat_res.verdict is None, "EMERGENCY must never return a verdict"
    assert chat_res.risk_score is None, "EMERGENCY must never return a risk score"
    assert "1930" in chat_res.reply
    assert "bank" in chat_res.reply.lower()
    assert "cybercrime.gov.in" in chat_res.reply
    assert any(b["action"] == "dial_1930" for b in chat_res.action_buttons)

def test_regression_hello_greets():
    """
    Regression: Greetings must return friendly welcome with no scam score.
    """
    for greeting in ["hello", "namaste", "namaskaram"]:
        intent_res = intent_classifier.classify(greeting)
        assert intent_res.intent == INTENT_SMALL_TALK

        chat_res = assistant_service.analyze_and_respond(
            AssistantChatRequest(message=greeting, language="en")
        )
        assert chat_res.verdict is None
        assert chat_res.risk_score is None
        assert "UPI Rakshak" in chat_res.reply
        assert len(chat_res.quick_replies) > 0

def test_regression_unclear_queries():
    """
    Regression: Vague queries must return clarification prompt with two choices.
    """
    unclear_msg = "help"
    intent_res = intent_classifier.classify(unclear_msg)
    assert intent_res.intent == INTENT_UNCLEAR

    chat_res = assistant_service.analyze_and_respond(
        AssistantChatRequest(message=unclear_msg, language="en")
    )
    assert chat_res.verdict is None
    assert chat_res.risk_score is None
    assert "didn't quite catch" in chat_res.reply or "check" in chat_res.reply.lower()
    assert len(chat_res.action_buttons) >= 2

def test_regression_out_of_scope_queries():
    """
    Regression: Out-of-scope questions (recipes, weather, coding, trivia)
    must return a polite explanation of Rakshak's cybersecurity scope with no verdict or score.
    """
    out_of_scope_queries = [
        "How do I make authentic Hyderabadi chicken biryani at home?",
        "What is the weather forecast for New Delhi today?",
        "Write python code for binary search tree insertion",
        "Who won the ICC Cricket World Cup in 2011?",
        "Tell me a funny joke about software developers."
    ]
    for q in out_of_scope_queries:
        intent_res = intent_classifier.classify(q)
        assert intent_res.intent == INTENT_OUT_OF_SCOPE, f"Expected OUT_OF_SCOPE for '{q}', got {intent_res.intent}"

        chat_res = assistant_service.analyze_and_respond(
            AssistantChatRequest(message=q, language="en")
        )
        assert chat_res.verdict is None, "OUT_OF_SCOPE must never return a verdict"
        assert chat_res.risk_score is None, "OUT_OF_SCOPE must never return a risk score"
        assert "UPI Rakshak AI" in chat_res.reply or "cybersecurity" in chat_res.reply.lower() or "suspicious" in chat_res.reply.lower()

def test_multilingual_how_to_guidance():
    """Validates Hindi and Telugu procedural answers."""
    # Hindi query
    hi_res = assistant_service.analyze_and_respond(
        AssistantChatRequest(message="1930 पर शिकायत कैसे दर्ज करें", language="hi")
    )
    assert hi_res.verdict is None
    assert hi_res.risk_score is None
    assert "1930" in hi_res.reply
    assert "cybercrime.gov.in" in hi_res.reply

    # Telugu query
    te_res = assistant_service.analyze_and_respond(
        AssistantChatRequest(message="1930 lo complain ela ivvali", language="te")
    )
    assert te_res.verdict is None
    assert te_res.risk_score is None
    assert "1930" in te_res.reply
    assert "cybercrime.gov.in" in te_res.reply

def test_channel_adapter_shared_intent_routing():
    """
    Validates that Telegram and WhatsApp channel adapters use the same
    shared intent classification logic and do not scan how-to questions as scams.
    """
    import asyncio

    # 1. How-to inquiry on Telegram
    res_tg_howto = asyncio.run(process_channel_submission(
        channel="telegram",
        sender_id="tg_test_12345",
        content_type="text",
        content="how to compliant to 1930"
    ))
    assert res_tg_howto["verdict"] is None
    assert res_tg_howto["risk_score"] is None
    assert "1930" in res_tg_howto["text"]
    assert any("cybercrime.gov.in" in b.get("url", "") or b.get("action") == "open_url" for b in res_tg_howto["buttons"])

    # 2. Emergency loss on WhatsApp
    res_wa_emerg = asyncio.run(process_channel_submission(
        channel="whatsapp",
        sender_id="wa_test_98765",
        content_type="text",
        content="I lost 5000 rupees"
    ))
    assert res_wa_emerg["verdict"] is None
    assert res_wa_emerg["risk_score"] is None
    assert "1930" in res_wa_emerg["text"]

    # 3. Threat message on Telegram (ANALYZE intent)
    res_tg_scam = asyncio.run(process_channel_submission(
        channel="telegram",
        sender_id="tg_test_67890",
        content_type="text",
        content="URGENT SBI account blocked. Visit http://sbi-kyc-fix.top immediately to reactivate."
    ))
    assert res_tg_scam["verdict"] in ["HIGH RISK", "SUSPICIOUS"]
    assert res_tg_scam["risk_score"] is not None and res_tg_scam["risk_score"] >= 70

def test_no_verdict_or_score_for_non_analyze_messages():
    """
    Strict safety check: Never show a SAFE/SUSPICIOUS/HIGH RISK verdict or score
    for HOW_TO, SMALL_TALK, or UNCLEAR messages.
    """
    non_analyze_samples = [
        "how to block my upi id",
        "what is digital arrest",
        "how do collect requests work",
        "is upi safe",
        "what should i prepare before calling 1930",
        "hello",
        "namaste",
        "thank you so much",
        "help",
        "what to do",
        "I lost 5000 rupees to scammer"
    ]

    for sample in non_analyze_samples:
        chat_res = assistant_service.analyze_and_respond(
            AssistantChatRequest(message=sample, language="en")
        )
        assert chat_res.verdict is None, f"Expected None verdict for '{sample}', got {chat_res.verdict}"
        assert chat_res.risk_score is None, f"Expected None risk_score for '{sample}', got {chat_res.risk_score}"
