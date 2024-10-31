from fastapi import FastAPI
from lifespan import lifespan
from api.routers import router

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("프로그램이 사용자에 의해 중단되었습니다.")
