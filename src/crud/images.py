from typing import Optional
from sqlalchemy import select

from models import RoomImage, HotelImage
from .base import CRUDBase
from utils.db import database
from schemas.images import RoomImageCreate, HotelImageCreate


class CRUDRoomImage(CRUDBase[RoomImage, RoomImageCreate, None]):
    async def get_many_by_room_id(self, room_id: int) -> Optional[RoomImage]:
        query = select(RoomImage).where(RoomImage.room_id == room_id)
        return await database.fetch_all(query)


room_image = CRUDRoomImage(RoomImage)


class CRUDHotelImage(CRUDBase[HotelImage, HotelImageCreate, None]):
    async def get_many_by_hotel_id(self, hotel_id: int) -> Optional[RoomImage]:
        query = select(HotelImage).where(HotelImage.hotel_id == hotel_id)
        return await database.fetch_all(query)


hotel_image = CRUDHotelImage(HotelImage)
