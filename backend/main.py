from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from detect.detect_new import get_dominant_colors

from ultralytics import YOLO

from dotenv import load_dotenv
load_dotenv()

import os
import time
import cv2

from openai import OpenAI
client = OpenAI()



app = FastAPI()

origins = [
    "http://localhost:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 이미지 분석 API
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
    for result in results:
        for box in result.boxes:
            if box.conf[0] >= 0.4:
                boxes.append(box)
                object_names.append(result.names[int(box.cls[0])])


    dominant_colors = get_dominant_colors(img)
    hex_colors = ['#%02x%02x%02x' % (color[0], color[1], color[2]) for color in dominant_colors]

    # object_palette, background_palette = extract_colors(img_rgb, boxes)


    return {
            "filename": file.filename,
            "saved_path": file_path,
            "dominant_colors": hex_colors,
            # "object_palette": object_palette,
            # "background_palette": background_palette,
            "object_names": object_names,
        }


# 이미지 변형 생성 API
@app.post("/image/variation")
async def create_image_variation(
    file_path: str,  # 이미 저장된 이미지의 경로
    prompt: str      # 사용자가 입력한 프롬프트
):
    # 생성된 이미지를 저장할 디렉토리 생성
    GENERATED_DIR = os.path.abspath("generated_images")
    os.makedirs(GENERATED_DIR, exist_ok=True)

    try:
        # 저장된 이미지 파일 열기
        with open(file_path, "rb") as image_file:
            response = client.images.create_edit(
                image=image_file,
                prompt=prompt,
                n=1,                # 생성할 이미지 수
                size="1024x1024",   # 이미지 크기
                model="dall-e-2"    # DALL-E 2 모델 사용
            )

        # 생성된 이미지 URL에서 이미지 다운로드 및 저장
        generated_image_url = response.data[0].url
        
        # 생성된 이미지의 파일명 생성 (시간 기반)
        timestamp = int(time.time())
        generated_filename = f"generated_{timestamp}.png"
        generated_path = os.path.join(GENERATED_DIR, generated_filename)

        # 생성된 이미지 URL에서 이미지 다운로드 및 저장
        import requests
        image_response = requests.get(generated_image_url)
        if image_response.status_code == 200:
            with open(generated_path, "wb") as f:
                f.write(image_response.content)

        return {
            "status": "success",
            "original_image": file_path,
            "generated_image_path": generated_path,
            "generated_image_url": generated_image_url,
            "prompt_used": prompt
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }




# 서버 실행 명령어
# uvicorn main:app --reload