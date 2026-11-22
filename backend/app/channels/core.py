import os
import json
import time
import hashlib
import datetime
from typing import Dict, Any, Optional, Union, List, Tuple
from sqlalchemy.orm import Session
from ..config import settings
from ..database import SessionLocal
from ..models.db_models import AnalysisHistory, Feedback
from ..core.masking import mask_sensitive_data
from ..detectors.nlp_classifier import nlp_classifier
from ..detectors.rule_engine import rule_engine
from ..detectors.url_scanner import url_scanner
from ..detectors.ocr_pipeline import ocr_pipeline
from ..fusion.risk_engine import risk_engine
from ..assistant.intent import intent_classifier, INTENT_ANALYZE
from ..assistant.service import assistant_service
from ..models.schemas import AssistantChatRequest

# In-memory rate limiting and deduplication storage
# {sender_hash: [timestamp1, timestamp2, ...]}
_RATE_LIMIT_BUCKET: Dict[str, List[float]] = {}
# Set of (channel, update_id/message_id) with insertion timestamps
_SEEN_UPDATES: Dict[Tuple[str, str], float] = {}
_SEEN_TTL_SECONDS = 3600  # 1 hour deduplication window

def hash_sender_id(sender_id: str) -> str:
    """
    Computes a one-way salted SHA-256 hash of the external sender ID
    (Telegram user ID or WhatsApp phone number). Never stores raw identity.
    """
    salt = settings.SENDER_HASH_SALT.encode("utf-8")
    payload = str(sender_id).strip().encode("utf-8")
    return hashlib.sha256(salt + payload).hexdigest()

def check_channel_rate_limit(sender_hash: str) -> Tuple[bool, int]:
    """
    Sliding window rate limiter: allows up to CHANNEL_RATE_LIMIT_PER_HOUR messages per hour.
    Returns (is_allowed, remaining_quota).
    """
    now = time.time()
    cutoff = now - 3600.0
    history = _RATE_LIMIT_BUCKET.get(sender_hash, [])
    # Prune timestamps older than 1 hour
    history = [ts for ts in history if ts > cutoff]
    
    limit = settings.CHANNEL_RATE_LIMIT_PER_HOUR
    if len(history) >= limit:
        _RATE_LIMIT_BUCKET[sender_hash] = history
        return False, 0
    
    history.append(now)
    _RATE_LIMIT_BUCKET[sender_hash] = history
    return True, limit - len(history)

def is_duplicate_message(channel: str, message_id: str) -> bool:
    """
    Deduplicates incoming webhooks/polling events within a 1-hour window.
    """
    now = time.time()
    key = (channel, str(message_id))
    
    # Prune expired keys if bucket grows large
    if len(_SEEN_UPDATES) > 5000:
        expired = [k for k, ts in _SEEN_UPDATES.items() if now - ts > _SEEN_TTL_SECONDS]
        for k in expired:
            _SEEN_UPDATES.pop(k, None)
            
    if key in _SEEN_UPDATES:
        return True
    
    _SEEN_UPDATES[key] = now
    return False

def delete_user_channel_data(sender_hash: str) -> int:
    """
    Privacy Right-to-be-Forgotten: permanently removes all analysis history
    associated with this salted hashed sender ID.
    """
    db = SessionLocal()
    try:
        deleted_count = db.query(AnalysisHistory).filter(
            AnalysisHistory.sender_hash == sender_hash
        ).delete(synchronize_session=False)
        db.commit()
        return deleted_count
    finally:
        db.close()

def purge_old_channel_history(days: int = 30) -> int:
    """
    Auto-cleanup job: removes channel records older than 30 days.
    """
    db = SessionLocal()
    try:
        cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        deleted = db.query(AnalysisHistory).filter(
            AnalysisHistory.channel.in_(["telegram", "whatsapp"]),
            AnalysisHistory.created_at < cutoff
        ).delete(synchronize_session=False)
        db.commit()
        return deleted
    finally:
        db.close()

