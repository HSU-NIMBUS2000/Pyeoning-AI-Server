import os
import openai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI 설정
OPENAI_KEY = os.getenv("OPENAI_KEY")
MODEL = os.getenv("OPENAI_MODEL")

# gpt 통신
def post_gpt(system_content, user_content):
    try:
        # 환경 변수 로드 확인
        print(f"Loaded OPENAI_KEY: {OPENAI_KEY[:5]}... (truncated for security)")
        print(f"Using model: {MODEL}")

        # API 키 설정
        openai.api_key = OPENAI_KEY

        # 새로운 OpenAI API 호출 방식
        print("Sending request to OpenAI API...")
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_content},  # 시스템 메시지
                {"role": "user", "content": user_content}       # 사용자 입력
            ],
            temperature=0.5
        )
        print("Received response from OpenAI API")

        # 응답에서 답변 추출
        answer = response['choices'][0]['message']['content']
        print("Extracted answer:", answer)
        return answer
    except Exception as e:
        print("Error:", e)
        return None

# 프롬프트 생성 - 예시
def create_prediction_prompt(prompt):
    print("Generating prediction prompt...")
    system_content = "You are a helpful consulting assistant."
    pre_prompt = "한국어로 답변해줘; 해당 자기소개서를 통해 나올 수 있는 예상 질문을 5개 출력해줘; 답변형식은 번호를 붙여서 답변만 한 문장씩 출력해줘; \n\n"
    answer = post_gpt(system_content, pre_prompt + prompt)
    if answer:
        print("Generated answer successfully")
    else:
        print("Failed to generate answer")
    return answer
