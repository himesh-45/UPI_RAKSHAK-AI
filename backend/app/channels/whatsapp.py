import os
import hmac
import base64
import hashlib
import logging
from typing import Dict, Any, Optional, Union, List
import httpx
from fastapi import APIRouter, Request, Response, Header, Query, HTTPException, status
from ..config import settings
from .core import process_channel_submission, is_duplicate_message, hash_sender_id, delete_user_channel_data

logger = logging.getLogger("whatsapp_bot")
router = APIRouter(prefix="/channels/whatsapp", tags=["WhatsApp Bot"])

def verify_twilio_signature(url: str, post_data: Dict[str, Any], signature: Optional[str]) -> bool:
    """
    Validates X-Twilio-Signature header using Twilio's standard HMAC-SHA1 algorithm.
    If TWILIO_AUTH_TOKEN is not configured, allows demo execution with a warning.
    """
    if not settings.TWILIO_AUTH_TOKEN:
        return True
    if not signature:
        return False

    # Twilio signature calculation: URL + sorted key-values
    s = url
    for k in sorted(post_data.keys()):
        s += k + str(post_data[k])
    
    mac = hmac.new(settings.TWILIO_AUTH_TOKEN.encode("utf-8"), s.encode("utf-8"), hashlib.sha1)
    computed = base64.b64encode(mac.digest()).decode("utf-8")
    return hmac.compare_digest(computed, signature)

def verify_meta_signature(raw_body: bytes, signature_header: Optional[str]) -> bool:
    """
    Validates X-Hub-Signature-256 header for Meta WhatsApp Cloud API webhooks.
    """
    if not settings.WHATSAPP_APP_SECRET:
        return True
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    
    expected_sig = signature_header.split("sha256=", 1)[1]
    mac = hmac.new(settings.WHATSAPP_APP_SECRET.encode("utf-8"), raw_body, hashlib.sha256)
    computed = mac.hexdigest()
    return hmac.compare_digest(computed, expected_sig)

async def send_twilio_reply(to_number: str, message_text: str) -> bool:
    """
    Sends an outbound WhatsApp message via Twilio REST API.
    """
    if not (settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_WHATSAPP_NUMBER):
        logger.info(f"[Twilio Mock] To {to_number}: {message_text[:80]}...")
        return True

    url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"
    from_wa = settings.TWILIO_WHATSAPP_NUMBER
    if not from_wa.startswith("whatsapp:"):
        from_wa = f"whatsapp:{from_wa}"
    
    target_wa = to_number
    if not target_wa.startswith("whatsapp:"):
        target_wa = f"whatsapp:{target_wa}"

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            res = await client.post(
                url,
                data={
                    "From": from_wa,
                    "To": target_wa,
                    "Body": message_text
                },
                auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            )
            return res.status_code in [200, 201]
        except Exception as e:
            logger.error(f"Failed to send Twilio WhatsApp message: {e}")
            return False

async def send_meta_reply(
    to_phone_number: str,
    text: str,
    buttons: Optional[List[Dict[str, str]]] = None
) -> bool:
    """
    Sends an outbound WhatsApp message via Meta Cloud API.
    Supports interactive button messages with fallback to text menus.
    """
    if not (settings.META_WHATSAPP_TOKEN and settings.META_PHONE_NUMBER_ID):
        logger.info(f"[Meta Mock] To {to_phone_number}: {text[:80]}...")
        return True

    url = f"https://graph.facebook.com/v19.0/{settings.META_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.META_WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload: Dict[str, Any] = {
        "messaging_product": "whatsapp",
        "to": to_phone_number,
    }

    # Meta interactive buttons allow up to 3 quick-reply buttons
    if buttons and 1 <= len(buttons) <= 3:
        meta_buttons = []
        for btn in buttons:
            meta_buttons.append({
                "type": "reply",
                "reply": {
                    "id": btn.get("id", "btn"),
                    "title": btn.get("label", "")[:20]  # Meta limit: 20 chars
                }
            })
        payload["type"] = "interactive"
        payload["interactive"] = {
            "type": "button",
            "body": {"text": text},
            "action": {"buttons": meta_buttons}
        }
    else:
        # Text message fallback (or if buttons > 3)
        payload["type"] = "text"
        payload["text"] = {"body": text}

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            res = await client.post(url, json=payload, headers=headers)
            return res.status_code in [200, 201]
        except Exception as e:
            logger.error(f"Failed to send Meta WhatsApp message: {e}")
            return False

async def download_media(media_url: str, auth: Optional[tuple] = None, headers: Optional[dict] = None) -> Optional[bytes]:
    """
    Downloads media asset (max 5MB) from Twilio or Meta storage.
    """
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            res = await client.get(media_url, auth=auth, headers=headers)
            if res.status_code == 200 and len(res.content) <= 5 * 1024 * 1024:
                return res.content
            return None
        except Exception as e:
            logger.error(f"Failed to download WhatsApp media from {media_url}: {e}")
            return None