def format_channel_report(
    report: Any,
    language: str = "en",
    remaining_quota: int = 20
) -> Dict[str, Any]:
    """
    Formats an evidence-based safety report for chat channels (Telegram/WhatsApp)
    with clear visual indicators, top 3 evidence items, emergency 1930 guidance,
    and action buttons.
    """
    verdict = report.verdict
    score = report.risk_score
    category = report.detected_category.replace("_", " ").title()
    
    if verdict == "HIGH RISK":
        emoji = "🔴"
        verdict_text_en = "HIGH RISK SCAM"
        verdict_text_hi = "अत्यधिक जोखिम (धोखाधड़ी)"
        verdict_text_te = "అధిక ప్రమాదం (మోసం)"
    elif verdict == "SUSPICIOUS":
        emoji = "🟡"
        verdict_text_en = "SUSPICIOUS CONTENT"
        verdict_text_hi = "संदिग्ध संदेश"
        verdict_text_te = "అనుమానాస్పద సందేశం"
    else:
        emoji = "🟢"
        verdict_text_en = "LIKELY SAFE"
        verdict_text_hi = "सुरक्षित प्रतीत होता है"
        verdict_text_te = "సురక్షితంగా కనిపిస్తోంది"

    # Select language headline
    if language == "hi":
        headline = f"{emoji} *यूपीआई रक्षक रिपोर्ट*: {verdict_text_hi}\n📊 *जोखिम स्कोर*: {score}/100\n📂 *श्रेणी*: {category}"
        evidence_header = "🔍 *मुख्य साक्ष्य (Evidence)*:"
        actions_header = "💡 *सलाह (Recommended Actions)*:"
    elif language == "te":
        headline = f"{emoji} *యూపీఐ రక్షక్ నివేదిక*: {verdict_text_te}\n📊 *ప్రమాద స్కోరు*: {score}/100\n📂 *వర్గం*: {category}"
        evidence_header = "🔍 *ప్రధాన సాక్ష్యాధారాలు*:"
        actions_header = "💡 *సూచించిన చర్యలు*:"
    else:
        headline = f"{emoji} *UPI Rakshak Report*: {verdict_text_en}\n📊 *Risk Score*: {score}/100\n📂 *Category*: {category}"
        evidence_header = "🔍 *Key Evidence*:"
        actions_header = "💡 *Recommended Actions*:"

    # Extract top 3 evidence points
    evidence_lines = []
    for ev in report.evidence[:3]:
        if hasattr(ev, "signal"):
            desc = ev.signal
            sev = getattr(ev, "severity", "MEDIUM")
        elif isinstance(ev, dict):
            desc = ev.get("signal") or ev.get("description", "")
            sev = ev.get("severity", "MEDIUM")
        else:
            desc = str(ev)
            sev = "MEDIUM"
        evidence_lines.append(f"• [{sev}] {desc}")
    
    evidence_text = "\n".join(evidence_lines) if evidence_lines else "• No overt malicious patterns detected."

    # Top recommended actions
    action_lines = []
    for act in report.recommended_actions[:2]:
        action_lines.append(f"• {act}")
    actions_text = "\n".join(action_lines)

    # High-risk emergency guidance
    emergency_text = ""
    if verdict == "HIGH RISK":
        if language == "hi":
            emergency_text = (
                "\n\n🚨 *तत्काल सुरक्षा चेतावनी*:\n"
                "1. कोई भी पिन (PIN) दर्ज न करें और न ही कोई क्यूआर (QR) स्कैन करें।\n"
                "2. यदि आपने पैसे ट्रांसफर कर दिए हैं, तो तुरंत *1930* पर कॉल करें या cybercrime.gov.in पर शिकायत दर्ज करें।"
            )
        elif language == "te":
            emergency_text = (
                "\n\n🚨 *తక్షణ భద్రతా హెచ్చరిక*:\n"
                "1. ఎలాంటి పిన్ (PIN) నమోదు చేయవద్దు మరియు QR స్కాన్ చేయవద్దు.\n"
                "2. ఒకవేళ డబ్బు బదిలీ చేసి ఉంటే, వెంటనే *1930* కు కాల్ చేయండి లేదా cybercrime.gov.in లో ఫిర్యాదు చేయండి."
            )
        else:
            emergency_text = (
                "\n\n🚨 *IMMEDIATE SAFETY ADVISORY*:\n"
                "1. NEVER enter your UPI PIN or scan any QR code to receive money.\n"
                "2. Golden-Hour Recovery: If money was lost, call *1930* immediately or file at cybercrime.gov.in."
            )

    full_message = (
        f"{headline}\n\n"
        f"{evidence_header}\n{evidence_text}\n\n"
        f"{actions_header}\n{actions_text}"
        f"{emergency_text}\n\n"
        f"🔒 _Salted SHA-256 privacy enabled. Type /delete_data to erase your scan records._"
    )

    # Standard interactive buttons definition
    buttons = [
        {"id": f"lang_hi_{report.id or 0}", "label": "🇮🇳 हिंदी में समझें", "action": "lang_hi"},
        {"id": f"lang_te_{report.id or 0}", "label": "🇮🇳 తెలుగులో వివరణ", "action": "lang_te"},
        {"id": f"report_{report.id or 0}", "label": "📋 Report Scam", "action": "report_scam"},
        {"id": "delete_my_data", "label": "🗑️ Delete My Data", "action": "delete_data"}
    ]
    if verdict == "HIGH RISK":
        buttons.insert(0, {"id": "call_1930", "label": "🚨 Dial 1930 Cyber Helpline", "action": "dial_1930"})

    return {
        "text": full_message,
        "verdict": verdict,
        "risk_score": score,
        "language": language,
        "buttons": buttons,
        "raw_report": report
    }

