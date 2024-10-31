# 앱의 수명 주기를 관리
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행될 코드
    print("애플리케이션이 시작되었습니다.")
    yield
    # 종료 시 실행될 코드
    print("애플리케이션이 종료되었습니다.")
