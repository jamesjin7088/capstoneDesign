from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from detect.detect_colors import get_dominant_colors
from detect.detect_colors import extract_colors
from ultralytics import YOLO

from dotenv import load_dotenv
load_dotenv()

import os
import time
import cv2

# import google.generativeai as genai
#
# google_api_key = os.getenv('GOOGLE_API_KEY')
# genai.configure(api_key = google_api_key)
#
# model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
#
# chat = model.start_chat()

app = FastAPI()

origins = [
    "http://127.0.0.1:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def hello():
    return {"message": "Hello World"}

@app.post("/image")
async def create_file(file: UploadFile):
    # 업로드된 파일 읽기
    content = await file.read()

    # 업로드 디렉토리 생성
    UPLOAD_DIR = os.path.abspath("uploads")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 파일명 생성 (시간 기반으로 고유한 파일명 생성)
    timestamp = int(time.time())
    file_extension = os.path.splitext(file.filename) [1]
    unique_filename = f"{timestamp}{file_extension}"

    # 파일 저장
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as f:
        f.write(content)

    # 이미지 읽기 및 확인
    img = cv2.imread(file_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # YOLO 모델 로드
    model = YOLO("yolo11m.pt")

    # 객체 검출
    results = model(img)

    # 객체 검출 후 박스 정보 추출

    boxes = []
    object_names = []
    # for result in results:
    #     for box in result.boxes:
    #         if box.conf[0] >= 0.4:
    #             boxes.append(box)
    #             object_names.append(result.names[int(box.cls[0])])


    dominant_colors = get_dominant_colors(img)
    hex_colors = ['#%02x%02x%02x' % (color[0], color[1], color[2]) for color in dominant_colors]

    # object_palette, background_palette = extract_colors(img_rgb, boxes)


    return {
            "filename": file.filename,
            "saved_path": file_path,
            "dominant_colors": hex_colors,
            # "object_palette": object_palette,
            # "background_palette": background_palette
        }






# uvicorn main:app --reload