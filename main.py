from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행될 코드
    print("애플리케이션이 시작되었습니다.")
    yield
    # 종료 시 실행될 코드
    print("애플리케이션이 종료되었습니다.")

app = FastAPI(lifespan=lifespan)

# 예시 - 참고해서 코드 짜기 -----------------------
@app.get("/")
async def root():
    return {"message": "안녕하세요, FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
# --------------------------------------------

# 의사 AI 와의 채팅 기능
@app.post("/api/doctor-ai/chat")
async def doctor_ai_chat():
    return {"답변답변"}







if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000) #8000 포트에서 실행
    except KeyboardInterrupt:
        print("프로그램이 사용자에 의해 중단되었습니다.")