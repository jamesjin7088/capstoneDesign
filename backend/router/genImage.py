from fastapi import APIRouter
from dotenv import load_dotenv
import openai
import webbrowser
import os

# .env 파일 로드
load_dotenv()

# API 키 가져오기
api_key = os.environ.get('OPENAI_API_KEY')

# 가져온 API 키 사용
if api_key:
    print(f"API 키 : {api_key}")
else:
    print("API 키를 찾을 수 없습니다.")

client = openai.OpenAI(api_key = api_key)



