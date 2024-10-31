# API 엔드포인트 정의, 서비스 레이어 호출해 요청 처리 (Spring Boot의 controller 같은 역할)
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from api.doctor_ai.models import AiChatRequest
from openAI.gpt_service import create_prediction_prompt

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "안녕하세요, FastAPI!"}

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@router.post("/api/doctor-ai/chat")
async def doctor_ai_chat(request: AiChatRequest):
    try:
        print(request.content)
        content = create_prediction_prompt(request.content)
        if content is None:
            raise HTTPException(status_code=204, detail="Something went wrong")

        response_data = {
            "status": 200,
            "data": content
        }
    except HTTPException as e:
        response_data = {
            "status": e.status_code,
            "data": "죄송합니다. 오류로 인해 예상 질문이 생성되지 않았습니다. 다시 시도해주세요."
        }
    return JSONResponse(content=response_data)