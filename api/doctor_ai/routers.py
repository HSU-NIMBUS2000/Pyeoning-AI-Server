# API 엔드포인트 정의, 서비스 레이어 호출해 요청 처리 (Spring Boot의 controller 같은 역할)
# routers.py

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from api.doctor_ai.models import AiChatRequest, AiSummationRequest
from openAI.gpt_service import create_prompt

router = APIRouter()

# 챗봇 기능 라우터
@router.post("/api/doctor-ai/chatbot")
async def chatbot_function(request: AiChatRequest):

    # 400 (새로운 질문 없음)
    if not request.newChat:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "data": None,
                "message": "새로운 질문이 없습니다."
            }
        )

    # 모델의 역할에 대한 전반적인 지침 (변하지 않는 것)
    system_content = (
        "당신은 전문 정신과 의사처럼 환자와 대화하는 AI입니다. 의사 지침을 반영하여 채팅을 진행하세요:\n"
        "다음에 맞는 답변을 생성해주세요. "
        "환자의 감정을 존중하며, 대화를 이끌어갈 때는 다음을 기억하세요: "
        "1) 말이 이어지도록 답장을 해주세요."
        "2) 환자가 친구처럼 편안함을 느낄 수 있도록 자연스럽고 대화가 이어지도록 생성해주세요."
        "3) 답변은 10~50자 정도를 유지하고 간결하게 표현하세요.\n\n"
        ""
        "##예시1"
        "[병명]"
        "우울장애, 불안장애"
        "[의사 지침]"
        "1. 자존감이 낮아져 있는 상태이므로, 주변에서 긍정적인 피드백을 받을 때 조금 더 자신감을 얻을 수 있음. 그래서 환자가 노력한 부분이나 잘해낸 일에 대해 칭찬과 인정을 해주는 것이 중요함."
        "2. 혼자 있는 시간이 많기 때문에, 소규모의 안전한 사회적 관계를 유지하고 서서히 확장해나가는 것이 필요함. 큰 모임이나 낯선 사람들과의 만남은 부담스러울 수 있으니, 가까운 친구나 가족과의 시간을 더 많이 가질 수 있도록 독려하는 것이 좋음."
        "3. 불안해하는 상황에 너무 자주 직면하게 되면 오히려 증상이 악화될 수 있음. 그래서 불안감을 유발하는 상황을 서서히 노출하는 방식으로 접근해야 함. 직장에서나 일상생활에서 무리하게 그를 몰아붙이기보다는, 차분한 환경에서 그의 속도에 맞게 일하도록 유도하는 것이 중요함."
        "[대화 내역]"
        "김환자 : 오늘은 날씨가 맑아서 기분이 아주 좋았고 행복하고 아주 즐거웠던 하루야"
        "펴닝: 기분이 아주 좋았다니 다행이에요! 가끔은 가벼운 산책을 하는 것도 좋아요!"
        "김환자 : 내일은 조깅을 한번 나가볼까 고민중이야!?"
        "펴닝 : 조깅 너무 좋죠! 달리기에 흥미가 있으신가요? "
        "[새로운 환자의 메시지]"
        "김환자 : 웅 나 달리기 완전 잘해. 초등학교때 달리기 시합에서 1등했었어. 히히"
        "[답변]"
        "우와~ 대박이신데요? 지금도 엄청 잘 달리실 거 같아요! 달리면 스트레스도 풀리고, 몸도 건강해지고 정말 좋은 것 같아요! 혹시 마지막으로 달려본게 언제이신가요?"
    )

    # 대화 내용을 문자열로 변환
    conversation_chatHistory = convert_chat_history_to_string(request.chatHistory)

    # 구체적인 가이드 작성 (변하는 것)
    prompt = (
        "[병명]"
        f'{request.disease}\n'
        "[의사 지침]"
        f" {request.prompt}\n\n"
        "다음은 환자와의 기존 대화 내역입니다. 과거의 대화 흐름과 환자의 감정 상태를 고려하여, 자연스럽게 답변을 작성해 주세요:\n"
        "[대화 내역]"
        f" {conversation_chatHistory}\n\n"
        "[새로운 환자의 메시지]"
        f"'{request.newChat}'"
        "불필요한 내용은 제외해 주세요. 오로지 새로운 메세지 내용만 생성해주세요.\n\n"
        "[답변]"
    )

    # AI 응답 생성
    new_chat = create_prompt(
        system_content=system_content,
        prompt=prompt
    )

    # 200 (AI 응답 생성 성공)
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "data": {
                "newChat": new_chat
            },
            "message": "AI 응답이 성공적으로 생성되었습니다."
        }
    )

