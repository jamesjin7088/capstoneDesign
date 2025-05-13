from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router.image import router as image_router


app = FastAPI()

origins = [
    "http://localhost:5173",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(image_router)


# 가상환경 실행
# source ~/Desktop/venvs/myapi/bin/activate
# 서버 실행 명령어
# uvicorn main:app --reload
# 로컬 IP로 서버 실행
# uvicorn main:app --host 172.30.1.2 --port 8000 --reload