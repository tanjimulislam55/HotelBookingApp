from typing import List
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import aiofiles
import os

from schemas.images import (
    RoomImageCreate,
    HotelImageCreate,
    RoomImageOut,
    HotelImageOut,
)
from models import User
from api.dependencies import get_current_active_superuser
from settings import settings

router = APIRouter()

directory = settings.STATIC_DIR


@router.post("/")
async def upload_file(file_in: UploadFile = File(...)):
    filename = os.path.join(directory, file_in.filename)
    is_file = os.path.exists(filename)
    if not is_file:
        async with aiofiles.open(filename, "wb") as f:
            while content := await file_in.read(1024):  # async read chunk
                await f.write(content)
            return {
                "Uploaded File": file_in.filename,
            }
    return "File already exists"


@router.get("/{name}")
async def get_image(name: str, room_id: int, hotel_id: int):
    imaage_name = os.path.join(directory, f"{name}.jpg")
    is_file = os.path.exists(imaage_name)
    if is_file:
        return FileResponse(imaage_name, media_type="image/jpg")
    return {"error": "File not found"}
