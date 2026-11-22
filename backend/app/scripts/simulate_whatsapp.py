import os
import sys
import asyncio
import argparse
from backend.app.channels.core import process_channel_submission

async def main():
    parser = argparse.ArgumentParser(description="Simulate incoming WhatsApp messages (Twilio/Meta) for offline verification")
    parser.add_argument("--text", type=str, help="Text message content to analyze")
    parser.add_argument("--image", type=str, help="Path to image/screenshot file to analyze")
    parser.add_argument("--voice", action="store_true", help="Simulate a voice note submission")
    parser.add_argument("--cmd", type=str, help="Simulate a bot command (e.g. /start, /delete_data, /help)")
    parser.add_argument("--sender", type=str, default="+919876543210", help="Simulated WhatsApp phone number")
    parser.add_argument("--lang", type=str, default="en", choices=["en", "hi", "te"], help="Language hint")

    args = parser.parse_args()

    content_type = "text"
    content = ""

    if args.cmd:
        content_type = "text"
        content = args.cmd
    elif args.image:
        if not os.path.exists(args.image):
            print(f"[Error] Image file not found: {args.image}")
            sys.exit(1)
        content_type = "image"
        with open(args.image, "rb") as f:
            content = f.read()
    elif args.voice:
        content_type = "voice"
        content = "voice_note"
    elif args.text:
        content_type = "text"
        content = args.text
    else:
        # Default test scenario: Hindi collect request
        content_type = "text"
        content = "बधाई हो! आपको Google Pay पर ₹3,000 का कैशबैक मिला है। तुरंत पाने के लिए अपना यूपीआई पिन दर्ज करें।"
        args.lang = "hi"

    print("=" * 65)
    print(" 📱 WHATSAPP BOT SIMULATOR (UPI RAKSHAK AI)")
    print(f" Sender Phone:    {args.sender} (will be salted SHA-256 hashed)")
    print(f" Content Type:    {content_type.upper()}")
    print(f" Language Hint:   {args.lang}")
    print("=" * 65)

    result = await process_channel_submission(
        channel="whatsapp",
        sender_id=args.sender,
        content_type=content_type,
        content=content,
        language_hint=args.lang
    )

    print("\n--- OUTBOUND WHATSAPP MESSAGE ---\n")
    print(result.get("text", ""))
    print("\n--- INTERACTIVE QUICK REPLIES ---")
    for btn in result.get("buttons", []):
        print(f" [{btn.get('label')}] -> Action: {btn.get('action')}")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(main())
