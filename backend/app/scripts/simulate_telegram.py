import os
import sys
import asyncio
import argparse
from backend.app.channels.core import process_channel_submission

async def main():
    parser = argparse.ArgumentParser(description="Simulate incoming Telegram messages for offline verification")
    parser.add_argument("--text", type=str, help="Text message content to analyze")
    parser.add_argument("--image", type=str, help="Path to image/screenshot file to analyze")
    parser.add_argument("--voice", action="store_true", help="Simulate a voice note submission")
    parser.add_argument("--cmd", type=str, help="Simulate a bot command (e.g. /start, /delete_data, /help)")
    parser.add_argument("--sender", type=str, default="user_tg_987654", help="Simulated Telegram User ID")
    parser.add_argument("--lang", type=str, default="en", choices=["en", "hi", "te"], help="Language hint")
    parser.add_argument("--group", action="store_true", help="Simulate a group chat message")

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
        # Default test scam scenario
        content_type = "text"
        content = "URGENT: Your SBI bank account will be blocked today at 9:30 PM. Complete your KYC now: http://sbi.co.in.kyc-renew.top or enter OTP."

    print("=" * 65)
    print(" 🤖 TELEGRAM BOT SIMULATOR (UPI RAKSHAK AI)")
    print(f" Sender ID:       {args.sender} (will be salted SHA-256 hashed)")
    print(f" Content Type:    {content_type.upper()}")
    print(f" Group Chat:      {args.group}")
    print("=" * 65)

    result = await process_channel_submission(
        channel="telegram",
        sender_id=args.sender,
        content_type=content_type,
        content=content,
        language_hint=args.lang,
        is_group=args.group,
        data_source="test_traffic"
    )

    print("\n--- OUTBOUND TELEGRAM MESSAGE ---\n")
    print(result.get("text", ""))
    print("\n--- INTERACTIVE BUTTONS ---")
    for btn in result.get("buttons", []):
        print(f" [{btn.get('label')}] -> Action: {btn.get('action')}")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(main())
