from typing import List
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException
from datetime import date

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
from models import User, Hotel, Room
from api.dependencies import get_current_active_superuser
from crud.hotels import hotel, facility_group, address
from crud.rooms import room
from crud.books import booked_by_user

router = APIRouter()


@router.get("/search/list", status_code=status.HTTP_200_OK)
async def search_hotels(
    check_in: date,
    check_out: date,
    city: str = None,
    area: str = None,
    rating_value: int = None,
    is_booked: bool = False,
    adult: int = 2,
    child: int = 1,
    min_rate: int = 0,
    max_rate: int = 100000,
    skip: int = 0,
    limit: int = 10,
):
    hotels: List[Hotel] = await hotel.get_many_filtered(
        skip, limit, rating_value, city, area
    )
    print(hotels)
    response = []
    for hotel_info in hotels:
        rooms: List[Room] = await room.get_many_filtered(
            skip,
            limit,
            hotel_info.id,
            adult,
            child,
            is_booked,
            min_rate,
            max_rate,
        )
        for room_info in rooms:
            if await booked_by_user.get_many_by_booked_date(
                check_in, check_out, room_info.id
            ):
                rooms.remove(room_info)
        if not rooms:
            continue
        result = {
            **HotelOut(**hotel_info).dict(),
            "facility_group": FacilityGroupOut(**hotel_info),
            "address": AddressOut(**hotel_info),
            "rooms": [
                {**RoomOut(**room_info).dict(), "amenity": AmenityOut(**room_info)}
                for room_info in rooms
            ],
        }
        response.append(result)
    return response


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


@router.get("/filtered", response_model=List[HotelOut], status_code=status.HTTP_200_OK)
async def get_related_hotels_filtered(
    city: str = None,
    area: str = None,
    rating_value: int = None,
    skip: int = 0,
    limit: int = 5,
):
    hotels: List[Hotel] = await hotel.get_many_filtered(
        skip, limit, rating_value, city, area
    )
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
    if not hotel_info:
        return None
    return {
        **HotelOut(**hotel_info).dict(),
        "facility_group": FacilityGroupOut(**hotel_info),
        "address": AddressOut(**hotel_info),
    }


@router.post("/", response_model=HotelOut, status_code=status.HTTP_201_CREATED)
async def create_new_hotel(
    hotel_in: HotelCreate, current_use: User = Depends(get_current_active_superuser)
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
