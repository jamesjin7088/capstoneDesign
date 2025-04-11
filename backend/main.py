from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import os
import subprocess
import sys
import numpy as np
from PIL import Image
import io
import time
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

@app.get("/image")
async def create_file(file: UploadFile):
    # 업로드된 파일 읽기
    content = await file.read()

    # 업로드 디렉토리 생성
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 파일명 생성 (시간 기반으로 고유한 파일명 생성)
    timestamp = int(time.time())
    file_extension = os.path.splitext(file.filename) [1]
    unique_filename = f"{timestamp}{file_extension}"

    # 파일 저장
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as f:
        f.write(content)

    return JSONResponse({
        "filename": file.filename,
        "saved_path": file_path,
    })


# uvicorn main:app --reload