async def process_channel_submission(
    channel: str,
    sender_id: str,
    content_type: str,
    content: Union[str, bytes],
    language_hint: Optional[str] = None,
    is_group: bool = False
) -> Dict[str, Any]:
    """
    Channel-agnostic entry point for Telegram and WhatsApp messages.
    Performs rate-limiting, privacy salting, multi-detector fusion,
    masked persistence, and localized response formatting.
    """
    sender_hash = hash_sender_id(sender_id)

    # 1. Rate Limiting (20 messages/hour)
    is_allowed, remaining = check_channel_rate_limit(sender_hash)
    if not is_allowed:
        return {
            "text": (
                "⚠️ *Hourly Rate Limit Reached* / *प्रति घंटा सीमा समाप्त*\n\n"
                "You have exceeded 20 threat analyses in one hour. "
                "Please wait before submitting additional messages to ensure service availability for all users."
            ),
            "verdict": "BLOCKED",
            "risk_score": 0,
            "buttons": []
        }

    # 2. Check for Bot Commands
    if content_type == "text" and isinstance(content, str):
        cmd = content.strip().lower()
        if cmd in ["/start", "/help", "hi", "hello", "namaste"]:
            return {
                "text": (
                    "🛡️ *Welcome to UPI Rakshak AI (यूपीआई रक्षक)*\n\n"
                    "I am an evidence-based digital payment scam detector. Send me:\n"
                    "• Suspicious SMS or WhatsApp messages\n"
                    "• Suspicious links or payment URLs\n"
                    "• Payment QR code screenshots\n\n"
                    "Available Commands:\n"
                    "• `/help` - Show instructions\n"
                    "• `/delete_data` - Permanently erase all your scan records\n"
                    "• `/lang hi` or `/lang te` - Change explanation language\n\n"
                    "🔒 *Privacy Standard*: We do not store your raw phone number or plain text identifiers."
                ),
                "verdict": "INFO",
                "risk_score": 0,
                "buttons": [
                    {"id": "lang_en", "label": "English", "action": "lang_en"},
                    {"id": "lang_hi", "label": "हिंदी", "action": "lang_hi"},
                    {"id": "lang_te", "label": "తెలుగు", "action": "lang_te"}
                ]
            }
        
        if cmd in ["/delete_data", "delete my data"]:
            count = delete_user_channel_data(sender_hash)
            return {
                "text": (
                    f"🗑️ *Data Privacy Erasure Complete*\n\n"
                    f"Successfully deleted {count} historical scan records associated with your hashed ID.\n"
                    "No residual logs or messages remain on our systems."
                ),
                "verdict": "INFO",
                "risk_score": 0,
                "buttons": []
            }

        if cmd in ["/arrest", "digital arrest", "/digital_arrest"]:
            return {
                "text": (
                    "🚨 *Digital Arrest Threat Checker / डिजिटल अरेस्ट जांच*\n\n"
                    "⚠️ *LEGAL FACT*: Indian Law, the CrPC, and BNSS do NOT recognize 'Digital Arrest'.\n\n"
                    "• Real police officers, CBI, ED, or judges NEVER place citizens under arrest via Skype or WhatsApp video calls.\n"
                    "• Real agencies NEVER demand money transfers to 'RBI verification accounts'.\n\n"
                    "👉 Paste what the caller or message claimed right now, and I will audit the coercion tactics."
                ),
                "verdict": "INFO",
                "risk_score": 0,
                "buttons": [
                    {"id": "call_1930", "label": "🚨 Dial 1930 Cyber Helpline", "action": "dial_1930"}
                ]
            }

    # 3. Detect Language
    target_language = language_hint if language_hint in ["hi", "te", "en"] else "en"

    # 4. Handle Voice Notes
    if content_type == "voice":
        if not settings.ENABLE_OFFLINE_STT:
            return {
                "text": (
                    "🎙️ *Voice Note Received* / *वॉयस नोट प्राप्त हुआ*\n\n"
                    "UPI Rakshak runs in offline privacy mode. Speech recognition is disabled on this server. "
                    "Please forward or paste the text of the voice message to instantly check it for scams."
                ),
                "verdict": "INFO",
                "risk_score": 0,
                "buttons": []
            }

    # 5. Execute Multi-Detector Risk Fusion
    if content_type == "image":
        # Content is image bytes
        image_bytes = content if isinstance(content, bytes) else b""
        ocr_res = ocr_pipeline.process_image(image_bytes)
        if not ocr_res.get("success", False):
            return {
                "text": "⚠️ Could not read image. Please ensure the QR code or text is clearly visible and try again.",
                "verdict": "SUSPICIOUS",
                "risk_score": 40,
                "buttons": []
            }
        
        extracted_text = ocr_res.get("combined_text", "")
        qr_analysis = ocr_res.get("qr_analysis")
        
        nlp_res = nlp_classifier.predict(extracted_text) if extracted_text else {"category": "legitimate", "confidence": 0.5, "language": target_language}
        rule_res = rule_engine.evaluate(extracted_text) if extracted_text else {"matched_rules": [], "rule_score": 0.0, "hard_override_high_risk": False}
        url_res = url_scanner.scan_all_urls(extracted_text)
        
        report = risk_engine.fuse(
            input_type="image",
            text=extracted_text,
            nlp_result=nlp_res,
            rule_result=rule_res,
            url_results=url_res,
            qr_result=qr_analysis,
            ocr_result=ocr_res,
            language_override=target_language
        )
        masked_input = f"[{channel.title()} Image] " + mask_sensitive_data(extracted_text[:300])

    else:
        # Text analysis
        text_content = str(content).strip()

        # 5a. Intent Classification: Route how-to, emergency, small-talk, and unclear to Knowledge Base
        intent_res = intent_classifier.classify(text_content)
        if intent_res.intent != INTENT_ANALYZE:
            chat_res = assistant_service.analyze_and_respond(
                AssistantChatRequest(message=text_content, language=target_language)
            )

            buttons = []
            for btn in chat_res.action_buttons:
                action = btn.get("action", "")
                btn_id = f"{action}_{int(time.time())}"
                buttons.append({
                    "id": btn_id,
                    "label": btn.get("label", "Action"),
                    "action": action,
                    "url": btn.get("url")
                })
            buttons.append({"id": "lang_hi", "label": "🇮🇳 हिंदी", "action": "lang_hi"})
            buttons.append({"id": "lang_te", "label": "🇮🇳 తెలుగు", "action": "lang_te"})
            buttons.append({"id": "delete_my_data", "label": "🗑️ Delete Data", "action": "delete_data"})

            return {
                "text": chat_res.reply,
                "verdict": None,
                "risk_score": None,
                "language": chat_res.language,
                "buttons": buttons,
                "raw_report": None
            }

        # 5b. Multi-detector threat analysis for ANALYZE intent
        nlp_res = nlp_classifier.predict(text_content)
        rule_res = rule_engine.evaluate(text_content)
        url_res = url_scanner.scan_all_urls(text_content)

        report = risk_engine.fuse(
            input_type="text",
            text=text_content,
            nlp_result=nlp_res,
            rule_result=rule_res,
            url_results=url_res,
            language_override=target_language
        )
        masked_input = mask_sensitive_data(text_content)

    # 6. Privacy Persistence (STRICT RULE: Never persist group chat messages)
    if not is_group:
        db = SessionLocal()
        try:
            record = AnalysisHistory(
                input_type="image" if content_type == "image" else "text",
                channel=channel,
                sender_hash=sender_hash,
                raw_input_masked=masked_input,
                verdict=report.verdict,
                risk_score=report.risk_score,
                detected_category=report.detected_category,
                language=report.language,
                evidence_json=json.dumps([e.model_dump() for e in report.evidence]),
                actions_json=json.dumps(report.recommended_actions),
                is_simulated=False
            )
            db.add(record)
            db.commit()
            db.refresh(record)
            report.id = record.id
        finally:
            db.close()

    # 7. Format Channel Reply
    return format_channel_report(report, language=target_language, remaining_quota=remaining)
