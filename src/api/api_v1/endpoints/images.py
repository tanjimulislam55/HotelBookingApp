from fastapi import APIRouter, status, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import List
from uuid import uuid1
import aiofiles
import os

from models import User
from api.dependencies import get_current_active_superuser
from settings import settings
from utils.db import database
from utils.zip import zipfile
from schemas.images import ImageOut

router = APIRouter()

directory = settings.STATIC_DIR


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_single_file(
    file_in: UploadFile = File(...),
    room_id: int = None,
    hotel_id: int = None,
    current_user: User = Depends(get_current_active_superuser),
):
    id = uuid1()
    unique_filename = f"{id}.jpg"
    filename = os.path.join(directory, unique_filename)
    is_file = os.path.exists(filename)
    if room_id and hotel_id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Either room id or hotel id is acceptable",
        )
    if not is_file:
        async with aiofiles.open(filename, "wb") as f:
            while content := await file_in.read(1024):  # async read chunk
                await f.write(content)
            if room_id:
                query = (
                    "INSERT INTO room_images(name, room_id) VALUES (:name, :room_id)"
                )
                values = {"name": unique_filename, "room_id": room_id}
                await database.execute(query=query, values=values)
            if hotel_id:
                query = (
                    "INSERT INTO hotel_images(name, hotel_id) VALUES (:name, :hotel_id)"
                )
                values = {"name": unique_filename, "hotel_id": hotel_id}
                await database.execute(query=query, values=values)
            return {
                "Uploaded File": file_in.filename,
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="File name conflicted"
        )


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ImageOut])
async def get_multiple_images(
    room_id: int = None, hotel_id: int = None, zipped: bool = False
):
    if room_id:
        query = "SELECT * FROM room_images WHERE room_id = :room_id"
        values = {"room_id": room_id}
        infos = await database.fetch_all(query=query, values=values)
    elif hotel_id:
        query = "SELECT * FROM hotel_images WHERE hotel_id = :hotel_id"
        values = {"hotel_id": hotel_id}
        infos = await database.fetch_all(query=query, values=values)
    if zipped:
        return zipfile([info.name for info in infos])
    return [ImageOut(**info).dict() for info in infos]


@router.get(
    "/{image_name}", response_class=FileResponse, status_code=status.HTTP_200_OK
)
async def get_multiple_image_response(image_name: str):
    filename = os.path.join(directory, image_name)
    if not os.path.exists(filename):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Image not found")
    return filename
