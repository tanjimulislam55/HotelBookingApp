from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException
from typing import List

from schemas import RoomCreate, RoomOut, AmenityCreate, AmenityOut
from models import User
from api.dependencies import get_current_active_superuser
from crud.rooms import room, amenity

router = APIRouter()


@router.get("/", response_model=List[RoomOut], status_code=status.HTTP_200_OK)
async def get_multiple_rooms(
    skip: int = 0,
    limit: int = 10,
):
    rooms = await room.get_many(skip, limit)
    return [
        {
            **RoomOut(**room_info).dict(),
            "amenity": AmenityOut(**room_info),
        }
        for room_info in rooms
    ]


@router.get("/{hotel_id}", response_model=List[RoomOut], status_code=status.HTTP_200_OK)
async def get_multiple_rooms_of_hotels(
    hotel_id: int,
    skip: int = 0,
    limit: int = 10,
):
    rooms = await room.get_many(skip, limit, hotel_id)
    return [
        {
            **RoomOut(**room_info).dict(),
            "amenity": AmenityOut(**room_info),
        }
        for room_info in rooms
    ]


@router.get("/{room_id}", response_model=RoomOut, status_code=status.HTTP_200_OK)
async def get_a_room(room_id: int):
    room_info = await room.get_one(room_id)
    return {
        **RoomOut(**room_info).dict(),
        "amenity": AmenityOut(**room_info),
    }


@router.post("/", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
async def create_new_room(room_in: RoomCreate):
    new_generated_room_id = await room.create(room_in.copy(exclude={"amenity"}))
    room_dict = room_in.copy(exclude={"amenity"}).dict()
    amenity_dict = room_in.amenity.dict()
    amenity_dict.update({"room_id": new_generated_room_id, "is_booked": False})
    try:
        new_generated_amenity_id = await amenity.create(AmenityCreate(**amenity_dict))
        return {
            "id": new_generated_room_id,
            **room_dict,
            "amenity": AmenityOut(**amenity_dict, id=new_generated_amenity_id),
        }
    except NotImplementedError:
        await room.remove(new_generated_room_id)
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Could not create."
        )


@router.delete("/{room_id}", status_code=status.HTTP_202_ACCEPTED)
async def remove_a_room(
    room_id: int, current_user: User = Depends(get_current_active_superuser)
):
    if not await room.get_one(room_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await room.remove(room_id)
    return {"message": "deleted successfully"}
