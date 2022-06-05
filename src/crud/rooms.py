from typing import Optional, List
from sqlalchemy import select, and_

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

    async def get_many_filtered(
        self,
        skip: int,
        limit: int,
        hotel_id: int,
        adult: int,
        child: int,
        is_booked: bool,
        min_rate: int,
        max_rate: int,
    ):
        query = (
            select(Room)
            .where(
                and_(
                    Room.hotel_id == hotel_id,
                    Room.adult == adult,
                    Room.child == child,
                    Room.is_booked == is_booked,
                    Room.rate.between(min_rate, max_rate),
                )
            )
            .offset(skip)
            .limit(limit)
        )

        return await database.fetch_all(query)


room = CRUDRoom(Room)


class CRUDAmenity(CRUDBase[Amenity, AmenityCreate, AmenityUpdate]):
    pass


amenity = CRUDAmenity(Amenity)
