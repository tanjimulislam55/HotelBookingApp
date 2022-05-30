from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File, Request
from fastapi.exceptions import HTTPException
import aiofiles
import os

from schemas import RoomCreate, RoomOut, RoomUpdate, ImageCreate, ImageBase
from models import User
from api.dependencies import get_current_active_superuser
from crud.rooms import room

router = APIRouter()


# @router.post("/awesome")
# async def post_form(file_in: UploadFile = File(...)):
#     async with aiofiles.open(file_in.filename, "wb") as f:
#         filename = os.path.join("static/", file_in.filename)
#         if not filename:
#             while content := await file_in.read(1024):  # async read chunk
#                 await f.write(content)
#             return {
#                 "Uploaded File": file_in.filename,
#             }
#     return "already exists"
