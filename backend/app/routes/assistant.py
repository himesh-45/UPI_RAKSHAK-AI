from fastapi import APIRouter, Depends, Query, Response
from typing import Optional, List
from ..models.schemas import AssistantChatRequest, AssistantChatResponse
from ..assistant.service import assistant_service
from ..assistant.share_card import generate_scam_alert_card, generate_guardian_avatar_png
from ..core.security import rate_limiter

router = APIRouter(prefix="/assistant", tags=["Multilingual Assistant"])

@router.post("/chat", response_model=AssistantChatResponse, dependencies=[Depends(rate_limiter)])
def chat(req: AssistantChatRequest):
    return assistant_service.analyze_and_respond(req)

@router.get("/share-card", dependencies=[Depends(rate_limiter)])
def get_share_card(
    verdict: str = Query("HIGH RISK", description="Verdict: HIGH RISK, SUSPICIOUS, SAFE"),
    score: int = Query(87, ge=0, le=100, description="Risk Score 0-100"),
    text: str = Query("Electricity disconnection notice tonight at 9:30 PM", description="Message text snippet"),
    language: str = Query("en", description="Language code: en, hi, te")
):
    """
    Renders a fast (< 50ms) server-side 1200x630 PNG card for family WhatsApp/Telegram sharing.
    """
    png_bytes = generate_scam_alert_card(
        verdict=verdict,
        score=score,
        message_snippet=text,
        language=language
    )
    return Response(content=png_bytes, media_type="image/png")

@router.get("/avatar")
def get_guardian_avatar(size: int = Query(640, ge=64, le=1024)):
    """
    Returns the official 640x640 guardian avatar PNG for bot profiles and official branding.
    """
    avatar_png = generate_guardian_avatar_png(size=size)
    return Response(content=avatar_png, media_type="image/png")
