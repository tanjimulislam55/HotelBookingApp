from typing import Optional, List
from sqlalchemy import select

from schemas.rooms import RoomCreate, RoomUpdate, AmenityCreate, AmenityUpdate
from models import Room, Amenity
from .base import CRUDBase
from utils.db import database


class CRUDRoom(CRUDBase[Room, RoomCreate, RoomUpdate]):
    async def get_many(
        self, skip: int, limit: int, hotel_id: Optional[int] = None
    ) -> List[Room]:
        if hotel_id:
            query = (
                select(Room).where(Room.hotel_id == hotel_id).offset(skip).limit(limit)
            )
            return await database.fetch_all(query)
        return await super().get_many(skip, limit)


room = CRUDRoom(Room)


class CRUDAmenity(CRUDBase[Amenity, AmenityCreate, AmenityUpdate]):
    pass


amenity = CRUDAmenity(Amenity)
