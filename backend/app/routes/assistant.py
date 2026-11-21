from fastapi import APIRouter, Depends
from ..models.schemas import AssistantChatRequest, AssistantChatResponse
from ..assistant.service import assistant_service
from ..core.security import rate_limiter

router = APIRouter(prefix="/assistant", tags=["Multilingual Assistant"])

@router.post("/chat", response_model=AssistantChatResponse, dependencies=[Depends(rate_limiter)])
def chat(req: AssistantChatRequest):
    return assistant_service.analyze_and_respond(req)
