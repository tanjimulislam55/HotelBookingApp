from typing import Optional
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