# =====================================================================
# 1. Twilio WhatsApp Webhook Endpoint
# =====================================================================
@router.post("/twilio")
async def twilio_whatsapp_webhook(
    request: Request,
    x_twilio_signature: Optional[str] = Header(None)
):
    """
    Webhook receiver for Twilio WhatsApp sandbox and production messages.
    """
    form_data = await request.form()
    data_dict = dict(form_data)

    # Validate Twilio signature
    full_url = str(request.url)
    if not verify_twilio_signature(full_url, data_dict, x_twilio_signature):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Twilio signature"
        )

    message_sid = data_dict.get("MessageSid", "")
    if is_duplicate_message("whatsapp", message_sid):
        return Response(content="<Response></Response>", media_type="application/xml")

    from_number = data_dict.get("From", "").replace("whatsapp:", "")
    body_text = data_dict.get("Body", "")
    num_media = int(data_dict.get("NumMedia", "0"))

    content_type = "text"
    content: Union[str, bytes] = body_text

    # Check for media attachments (Images, Audio)
    if num_media > 0:
        media_url = data_dict.get("MediaUrl0", "")
        media_content_type = data_dict.get("MediaContentType0", "")
        auth = (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN) if settings.TWILIO_AUTH_TOKEN else None
        
        media_bytes = await download_media(media_url, auth=auth)
        if media_bytes:
            if "image" in media_content_type:
                content_type = "image"
                content = media_bytes
            elif "audio" in media_content_type or "ogg" in media_content_type:
                content_type = "voice"
                content = "voice_note"

    result = await process_channel_submission(
        channel="whatsapp",
        sender_id=from_number,
        content_type=content_type,
        content=content
    )

    # Build TwiML response
    twiml_reply = (
        f'<?xml version="1.0" encoding="UTF-8"?>'
        f'<Response><Message>{result["text"]}</Message></Response>'
    )
    return Response(content=twiml_reply, media_type="application/xml")

# =====================================================================
# 2. Meta WhatsApp Cloud API Webhook Endpoints
# =====================================================================
@router.get("/meta")
def meta_webhook_verification(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token")
):
    """
    Verification challenge handshake for Meta WhatsApp Cloud API.
    """
    if hub_mode == "subscribe":
        if settings.META_VERIFY_TOKEN and hub_verify_token != settings.META_VERIFY_TOKEN:
            raise HTTPException(status_code=403, detail="Verification token mismatch")
        return Response(content=hub_challenge or "", media_type="text/plain")
    
    raise HTTPException(status_code=400, detail="Invalid verification request")

@router.post("/meta")
async def meta_webhook_events(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None)
):
    """
    Event receiver for Meta WhatsApp Cloud API incoming messages.
    """
    raw_body = await request.body()
    if not verify_meta_signature(raw_body, x_hub_signature_256):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Meta X-Hub-Signature-256"
        )

    try:
        body = json.loads(raw_body.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    entries = body.get("entry", [])
    for entry in entries:
        changes = entry.get("changes", [])
        for change in changes:
            value = change.get("value", {})
            messages = value.get("messages", [])
            for msg in messages:
                msg_id = msg.get("id", "")
                if is_duplicate_message("whatsapp", msg_id):
                    continue

                from_number = msg.get("from", "")
                msg_type = msg.get("type", "text")
                content_type = "text"
                content: Union[str, bytes] = ""

                if msg_type == "text":
                    content_type = "text"
                    content = msg.get("text", {}).get("body", "")
                elif msg_type == "interactive":
                    # Button reply
                    btn_reply = msg.get("interactive", {}).get("button_reply", {})
                    btn_id = btn_reply.get("id", "")
                    if btn_id == "delete_my_data":
                        h_id = hash_sender_id(from_number)
                        del_count = delete_user_channel_data(h_id)
                        await send_meta_reply(
                            from_number,
                            f"🗑️ All {del_count} scan records associated with your session have been permanently deleted."
                        )
                        continue
                    content_type = "text"
                    content = btn_reply.get("title", "")
                elif msg_type == "image":
                    content_type = "image"
                    image_id = msg.get("image", {}).get("id")
                    if image_id and settings.META_WHATSAPP_TOKEN:
                        # Fetch image URL from Graph API
                        async with httpx.AsyncClient(timeout=15.0) as client:
                            meta_media_url = f"https://graph.facebook.com/v19.0/{image_id}"
                            headers = {"Authorization": f"Bearer {settings.META_WHATSAPP_TOKEN}"}
                            r = await client.get(meta_media_url, headers=headers)
                            if r.status_code == 200:
                                download_url = r.json().get("url")
                                if download_url:
                                    downloaded = await download_media(download_url, headers=headers)
                                    if downloaded:
                                        content = downloaded
                elif msg_type in ["audio", "voice"]:
                    content_type = "voice"
                    content = "voice_note"

                # Run through core pipeline
                result = await process_channel_submission(
                    channel="whatsapp",
                    sender_id=from_number,
                    content_type=content_type,
                    content=content
                )

                # Send outbound reply with buttons
                await send_meta_reply(
                    to_phone_number=from_number,
                    text=result["text"],
                    buttons=result.get("buttons", [])[:3]
                )

    return {"status": "success"}
