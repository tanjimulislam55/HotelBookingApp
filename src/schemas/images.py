from typing import Optional
from pydantic import BaseModel


class ImageBase(BaseModel):
    name: str
    description: Optional[str]
    source_url: Optional[str]


class RoomImageCreate(ImageBase):
    room_id: int


class HotelImageCreate(ImageBase):
    hotel_id: int


class RoomImageOut(RoomImageCreate):
    id: int

    class Config:
        orm_mode = True


class HotelImageOut(HotelImageCreate):
    id: int

    class Config:
        orm_mode = True
