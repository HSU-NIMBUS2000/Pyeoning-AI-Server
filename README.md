# 펴닝 - AI 서버
![시작페이지](https://github.com/user-attachments/assets/6a1d76d3-0555-4f7a-9dea-9cb311858373)

## 소개
LLM을 활용한 AI 정신과 의사 서비스의 AI 서버 부분. FastAPI를 사용하여 구현되었으며, 환자와 AI 의사 간의 대화를 처리.

## 기능
- AI 의사 응답 생성
- 대화 내용 위험도 평가
- 개인화된 프롬프트 처리

## 시스템 요구사항
- Python 3.8+
- FastAPI
- Uvicorn
- 기타 필요한 라이브러리 (requirements.txt 참조)

## 설치 방법
1. 저장소 클론:
   ```
   git clone [저장소 URL]
   ```
2. 프로젝트 디렉토리로 이동:
   ```
   cd [프로젝트 디렉토리]
   ```
3. 가상 환경을 생성하고 활성화:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows의 경우: venv\Scripts\activate
   ```
4. 필요한 패키지를 설치:
   ```
   pip install -r requirements.txt
   ```

## 실행 방법
1. 서버를 시작:
   ```
   uvicorn main:app --reload
   ```
2. 브라우저에서 `http://localhost:8000/docs`에 접속하여 Swagger UI를 통해 API를 테스트 가능.

## API 엔드포인트
- POST /api/doctor-ai/chat: AI 의사 채팅 응답 생성

## 환경 변수
- `LLM_API_KEY`: LLM API 키
- `DATABASE_URL`: 데이터베이스 연결 URL

## 기여 방법
1. 포크
2. 새 브랜치를 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 푸시 (`git push origin feature/AmazingFeature`)
5. Pull Request를 생성
