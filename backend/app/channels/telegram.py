import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any, Optional, Union
import httpx
from fastapi import APIRouter, Request, Header, HTTPException, status
from ..config import settings
from .core import process_channel_submission, is_duplicate_message, hash_sender_id, delete_user_channel_data

logger = logging.getLogger("telegram_bot")
router = APIRouter(prefix="/channels/telegram", tags=["Telegram Bot"])

TELEGRAM_API_BASE = "https://api.telegram.org/bot"

def get_telegram_client() -> Optional[httpx.AsyncClient]:
    if not settings.TELEGRAM_BOT_TOKEN:
        return None
    return httpx.AsyncClient(base_url=f"{TELEGRAM_API_BASE}{settings.TELEGRAM_BOT_TOKEN}", timeout=15.0)

async def send_telegram_message(
    chat_id: Union[int, str],
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "Markdown"
) -> bool:
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.info(f"[Telegram Mock] To {chat_id}: {text[:80]}...")
        return True
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        url = f"{TELEGRAM_API_BASE}{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup
            
        try:
            res = await client.post(url, json=payload)
            return res.status_code == 200
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

async def answer_callback_query(callback_query_id: str, text: Optional[str] = None):
    if not settings.TELEGRAM_BOT_TOKEN:
        return
    async with httpx.AsyncClient(timeout=10.0) as client:
        url = f"{TELEGRAM_API_BASE}{settings.TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
        payload = {"callback_query_id": callback_query_id}
        if text:
            payload["text"] = text
        try:
            await client.post(url, json=payload)
        except Exception as e:
            logger.error(f"Failed to answer callback query: {e}")

async def download_telegram_file(file_id: str) -> Optional[bytes]:
    if not settings.TELEGRAM_BOT_TOKEN:
        return None
    async with httpx.AsyncClient(timeout=20.0) as client:
        # Step 1: get file path
        url = f"{TELEGRAM_API_BASE}{settings.TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}"
        try:
            res = await client.get(url)
            if res.status_code != 200:
                return None
            data = res.json()
            file_path = data.get("result", {}).get("file_path")
            if not file_path:
                return None
            
            # Step 2: download content
            download_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/{file_path}"
            file_res = await client.get(download_url)
            if file_res.status_code == 200 and len(file_res.content) <= 5 * 1024 * 1024:
                return file_res.content
            return None
        except Exception as e:
            logger.error(f"Failed to download Telegram file {file_id}: {e}")
            return None

def build_telegram_keyboard(buttons: list) -> Dict[str, Any]:
    """
    Translates core button specifications into Telegram inline keyboard markup.
    """
    inline_keyboard = []
    row = []
    for btn in buttons:
        action = btn.get("action", "")
        if action == "dial_1930":
            # Telegram url button for helpline
            row.append({"text": btn["label"], "url": "https://cybercrime.gov.in"})
        else:
            row.append({"text": btn["label"], "callback_data": btn["id"]})
        if len(row) == 2:
            inline_keyboard.append(row)
            row = []
    if row:
        inline_keyboard.append(row)
    return {"inline_keyboard": inline_keyboard}

