from typing import Optional
from pydantic import BaseModel


class ImageBase(BaseModel):
    title: Optional[str]
    description: Optional[str]


class ImageCreate(ImageBase):
    source_url: Optional[str]
    file_name: Optional[str]
    room_id: int


class ImageOut(ImageCreate):
    id: int

    class Config:
        orm_mode = True
