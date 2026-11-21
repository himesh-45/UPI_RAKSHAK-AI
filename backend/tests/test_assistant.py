import pytest
from backend.app.models.schemas import AssistantChatRequest
from backend.app.assistant.service import assistant_service

def test_assistant_english_response():
    req = AssistantChatRequest(
        message="Your UPI account will be blocked tonight. Click here to verify your OTP: http://sbi-fake.top",
        language="en"
    )
    res = assistant_service.analyze_and_respond(req)

    assert res.verdict == "HIGH RISK"
    assert res.language == "en"
    assert "High Risk Scam Warning" in res.reply
    assert "What Looks Suspicious?" in res.reply
    assert "What NOT To Do" in res.reply
    assert "1930" in res.reply

def test_assistant_telugu_query():
    req = AssistantChatRequest(
        message="నాకు ఈ మెసేజ్ వచ్చింది: మీ SBI ఖాతా కేవైసీ పెండింగ్ ఉన్నందున ఈ రాత్రి బ్లాక్ చేయబడుతుంది. వెంటనే లింక్ ఓపెన్ చేయండి http://fake.top",
        language="te"
    )
    res = assistant_service.analyze_and_respond(req)

    assert res.verdict == "HIGH RISK"
    assert res.language == "te"
    assert "అధిక ప్రమాదం" in res.reply
    assert "1930" in res.reply
    assert "UPI పిన్" in res.reply

def test_assistant_hindi_query():
    req = AssistantChatRequest(
        message="मुझे यह संदेश मिला: आपका बिजली बिल नहीं भरा है। आज रात 9:30 बजे बिजली काट दी जाएगी। कॉल करें +91-98765-43210",
        language="hi"
    )
    res = assistant_service.analyze_and_respond(req)

    assert res.verdict == "HIGH RISK"
    assert res.language == "hi"
    assert "उच्च जोखिम चेतावनी" in res.reply
    assert "1930" in res.reply

def test_assistant_safe_message():
    req = AssistantChatRequest(
        message="SBI Security Alert: OTP for login is 482910. Valid for 10 minutes. Do NOT share with anyone.",
        language="en"
    )
    res = assistant_service.analyze_and_respond(req)

    assert res.verdict == "SAFE"
    assert res.risk_score <= 34
    assert "No Strong Scam Signals Found" in res.reply or "Safe" in res.reply