async def handle_telegram_update(update: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core dispatcher for an incoming Telegram update object.
    Supports private chats, mentions in group chats, media downloads,
    callback queries, and deduplication.
    """
    update_id = str(update.get("update_id", ""))
    if is_duplicate_message("telegram", update_id):
        logger.info(f"Ignoring duplicate Telegram update: {update_id}")
        return {"status": "ignored_duplicate"}

    # Handle Callback Queries (inline button clicks)
    if "callback_query" in update:
        cb = update["callback_query"]
        cb_id = cb.get("id")
        from_user = cb.get("from", {})
        sender_id = str(from_user.get("id", ""))
        data = cb.get("data", "")
        chat = cb.get("message", {}).get("chat", {})
        chat_id = chat.get("id")

        if data.startswith("lang_hi"):
            await answer_callback_query(cb_id, "हिंदी में समझें चुना गया")
            await send_telegram_message(chat_id, "🇮🇳 *हिंदी में पुनः विश्लेषण*:\nयह संदेश संदिग्ध भुगतान तत्वों की जांच करता है। किसी भी स्थिति में अपना पिन या ओटीपी साझा न करें।")
        elif data.startswith("lang_te"):
            await answer_callback_query(cb_id, "తెలుగు ఎంపిక చేయబడింది")
            await send_telegram_message(chat_id, "🇮🇳 *తెలుగులో వివరణ*:\nఈ సందేశం మోసపూరిత లావాదేవీల నమూనాలను కలిగి ఉంది. ఎవరితోనూ మీ UPI పిన్ లేదా OTP ని పంచుకోవద్దు.")
        elif data.startswith("report"):
            await answer_callback_query(cb_id, "Scam Reported! Thank you.")
            await send_telegram_message(chat_id, "📋 *Scam Recorded*: Our threat intelligence analysts have received your flag. Thank you for protecting the community!")
        elif data == "delete_my_data":
            h_id = hash_sender_id(sender_id)
            count = delete_user_channel_data(h_id)
            await answer_callback_query(cb_id, "Data deleted")
            await send_telegram_message(chat_id, f"🗑️ All {count} scan records associated with your session have been permanently deleted.")
        else:
            await answer_callback_query(cb_id)
            
        return {"status": "callback_handled"}

    message = update.get("message")
    if not message:
        return {"status": "no_message"}

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    chat_type = chat.get("type", "private")
    is_group = chat_type in ["group", "supergroup"]

    from_user = message.get("from", {})
    sender_id = str(from_user.get("id", "anonymous"))

    # In groups: only respond when explicitly mentioned or replied to
    if is_group:
        bot_username = os.getenv("TELEGRAM_BOT_USERNAME", "upirakshak_bot").lower()
        text_content = message.get("text", "") or message.get("caption", "")
        entities = message.get("entities", [])
        is_mentioned = False
        for ent in entities:
            if ent.get("type") == "mention":
                offset = ent.get("offset", 0)
                length = ent.get("length", 0)
                mention_text = text_content[offset:offset+length].lower().lstrip("@")
                if mention_text == bot_username:
                    is_mentioned = True
                    break
        
        reply_to = message.get("reply_to_message", {})
        if reply_to and reply_to.get("from", {}).get("is_bot", False):
            is_mentioned = True

        if not is_mentioned:
            return {"status": "group_ignored_no_mention"}

    # Identify content type
    content_type = "text"
    content = ""

    if "photo" in message:
        # Highest resolution is last in list
        photos = message["photo"]
        largest_photo = photos[-1]
        file_id = largest_photo.get("file_id")
        content_type = "image"
        # Download photo
        downloaded = await download_telegram_file(file_id)
        if downloaded:
            content = downloaded
        else:
            content = b""
    elif "voice" in message or "audio" in message:
        content_type = "voice"
        content = "voice_note"
    elif "text" in message:
        content_type = "text"
        content = message["text"]
    elif "caption" in message:
        content_type = "text"
        content = message["caption"]

    # Process through core pipeline
    result = await process_channel_submission(
        channel="telegram",
        sender_id=sender_id,
        content_type=content_type,
        content=content,
        is_group=is_group
    )

    # Format Telegram reply
    reply_markup = build_telegram_keyboard(result.get("buttons", [])) if result.get("buttons") else None
    await send_telegram_message(
        chat_id=chat_id,
        text=result["text"],
        reply_markup=reply_markup
    )

    return {"status": "success", "verdict": result.get("verdict"), "score": result.get("risk_score")}

@router.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Optional[str] = Header(None)
):
    """
    Webhook endpoint for production Telegram Bot updates.
    Verifies secret token header if configured.
    """
    if settings.TELEGRAM_WEBHOOK_SECRET:
        if x_telegram_bot_api_secret_token != settings.TELEGRAM_WEBHOOK_SECRET:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Telegram webhook secret token"
            )
            
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    result = await handle_telegram_update(body)
    return result

async def run_polling_bot():
    """
    Long-polling worker for development and local testing.
    Run via: python -m backend.app.channels.telegram --poll
    """
    if not settings.TELEGRAM_BOT_TOKEN:
        print("[Telegram Bot] ERROR: TELEGRAM_BOT_TOKEN is not configured in .env")
        return

    print("[Telegram Bot] Starting long polling service...")
    offset = 0
    async with httpx.AsyncClient(timeout=35.0) as client:
        while True:
            try:
                url = f"{TELEGRAM_API_BASE}{settings.TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json()
                    updates = data.get("result", [])
                    for up in updates:
                        up_id = up.get("update_id", 0)
                        offset = max(offset, up_id + 1)
                        await handle_telegram_update(up)
                elif res.status_code == 409:
                    print("[Telegram Bot] Conflict: Webhook is active. Delete webhook to use polling.")
                    await asyncio.sleep(10)
                else:
                    await asyncio.sleep(2)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[Telegram Bot Polling Error]: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    if "--poll" in sys.argv:
        asyncio.run(run_polling_bot())
    else:
        print("Usage: python -m backend.app.channels.telegram --poll")
