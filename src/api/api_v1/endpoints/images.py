from typing import List
from fastapi import APIRouter, UploadFile, File
from fastapi.exceptions import HTTPException
import aiofiles
import os

from schemas import ImageCreate, ImageBase
from models import User
from api.dependencies import get_current_active_superuser
from settings import settings

router = APIRouter()

directory = settings.STATIC_DIR


@router.post("/upload_image")
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
