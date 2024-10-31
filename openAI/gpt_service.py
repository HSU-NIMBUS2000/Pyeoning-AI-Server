# OpenAI 관련 로직

import os
import openai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI 설정
OPENAI_KEY = os.getenv("OPENAI_KEY")
# print("Loaded OPENAI_KEY:", OPENAI_KEY)  # 디버깅용-제대로 로드 됨

MODEL = os.getenv("OPENAI_MODEL")
# gpt 통신
def post_gpt(system_content, user_content):
    try:
        openai.api_key = OPENAI_KEY
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "시스템 메시지"},
                {"role": "user", "content": "사용자 입력"}
            ]
        )
        answer = response['choices'][0]['message']['content']
        return answer
    except Exception as e:
        print("Error:", e)
        return None

# 프롬프트 생성 - 예시
def create_prediction_prompt(prompt):
    system_content = "You are a helpful consulting assistant."
    pre_prompt = "한국어로 답변해줘; 해당 자기소개서를 통해 나올 수 있는 예상 질문을 5개 출력해줘; 답변형식은 번호를 붙여서 답변만 한 문장씩 출력해줘; \n\n"
    answer = post_gpt(system_content, pre_prompt + prompt)
    return answer
