from typing import Optional, List
from sqlalchemy import select

from schemas.hotels import (
    HotelCreate,
    HotelUpdate,
    FacilityGroupCreate,
    FacilityGroupUpdate,
    AddressCreate,
    AddressUpdate,
)
from models import Hotel, FacilityGroup, Address
from .base import CRUDBase
from utils.db import database


class CRUDHotel(CRUDBase[Hotel, HotelCreate, HotelUpdate]):
    async def get_one_by_name(self, name: str) -> Optional[Hotel]:
        query = select(Hotel).where(Hotel.name == name)
        return await database.fetch_one(query)

    async def get_one(self, id: int) -> Optional[Hotel]:
        query = select(Hotel).where(Hotel.id == id)
        return await database.fetch_one(query)

    async def get_many(self, skip: int, limit: int) -> List[Hotel]:
        query = select(Hotel).offset(skip).limit(limit)
        return await database.fetch_all(query)


hotel = CRUDHotel(Hotel)


class CRUDFacilityGroup(
    CRUDBase[FacilityGroup, FacilityGroupCreate, FacilityGroupUpdate]
):
    async def get_one_by_hotel_id(self, hotel_id: int) -> Optional[Hotel]:
        query = select(FacilityGroup).where(FacilityGroup.hotel_id == hotel_id)
        return await database.fetch_one(query)


facility_group = CRUDFacilityGroup(FacilityGroup)


class CRUDAddress(CRUDBase[Address, AddressCreate, AddressUpdate]):
    pass


address = CRUDAddress(Address)
