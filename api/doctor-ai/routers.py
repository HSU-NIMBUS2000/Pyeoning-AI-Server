# API 엔드포인트 정의, 서비스 레이어 호출해 요청 처리 (Spring Boot의 controller 같은 역할)

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "안녕하세요, FastAPI!"}

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@router.post("/api/doctor-ai/chat")
async def doctor_ai_chat():
    return {"답변답변"}
