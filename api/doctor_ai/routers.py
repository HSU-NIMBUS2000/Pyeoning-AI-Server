# API 엔드포인트 정의, 서비스 레이어 호출해 요청 처리 (Spring Boot의 controller 같은 역할)
# routers.py

from fastapi import APIRouter, HTTPException
from api.doctor_ai.models import AiChatRequest, AiSummationRequest
from openAI.gpt_service import create_prompt

router = APIRouter()

# 챗봇 기능 라우터
@router.post("/api/doctor-ai/chatbot")
async def chatbot_function(request: AiChatRequest):

    # 400 (새로운 질문 없음)
    if not request.newChat:
        raise HTTPException(
            status_code=400,
            detail={
                "status": 400,
                "data": None,
                "message": "새로운 질문이 없습니다."
            }
        )

    # 모델의 역할에 대한 전반적인 지침 (변하지 않는 것)
    system_content = (
        "당신은 전문 정신과 의사처럼 환자와 대화하는 AI입니다. "
        "환자가 자신의 감정을 표현할 때 진심으로 귀 기울이고, 필요한 경우 위로하거나 공감하는 말을 건네세요. "
        "대화는 딱딱하지 않고, 환자가 친구처럼 편안함을 느낄 수 있도록 부드럽고 자연스럽게 이어지도록 진행합니다. "
        "환자의 감정을 존중하며, 대화를 이끌어갈 때는 다음을 기억하세요: "
        "1) 상대방의 말을 받아들이고 이어가며 공감하기,"
        "2) 힘든 점에 대해 자세히 묻고, 상대가 편하게 말할 수 있도록 분위기를 조성하기, "
        "3) 필요할 때 작은 긍정의 씨앗을 심어 희망을 느낄 수 있도록 격려하기."
    )

    # 대화 내용을 문자열로 변환
    conversation_chatHistory = convert_chat_history_to_string(request.chatHistory)

    # 더 구체적인 가이드 (변하는 것)
    prompt = (
        f"환자는 '{request.disease}' 병을 앓고 있습니다. "
        "아래는 환자의 담당 의사가 제공한 지침입니다. 이를 반드시 반영하여 대화를 진행하세요:\n"
        f"의사 지침: {request.prompt}\n\n"
        "다음은 환자와의 기존 대화 내역입니다. 과거의 대화 흐름과 환자의 감정 상태를 고려하여, 자연스럽고 공감이 담긴 답변을 작성해 주세요:\n"
        f"대화 내역: {conversation_chatHistory}\n\n"
        f"현재 환자의 메시지: '{request.newChat}'에 대한 답변을 생성합니다. "
        "환자가 자신의 감정을 이해받고 있다고 느끼도록 공감적이고 부드러운 톤으로 답변해 주세요. "
    )

    response = create_prompt(
        system_content=system_content,
        prompt=prompt
    )

    # 200 (AI 응답 생성 성공)
    return {
        "status": 200,
        "data": {
            "response": response
        },
        "message": "AI 응답이 성공적으로 생성되었습니다."
    }

# 요약 기능 라우터
@router.post("/api/doctor-ai/summarize")
async def summary_function(request: AiSummationRequest):
    # 400 (대화 내용 필요)
    if not request.chatHistory:
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
        prompt=prompt,
    )

    # 200 (요약 보고서 생성 성공)
    return {
        "status": 200,
        "data": {
            "summary": summary
        },
        "message": "요약 보고서가 성공적으로 생성되었습니다."
    }




def convert_chat_history_to_string(chat_history):
    # 각 대화 내용을 문자열로 변환
    conversation_chatHistory = "\n".join(
        f"{message['sender']}: {message['message']}" for message in chat_history
    )
    return conversation_chatHistory