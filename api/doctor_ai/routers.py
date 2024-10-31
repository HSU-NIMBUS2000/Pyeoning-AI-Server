# API 엔드포인트 정의, 서비스 레이어 호출해 요청 처리 (Spring Boot의 controller 같은 역할)
# routers.py

from fastapi import APIRouter, HTTPException
from api.doctor_ai.models import AiChatRequest, AiSummationRequest
from openAI.gpt_service import create_prompt

router = APIRouter()

# 챗봇 기능 라우터
@router.post("/api/doctor-ai/chatbot")
async def chatbot_function(request: AiChatRequest):
    # 모델이 어떤 역할을 수행할 지 설정
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
    # 400 (대화 내용 필요)
    if not request.chat_history:
        raise HTTPException(
            status_code=400,
            detail={
                "status": 400,
                "data": None,
                "message": "요약을 위한 대화 내용이 필요합니다."
            }
        )

    # 400 (병명 필요)
    if not request.disease:
        if not request.disease:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": 400,
                    "data": None,
                    "message": "정확한 요약을 위해 병명이 필요합니다."
                }
            )

    # 모델이 어떤 역할을 수행할지 설정
    system_content = (
        "당신은 환자의 병명과 대화 기록을 바탕으로, 대화의 핵심 내용을 간결하고 정확하게 요약하는 "
        "전문 의료 보조 인공지능입니다. 요약은 담당 정신과 의사가 진료에 활용할 수 있도록 한글로 제공해 주세요. "
        "요약본은 다음 사항을 포함해야 합니다: 1) 주요 감정 상태, 2) 환자의 주된 고민이나 증상, 3) 마지막으로 중요한 상담 포인트를 "
        "한 줄로 간략히 정리해 주세요. 정보가 많다면 요약이 길어져도 괜찮습니다. 다만, 환자의 상황을 명확히 이해할 수 있도록 구조화하고 "
        "불필요한 내용은 제외해 주세요. 오로지 요약본만 생성해주세요."
    )

    pre_prompt = f"'{request.disease}'를 앓고 있는 환자의 대화 내용을 요약합니다:"
    summary = create_prompt(
        system_content=system_content,
        pre_prompt=pre_prompt,
        conversation_list=request.chat_history,
        diagnosis=request.disease
    )

    # 200 (요약 보고서 생성 성공)
    return {
        "status": 200,
        "data": {
            "summary": summary
        },
        "message": "요약 보고서가 성공적으로 생성되었습니다."
    }