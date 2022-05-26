from typing import Optional
from sqlalchemy import select

from schemas.hotels import (
    HotelCreate,
    HotelUpdate,
    FacilityGroupCreate,
    FacilityGroupUpdate,
)
from models import Hotel, FacilityGroup
from .base import CRUDBase
from utils.db import database


class CRUDHotel(CRUDBase[Hotel, HotelCreate, HotelUpdate]):
    async def get_one_by_name(self, name: str) -> Optional[Hotel]:
        query = select(self.model).where(self.model.name == name)
        return await database.fetch_one(query)


hotel = CRUDHotel(Hotel)


class CRUDFacilityGroup(
    CRUDBase[FacilityGroup, FacilityGroupCreate, FacilityGroupUpdate]
):
    pass


facility_group = CRUDFacilityGroup(FacilityGroup)
