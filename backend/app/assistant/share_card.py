"""
Server-Side Shareable 'Scam Alert' Card Generator (Pillow).
Generates high-resolution 1200x630 OpenGraph / social share cards in < 50ms.
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
    Renders a 1200x630 PNG image buffer suitable for Telegram and web social sharing.
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

    # Colors - Midnight Navy + Gold + Teal theme palette
    is_high = verdict.upper() in ["HIGH RISK", "DANGER"] or score >= 70
    is_suspicious = verdict.upper() in ["SUSPICIOUS", "WARNING"] or (score >= 35 and score < 70)

    if is_high:
        accent_color = (244, 63, 94)       # Semantic High Risk #F43F5E
        accent_glow = (244, 63, 94, 40)
        verdict_label = "HIGH RISK SCAM"
    elif is_suspicious:
        accent_color = (251, 146, 60)      # Semantic Suspicious #FB923C (distinct orange)
        accent_glow = (251, 146, 60, 40)
        verdict_label = "SUSPICIOUS THREAT"
    else:
        accent_color = (52, 211, 153)      # Semantic Safe #34D399
        accent_glow = (52, 211, 153, 40)
        verdict_label = "LIKELY SAFE"

    bg_color = (5, 10, 24)                 # Deep Midnight Navy #050A18
    card_bg = (15, 29, 58)                 # Surface Card Navy #0F1D3A
    border_color = (30, 58, 95)            # Navy Border #1E3A5F
    teal_accent = (53, 208, 200)           # Shield Teal #35D0C8
    gold_accent = (217, 164, 65)           # Brand Gold #D9A441
    gold_light = (245, 201, 106)           # Gold-400 #F5C96A
    text_white = (245, 241, 230)           # Warm White #F5F1E6
    text_muted = (169, 180, 204)           # Slate Muted #A9B4CC

    # Create base canvas
    img = Image.new("RGB", (1200, 630), bg_color)
    draw = ImageDraw.Draw(img)

    # 1. Subtle Background Grid Lines
    for x in range(0, 1200, 60):
        draw.line([(x, 0), (x, 630)], fill=(11, 21, 48), width=1)
    for y in range(0, 630, 60):
        draw.line([(0, y), (1200, y)], fill=(11, 21, 48), width=1)

    # 2. Outer Border Frame
    draw.rectangle([(24, 24), (1176, 606)], outline=border_color, width=2)
    # Corner accent ticks in brand Gold
    tick_len = 22
    draw.line([(24, 24), (24 + tick_len, 24)], fill=gold_accent, width=3)
    draw.line([(24, 24), (24, 24 + tick_len)], fill=gold_accent, width=3)
    draw.line([(1176, 24), (1176 - tick_len, 24)], fill=gold_accent, width=3)
    draw.line([(1176, 24), (1176, 24 + tick_len)], fill=gold_accent, width=3)
    draw.line([(24, 606), (24 + tick_len, 606)], fill=gold_accent, width=3)
    draw.line([(24, 606), (24, 606 - tick_len)], fill=gold_accent, width=3)
    draw.line([(1176, 606), (1176 - tick_len, 606)], fill=gold_accent, width=3)
    draw.line([(1176, 606), (1176, 606 - tick_len)], fill=gold_accent, width=3)

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
    # Guardian Shield Emblem (Teal Shield + Gold Accent Rim)
    shield_pts = [(60, 48), (80, 56), (80, 78), (60, 92), (40, 78), (40, 56)]
    draw.polygon(shield_pts, fill=card_bg, outline=teal_accent, width=2)
    draw.text((100, 55), "UPI RAKSHAK AI", font=font_logo, fill=gold_light)
    draw.text((330, 60), "•  OFFICIAL CITIZEN SAFETY ALERT", font=font_sub, fill=text_muted)

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
    draw.rounded_rectangle([(60, 220), (1140, 315)], radius=12, fill=card_bg, outline=border_color, width=1)
    draw.text((85, 232), "FLAGGED CONTENT SNIPPET:", font=font_bold, fill=teal_accent)
    draw.text((85, 265), f'"{safe_snippet}"', font=font_body, fill=text_white)

    # 7. Evidence Bullets
    draw.text((60, 340), "KEY DETECTED THREAT INDICATORS:", font=font_bold, fill=gold_light)
    y_pos = 375
    for i, reason in enumerate(reasons[:3]):
        # Bullet pip
        draw.ellipse([(65, y_pos + 6), (75, y_pos + 16)], fill=accent_color)
        draw.text((90, y_pos), f"{reason}", font=font_body, fill=text_white)
        y_pos += 36

    # 8. Golden Rule Advice Footer
    draw.rounded_rectangle([(60, 500), (1140, 580)], radius=12, fill=(11, 21, 48), outline=teal_accent, width=1)
    # Thin gold top bar
    draw.line([(72, 500), (1128, 500)], fill=gold_accent, width=2)
    draw.text((85, 515), "GOLDEN RULE: Receiving money NEVER requires entering your UPI PIN.", font=font_bold, fill=gold_light)
    draw.text((85, 545), "Call 1930 immediately within the Golden Hour | Register at https://cybercrime.gov.in", font=font_sub, fill=text_white)

    # Output to in-memory bytes
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def generate_guardian_avatar_png(size: int = 640) -> bytes:
    """Generates high-res 640x640 guardian avatar PNG for bot profiles and official assets in Midnight Navy + Gold + Teal."""
    img = Image.new("RGBA", (size, size), (5, 10, 24, 255))
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2
    r_outer = int(size * 0.44)

    # Outer teal glow halo
    draw.ellipse(
        [(cx - r_outer, cy - r_outer), (cx + r_outer, cy + r_outer)],
        outline=(53, 208, 200, 160),
        width=int(size * 0.015)
    )

    # Hexagonal chassis with Gold rim
    import math
    hex_pts = []
    r_hex = int(size * 0.38)
    for i in range(6):
        angle = math.radians(60 * i - 30)
        px = cx + r_hex * math.cos(angle)
        py = cy + r_hex * math.sin(angle)
        hex_pts.append((px, py))

    draw.polygon(hex_pts, fill=(15, 29, 58, 255), outline=(217, 164, 65, 255))

    # Center Shield with Teal Rim
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
    draw.polygon(s_pts, fill=(11, 21, 48, 255), outline=(53, 208, 200, 255))

    # Center Gold emblem circle
    draw.ellipse(
        [(cx - int(size * 0.08), cy - int(size * 0.08)), (cx + int(size * 0.08), cy + int(size * 0.08))],
        fill=(245, 201, 106, 230),
        outline=(53, 208, 200, 255)
    )
    draw.ellipse(
        [(cx - int(size * 0.04), cy - int(size * 0.04)), (cx + int(size * 0.04), cy + int(size * 0.04))],
        fill=(5, 10, 24, 255)
    )

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