# 요약 기능 라우터
@router.post("/api/doctor-ai/summarize")
async def summary_function(request: AiSummationRequest):
    # 400 (대화 내용 필요)
    if not request.chatHistory:
        return JSONResponse(
            status_code=400,
            content={
                "status": 400,
                "data": None,
                "message": "요약을 위한 대화 내용이 필요합니다."
            }
        )

    # 400 (병명 필요)
    if not request.disease:
        if not request.disease:
            return JSONResponse(
                status_code=400,
                content={
                    "status": 400,
                    "data": None,
                    "message": "정확한 요약을 위해 병명이 필요합니다."
                }
            )

    # 모델이 어떤 역할을 수행할지 설정
    system_content = (
        "당신은 환자의 병명과 대화 기록을 바탕으로, 대화의 핵심 내용을 간결하고 정확하게 요약하는 "
        "전문 의료 보조 인공지능입니다. 요약은 담당 정신과 의사가 진료에 활용할 수 있도록 한글로 제공해 주세요. "
        "요약본은 다음 사항을 포함해야 합니다."
        "1) 주요 감정 상태"
        "2) 환자의 주된 고민이나 증상"
        "3) 앞으로 상담을 할 때 참고하면 좋을 사항"
        "최대한 간략히 정리해 주세요. 정보가 많다면 요약이 길어져도 괜찮습니다. 다만, 환자의 상황을 명확히 이해할 수 있도록 구조화하고 "
        "불필요한 내용은 제외해 주세요. 오로지 요약본만 생성해주세요."
        "내용이 부족하다면 아주 간략하게 요약해주세요.\n\n"
        "### 예시1\n"
        "[병명]"
        "우울장애, 불안장애\n"
        "[대화 내역]"
        "김환자: 최근 업무에서 작은 실수를 했는데, 계속 자책하게 돼요. 그 실수만 생각하면 스트레스를 받아요."
        "펴닝: 완벽주의적인 성향 때문에 더 힘들게 느껴질 수 있어요. 그럴 땐 작은 성취에도 자신을 격려해보는 연습을 해보는 게 좋을 것 같아요. 스스로 “충분히 잘해냈다”고 말해보면 어떨까요?"
        "김환자: 해보려고는 하지만, 제 자신을 그렇게 쉽게 용서하기가 어렵네요. 그리고 다른 사람들과 만나는 것도 불안해서 자꾸 피하게 돼요."
        "펴닝: 사회적 불안은 천천히 극복하는 게 중요해요. 가까운 친구들과의 소규모 만남부터 시작해보면 좋을 것 같습니다. 너무 큰 모임은 피하되, 천천히 자신감을 쌓아가면 돼요."
        "김환자: 요즘 수면도 문제예요. 밤에 잠을 제대로 못 자거나 자주 깨서 피곤해요. 중요한 업무가 있었던 날은 더 심해요."
        "펴닝: 수면 문제는 업무 스트레스와 연관이 있어 보이네요. 자기 전에 5분 정도 간단한 명상이나 호흡법을 시도해보는 건 어떨까요? 안정감을 찾는 데 도움이 될 수 있어요."
        "김환자: 좋은 생각 같아요. 그걸 한번 해볼게요.\n"
        "[답변]"
        "해당 환자는 자신의 업무에서 실수를 했을 때 자책하는 경향이 강하였습니다."
        "특히, 완벽주의적인 성향으로 인해 작은 실수조차 큰 스트레스로 다가오며, 이를 계속해서 반추하며 스스로를 비판하는 모습을 보였습니다."
        "또한, 환자는 사회적 상황에서도 자신이 타인에게 어떻게 보일지에 대한 불안감이 커, 대인관계를 피하게 되고, 그 결과 혼자만의 시간을 보내는 경우가 많아지고 있었습니다."
        "이로 인해 외로움과 사회적 고립감이 심해지는 경향이 관찰되었습니다."
        "환자는 수면 문제도 겪고 있었습니다."
        "업무에서의 스트레스와 불안으로 인해 밤에 잠을 이루지 못하거나 자주 깨는 수면 패턴이 반복되고 있었습니다."
        "특히 중요한 업무나 실수가 있었던 날은 불안이 극대화되어 수면의 질이 더 낮아지는 경향이 있었습니다."
        "이로 인해 피로감이 누적되고, 이는 일상생활과 정서적인 안정을 방해하는 요인으로 작용하고 있었습니다."
        "환자는 이러한 수면 문제를 해결하고자 하는 의지를 표현하였으나, 구체적인 방법을 찾지 못하고 있는 상태였습니다."
        "해당 환자에게는 자신을 지나치게 비판하는 경향을 줄이기 위해, 작은 성취에도 긍정적인 피드백을 줄 것을 권장하였습니다."
        "상담 중에는 스스로에게 “충분히 잘해냈다”라고 말하는 연습을 하도록 제안하였고, 환자도 이를 시도해보겠다는 긍정적인 반응을 보였습니다."
        "사회적 불안에 대해서는 큰 모임을 피하되, 가까운 친구와의 소규모 만남부터 천천히 재개하는 방법을 제안하였습니다."
        "또한, 수면 문제를 해결하기 위해 잠들기 전 5분 정도 간단한 명상이나 호흡법을 시도해보도록 권유하였습니다."
        "환자는 이러한 권장 사항들을 긍정적으로 받아들였으며, 이를 실천해보겠다고 하였습니다."
    )

    # 대화 내역을 문자열로 변환
    conversation_chatHistory = convert_chat_history_to_string(request.chatHistory)

    # 구체적인 가이드 작성 (변하는 것)
    prompt = (
        "[병명]"
        f"'{request.disease}'"
        "[대화 내역]"
        f"{conversation_chatHistory}\n\n"
        "불필요한 내용은 제외해 주세요. 오로지 요약보고서만 생성해주세요."
        "[답변]"
    )

    # AI 응답 생성
    summary = create_prompt(
        system_content=system_content,
        prompt=prompt
    )

    # 200 (요약 보고서 생성 성공)
    return JSONResponse(
        status_code=200,
        content={
            "status": 200,
            "data": {
                "summary": summary
            },
            "message": "요약 보고서가 성공적으로 생성되었습니다."
        }
    )


# 각 대화 내용을 문자열로 변환하는 메서드
def convert_chat_history_to_string(chat_history):
    conversation_chatHistory = "\n".join(
        f"{message['sender']}: {message['message']}" for message in chat_history
    )
    return conversation_chatHistory