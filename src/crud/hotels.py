from typing import Optional
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from schemas.hotels import (
    HotelCreate,
    HotelUpdate,
    FacilityGroupCreate,
    FacilityGroupUpdate,
    AddressCreate,
    AddressUpdate,
)
from models import Hotel, FacilityGroup, Address, Room
from .base import CRUDBase
from utils.db import database


class CRUDHotel(CRUDBase[Hotel, HotelCreate, HotelUpdate]):
    async def get_one_by_name(self, name: str) -> Optional[Hotel]:
        query = select(Hotel).where(Hotel.name == name)
        return await database.fetch_one(query)

    async def get_many_filtered(
        self,
        skip,
        limit,
        rating_value: Optional[str] = None,
        city: Optional[str] = None,
        area: Optional[str] = None,
        adult: Optional[int] = None,
        child: Optional[int] = None,
        is_booked: Optional[bool] = None,
        max_occupancies: Optional[int] = None,
        min_rate: Optional[int] = None,
        max_rate: Optional[int] = None,
    ):
        query = (
            select(Hotel)
            .options(joinedload(Hotel.rooms))
            .options(joinedload(Hotel.address))
            .where(
                and_(
                    Hotel.rating_value == rating_value,
                    Address.city == city,
                    Address.area == area,
                    Room.adult == adult,
                    Room.child == child,
                    Room.is_booked == is_booked,
                    Room.max_occupancies == max_occupancies,
                    Room.rate.between(min_rate, max_rate),
                )
            )
            .offset(skip)
            .limit(limit)
        )

        return await database.fetch_all(query)


class CRUDFacilityGroup(
    CRUDBase[FacilityGroup, FacilityGroupCreate, FacilityGroupUpdate]
):
    async def get_one_by_hotel_id(self, hotel_id: int) -> Optional[Hotel]:
        query = select(FacilityGroup).where(FacilityGroup.hotel_id == hotel_id)
        return await database.fetch_one(query)


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):
    pass


hotel = CRUDHotel(Hotel)
facility_group = CRUDFacilityGroup(FacilityGroup)
address = CRUDAddress(Address)
