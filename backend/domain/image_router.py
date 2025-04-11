from fastapi import FastAPI, File, UploadFile, APIRouter

router = APIRouter(
    prefix="/upload"
)

@router.get("/image")
async def create_upload_file(file: UploadFile):
        return {"filename": file.filename}


# app.include_router(image_router.router)