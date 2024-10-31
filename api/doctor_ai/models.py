# Spring Boot의 Entity와 유사
# 해당 프로젝트의 FastAPI에서는 DB를 사용하지 않을 것이므로
# Pydantic 모델 정의에 사용 (DTO와 유사)
from pydantic import BaseModel

# ai 의사 채팅 request model
class AiChatRequest(BaseModel):
    content: str
