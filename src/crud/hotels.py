from typing import Optional, Union, List
from sqlalchemy import select, or_

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

    async def get_many_filtered(
        self,
        skip: int,
        limit: int,
        rating_value: Union[int, None],
        city: Union[str, None],
        area: Union[str, None],
    ) -> List[Hotel]:
        query = (
            select(Hotel)
            .join(Address)
            .where(
                Hotel.id == Address.hotel_id,
            )
            .where(
                or_(
                    Hotel.rating_value == rating_value,
                    Address.city.like(f"{city}%"),
                    Address.area.like(f"{area}%"),
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
