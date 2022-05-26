from typing import List, Optional
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException

from schemas import HotelCreate, FacilityGroupCreate
from models import User
from api.dependencies import get_current_active_superuser, get_current_user
from crud.hotels import hotel, facility_group
from settings import settings

router = APIRouter()


@router.get("/")
async def get_multiple_hotels(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_superuser),
):
    return await hotel.get_many(skip, limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_hotel(hotel_in: HotelCreate):
    hotel_info = await hotel.get_one_by_name(hotel_in.name)
    if hotel_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This name is already taken"
        )
    new_generated_hotel_id = await hotel.create(
        hotel_in.copy(exclude={"facility_group"})
    )
    facility_group_dict = hotel_in.copy(exclude={"facility_group"}).dict()
    facility_group_dict.update({"hotel_id": new_generated_hotel_id})
    try:
        await facility_group.create(FacilityGroupCreate(**facility_group_dict, {"hotel_id": new_generated_hotel_id}))
        return {**hotel_in.dict(), "id": new_generated_hotel_id}
    except:
        await hotel.remove(new_generated_hotel_id)
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Could not create."
        )
