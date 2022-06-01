from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException

from schemas import (
    HotelCreate,
    FacilityGroupCreate,
    HotelOut,
    AddressCreate,
    FacilityGroupOut,
    AddressOut,
    RoomOut,
    AmenityOut,
)
from models import User
from api.dependencies import get_current_active_superuser
from crud.hotels import hotel, facility_group, address

router = APIRouter()


@router.get("/search/list", status_code=status.HTTP_200_OK)
async def search_hotels(
    city: str,
    area: str,
    is_booked: bool = False,
    adult: int = 2,
    child: int = 1,
    max_occupancies: int = 4,
    min_rate: int = 0,
    max_rate: int = 10000,
    rating_value: int = 3,
    skip: int = 0,
    limit: int = 10,
):
    hotels = await hotel.get_many_filtered(
        skip,
        limit,
        rating_value,
        city,
        area,
        adult,
        child,
        is_booked,
        max_occupancies,
        min_rate,
        max_rate,
    )
    return hotels
    return [
        {
            **HotelOut(**hotel_info).dict(),
            "facility_group": FacilityGroupOut(**hotel_info),
            "address": AddressOut(**hotel_info),
            "rooms": {
                **RoomOut(**hotel_info).dict(),
                "amenity": AmenityOut(**hotel_info),
            },
        }
        for hotel_info in hotels
    ]


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
async def create_new_hotel(hotel_in: HotelCreate):
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
        new_generated_facility_group_id = await facility_group.create(
            FacilityGroupCreate(**facility_group_dict)
        )
        new_generated_address_id = await address.create(AddressCreate(**address_dict))
        return {
            "id": new_generated_hotel_id,
            **hotel_dict,
            "facility_group": FacilityGroupOut(
                **facility_group_dict, id=new_generated_facility_group_id
            ),
            "address": AddressOut(**address_dict, id=new_generated_address_id),
        }
    except NotImplementedError:
        await hotel.remove(new_generated_hotel_id)
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Could not create."
        )


@router.delete("/{hotel_id}", status_code=status.HTTP_202_ACCEPTED)
async def remove_a_hotel(
    hotel_id: int, current_user: User = Depends(get_current_active_superuser)
):
    if not await hotel.get_one(hotel_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await hotel.remove(hotel_id)
    return {"message": "deleted successfully"}
