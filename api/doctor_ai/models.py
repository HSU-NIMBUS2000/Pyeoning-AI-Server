# Spring Boot의 Entity와 유사
# 해당 프로젝트의 FastAPI에서는 DB를 사용하지 않을 것이므로
# Pydantic 모델 정의에 사용 (DTO와 유사)

from pydantic import BaseModel
from typing import List, Dict

# ai 의사 채팅 request model
class AiChatRequest(BaseModel):
    newChat: str
    chatHistory: List[Dict[str, str]]
    prompt: str

# 요약 기능 request model
class AiSummationRequest(BaseModel):
    disease: str # 병명
    chat_history: List[Dict[str, str]] # 채팅 히스토리
