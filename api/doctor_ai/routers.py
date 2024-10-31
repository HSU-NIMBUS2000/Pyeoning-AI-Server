# API 엔드포인트 정의, 서비스 레이어 호출해 요청 처리 (Spring Boot의 controller 같은 역할)
# routers.py

from fastapi import APIRouter
from api.doctor_ai.models import AiChatRequest, AiSummationRequest
from openAI.gpt_service import create_prompt

router = APIRouter()

# 챗봇 기능 라우터
@router.post("/api/doctor-ai/chatbot")
async def chatbot_function(request: AiChatRequest):
    system_content = "You are an AI-powered psychiatrist chatbot."
    pre_prompt = request.prompt
    response = create_prompt(
        system_content,
        pre_prompt,
        new_question=request.newChat,
        existing_questions=request.chatHistory
    )
    return {"response": response}

# 요약 기능 라우터
@router.post("/api/doctor-ai/summarize")
async def summary_function(request: AiSummationRequest):
    system_content = "You are a medical assistant specializing in summarizing patient interactions."
    pre_prompt = f"{request.disease} 관련 대화 내용을 요약합니다:"
    response = create_prompt(
        system_content=system_content,
        pre_prompt=pre_prompt,
        conversation_list=request.chat_history,
        diagnosis=request.disease
    )
    return {"response": response}
