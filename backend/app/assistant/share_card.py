"""
Server-Side Shareable 'Scam Alert' Card Generator (Pillow).
Generates high-resolution 1200x630 OpenGraph/WhatsApp cards in < 50ms.
Includes guardian branding, score badge, masked text snippet, key evidence,
and statutory 1930 helpline guidance.
"""

import io
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont
from .generator import GuardrailEngine


def generate_scam_alert_card(
    verdict: str = "HIGH RISK",
    score: int = 87,
    message_snippet: str = "Your electricity power will be disconnected at 9:30 PM tonight. Pay immediately.",
    reasons: Optional[List[str]] = None,
    language: str = "en"
) -> bytes:
    """
    Renders a 1200x630 PNG image buffer suitable for WhatsApp/Telegram sharing.
    """
    if reasons is None:
        reasons = [
            "Coercive urgency & disconnection deadline",
            "Unverified phone number / payment link",
            "Requests instant payment outside official portal"
        ]

    # Pre-mask any PII in snippet
    safe_snippet = GuardrailEngine.mask_pii(message_snippet)
    if len(safe_snippet) > 160:
        safe_snippet = safe_snippet[:157] + "..."

    # Colors
    is_high = verdict.upper() in ["HIGH RISK", "DANGER"] or score >= 70
    is_suspicious = verdict.upper() in ["SUSPICIOUS", "WARNING"] or (score >= 35 and score < 70)

    if is_high:
        accent_color = (239, 68, 68)       # Red-500
        accent_glow = (239, 68, 68, 40)
        verdict_label = "HIGH RISK SCAM"
    elif is_suspicious:
        accent_color = (245, 158, 11)     # Amber-500
        accent_glow = (245, 158, 11, 40)
        verdict_label = "SUSPICIOUS THREAT"
    else:
        accent_color = (16, 185, 129)     # Green-500
        accent_glow = (16, 185, 129, 40)
        verdict_label = "LIKELY SAFE"

    bg_color = (10, 15, 29)               # Deep Navy #0a0f1d
    card_bg = (16, 24, 46)                # Slate-900 #10182e
    border_color = (30, 41, 69)           # Slate-800
    cyan_accent = (0, 229, 255)           # Electric Cyan #00e5ff
    text_white = (248, 250, 252)          # Slate-50
    text_muted = (148, 163, 184)          # Slate-400

    # Create base canvas
    img = Image.new("RGB", (1200, 630), bg_color)
    draw = ImageDraw.Draw(img)

    # 1. Subtle Background Grid Lines
    for x in range(0, 1200, 60):
        draw.line([(x, 0), (x, 630)], fill=(16, 23, 42), width=1)
    for y in range(0, 630, 60):
        draw.line([(0, y), (1200, y)], fill=(16, 23, 42), width=1)

    # 2. Outer Border Frame
    draw.rectangle([(24, 24), (1176, 606)], outline=border_color, width=2)
    # Corner accent ticks
    tick_len = 20
    draw.line([(24, 24), (24 + tick_len, 24)], fill=cyan_accent, width=3)
    draw.line([(24, 24), (24, 24 + tick_len)], fill=cyan_accent, width=3)
    draw.line([(1176, 24), (1176 - tick_len, 24)], fill=cyan_accent, width=3)
    draw.line([(1176, 24), (1176, 24 + tick_len)], fill=cyan_accent, width=3)
    draw.line([(24, 606), (24 + tick_len, 606)], fill=cyan_accent, width=3)
    draw.line([(24, 606), (24, 606 - tick_len)], fill=cyan_accent, width=3)
    draw.line([(1176, 606), (1176 - tick_len, 606)], fill=cyan_accent, width=3)
    draw.line([(1176, 606), (1176, 606 - tick_len)], fill=cyan_accent, width=3)

    # Fonts (Fallback to default if custom ttf unavailable)
    try:
        font_logo = ImageFont.truetype("arialbd.ttf", 26)
        font_title = ImageFont.truetype("arialbd.ttf", 40)
        font_score = ImageFont.truetype("arialbd.ttf", 46)
        font_body = ImageFont.truetype("arial.ttf", 22)
        font_bold = ImageFont.truetype("arialbd.ttf", 22)
        font_sub = ImageFont.truetype("arial.ttf", 18)
    except IOError:
        font_logo = font_title = font_score = font_body = font_bold = font_sub = ImageFont.load_default()

    # 3. Header Branding
    # Guardian Shield Emblem
    shield_pts = [(60, 48), (80, 56), (80, 78), (60, 92), (40, 78), (40, 56)]
    draw.polygon(shield_pts, fill=card_bg, outline=cyan_accent, width=2)
    draw.text((100, 55), "UPI RAKSHAK AI", font=font_logo, fill=cyan_accent)
    draw.text((320, 60), "•  OFFICIAL CITIZEN SAFETY ALERT", font=font_sub, fill=text_muted)

    # 4. Verdict Banner Box
    draw.rounded_rectangle([(60, 115), (780, 195)], radius=12, fill=card_bg, outline=accent_color, width=2)
    draw.text((85, 132), f"VERDICT: {verdict_label}", font=font_title, fill=accent_color)

    # 5. Score Circle Widget
    score_cx, score_cy, score_r = 980, 155, 68
    draw.ellipse(
        [(score_cx - score_r, score_cy - score_r), (score_cx + score_r, score_cy + score_r)],
        fill=card_bg,
        outline=accent_color,
        width=4
    )
    score_text = f"{score}"
    draw.text((score_cx - 26, score_cy - 30), score_text, font=font_score, fill=text_white)
    draw.text((score_cx - 24, score_cy + 18), "/100 RISK", font=font_sub, fill=accent_color)

    # 6. Flagged Message Quote Box
    draw.rounded_rectangle([(60, 220), (1140, 315)], radius=10, fill=card_bg, outline=border_color, width=1)
    draw.text((85, 232), "FLAGGED CONTENT SNIPPET:", font=font_bold, fill=cyan_accent)
    draw.text((85, 265), f'"{safe_snippet}"', font=font_body, fill=text_white)

    # 7. Evidence Bullets
    draw.text((60, 340), "KEY DETECTED THREAT INDICATORS:", font=font_bold, fill=text_white)
    y_pos = 375
    for i, reason in enumerate(reasons[:3]):
        # Bullet pip
        draw.ellipse([(65, y_pos + 6), (75, y_pos + 16)], fill=accent_color)
        draw.text((90, y_pos), f"{reason}", font=font_body, fill=text_white)
        y_pos += 36

    # 8. Golden Rule Advice Footer
    draw.rounded_rectangle([(60, 500), (1140, 580)], radius=10, fill=(18, 30, 58), outline=cyan_accent, width=1)
    draw.text((85, 515), "GOLDEN RULE: Receiving money NEVER requires entering your UPI PIN.", font=font_bold, fill=cyan_accent)
    draw.text((85, 545), "Call 1930 immediately within the Golden Hour | Register at https://cybercrime.gov.in", font=font_sub, fill=text_white)

    # Output to in-memory bytes
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def generate_guardian_avatar_png(size: int = 640) -> bytes:
    """Generates high-res 640x640 guardian avatar PNG for bot profiles and official assets."""
    img = Image.new("RGBA", (size, size), (10, 15, 29, 255))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    r_outer = int(size * 0.42)

    # Outer cyan halo
    draw.ellipse(
        [(cx - r_outer, cy - r_outer), (cx + r_outer, cy + r_outer)],
        outline=(0, 229, 255, 180),
        width=int(size * 0.015)
    )

    # Hexagonal chassis
    import math
    hex_pts = []
    r_hex = int(size * 0.36)
    for i in range(6):
        angle = math.radians(60 * i - 30)
        px = cx + r_hex * math.cos(angle)
        py = cy + r_hex * math.sin(angle)
        hex_pts.append((px, py))

    draw.polygon(hex_pts, fill=(16, 24, 46, 255), outline=(0, 229, 255, 255))

    # Center Shield
    shield_w = int(size * 0.22)
    shield_h = int(size * 0.26)
    s_pts = [
        (cx, cy - shield_h),
        (cx + shield_w, cy - shield_h + int(shield_h * 0.3)),
        (cx + shield_w, cy + int(shield_h * 0.4)),
        (cx, cy + shield_h),
        (cx - shield_w, cy + int(shield_h * 0.4)),
        (cx - shield_w, cy - shield_h + int(shield_h * 0.3))
    ]
    draw.polygon(s_pts, fill=(12, 18, 43, 255), outline=(0, 229, 255, 255))

    # Center lock/check circle
    draw.ellipse(
        [(cx - int(size * 0.08), cy - int(size * 0.08)), (cx + int(size * 0.08), cy + int(size * 0.08))],
        fill=(0, 229, 255, 220)
    )
    draw.ellipse(
        [(cx - int(size * 0.04), cy - int(size * 0.04)), (cx + int(size * 0.04), cy + int(size * 0.04))],
        fill=(10, 15, 29, 255)
    )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
