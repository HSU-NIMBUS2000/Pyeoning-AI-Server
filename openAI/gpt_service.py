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
        # 환경 변수 매핑 확인
        print(f"Loaded OPENAI_KEY: {OPENAI_KEY[:5]}... (truncated for security)")
        print(f"Using model: {MODEL}")

        # 프롬프트 확인
        print("system_content: ", system_content) # 모델이 어떤 역할을 수행할 지 설정
        print("user_content: ", user_content) # 사용자 요청이나 질문을 설정

        # API 키 설정
        openai.api_key = OPENAI_KEY

        # OpenAI API 호출
        print("OpenAI API에게 요청 보내는 중")
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            temperature=0.5
        )
        print("OpenAI API로부터 응답 받음")

        # 응답에서 답변 추출
        answer = response['choices'][0]['message']['content']
        print("openAI 응답 :", answer)
        return answer
    except Exception as e:
        print("openAI 응답 오류 발생 :", e)
        return None

# 다양한 프롬프트 생성 - OCP 만족하도록 나중에 수정할 것
def create_prompt(system_content, pre_prompt, **kwargs):

    # 사용자 요청이나 질문을 설정
    user_input = ""

    # 챗봇 기능일 경우
    if "new_question" in kwargs and "existing_questions" in kwargs:
        user_input = f"{pre_prompt}\n새로운 질문: {kwargs['new_question']}\n기존 질문들: {', '.join(kwargs['existing_questions'])}"

    # 요약 기능일 경우
    elif "conversation_list" in kwargs and "diagnosis" in kwargs:
        # 대화 내용을 문자열로 변환
        conversation_texts = "\n".join(
            [f"{item['sender']}: {item['message']}" for item in kwargs["conversation_list"]]
        )
        user_input = f"{pre_prompt}\n대화 내용:\n{conversation_texts}"

    # OpenAI API 호출
    answer = post_gpt(system_content, user_input)

    if answer:
        print("openAI 응답 생성 성공")
    else:
        print("openAI 응답 생성 실패")
    return answer
