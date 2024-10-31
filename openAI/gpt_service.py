import os
import openai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# OpenAI 설정
OPENAI_KEY = os.getenv("OPENAI_KEY")
MODEL = os.getenv("OPENAI_MODEL")

# GPT 통신 함수
def post_gpt(system_content, user_content):
    try:
        # 환경 변수 로드 확인
        print(f"Loaded OPENAI_KEY: {OPENAI_KEY[:5]}... (truncated for security)")
        print(f"Using model: {MODEL}")

        # API 키 설정
        openai.api_key = OPENAI_KEY

        # OpenAI API 호출
        print("Sending request to OpenAI API...")
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
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

# 다양한 프롬프트 생성 - OCP 만족
def create_prompt(system_content, pre_prompt, **kwargs):
    user_input = ""

    # 챗봇 기능일 경우
    if "new_question" in kwargs and "existing_questions" in kwargs:
        user_input = f"{pre_prompt}\n새로운 질문: {kwargs['new_question']}\n기존 질문들: {', '.join(kwargs['existing_questions'])}"

    # 요약 기능일 경우
    elif "conversation_list" in kwargs and "diagnosis" in kwargs:
        # 대화 내용을 문자열로 변환
        conversation_texts = [item['message'] for item in kwargs['conversation_list']]
        user_input = f"{pre_prompt}\n대화 내용: {', '.join(conversation_texts)}\n진단명: {kwargs['diagnosis']}"

    answer = post_gpt(system_content, user_input)
    if answer:
        print("Generated answer successfully")
    else:
        print("Failed to generate answer")
    return answer
