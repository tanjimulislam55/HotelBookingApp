from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from schemas import (
    HotelCreate,
    FacilityGroupCreate,
    HotelOut,
    AddressCreate,
    FacilityGroupOut,
    AddressOut,
)
from models import User
from api.dependencies import get_current_active_superuser
from crud.hotels import hotel, facility_group, address

router = APIRouter()


@router.get("/", response_model=List[HotelOut], status_code=status.HTTP_200_OK)
async def get_multiple_hotels(
    skip: int = 0,
    limit: int = 10,
):
    hotels = await hotel.get_many(skip, limit)
    return [
        {
            **HotelOut(**hotel_info).dict(),
            "facility_group": FacilityGroupOut(**hotel_info),
            "address": AddressOut(**hotel_info),
        }
        for hotel_info in hotels
    ]


@router.get("/{hotel_id}", response_model=HotelOut, status_code=status.HTTP_200_OK)
async def get_a_hotel(hotel_id: int):
    hotel_info = await hotel.get_one(hotel_id)
    return {
        **HotelOut(**hotel_info).dict(),
        "facility_group": FacilityGroupOut(**hotel_info),
        "address": AddressOut(**hotel_info),
    }


@router.post("/", response_model=HotelOut, status_code=status.HTTP_201_CREATED)
async def create_new_hotel(
    hotel_in: HotelCreate, current_user: User = Depends(get_current_active_superuser)
):
    hotel_info = await hotel.get_one_by_name(hotel_in.name)
    if hotel_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="This name is already taken"
        )
    new_generated_hotel_id = await hotel.create(
        hotel_in.copy(exclude={"facility_group", "address"})
    )
    hotel_dict = hotel_in.copy(exclude={"facility_group", "address"}).dict()
    facility_group_dict = hotel_in.facility_group.dict()
    facility_group_dict.update({"hotel_id": new_generated_hotel_id})
    address_dict = hotel_in.address.dict()
    address_dict.update({"hotel_id": new_generated_hotel_id})
    try:
        await facility_group.create(FacilityGroupCreate(**facility_group_dict))
        await address.create(AddressCreate(**address_dict))
        return {
            "id": new_generated_hotel_id,
            **hotel_dict,
            **facility_group_dict,
            **address_dict,
        }
    except NotImplementedError:
        await hotel.remove(new_generated_hotel_id)
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Could not create."
        )
