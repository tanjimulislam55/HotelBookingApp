from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from schemas import RoomCreate, RoomOut, AmenityCreate
from models import User
from api.dependencies import get_current_active_superuser
from crud.rooms import room, amenity
from settings import settings

router = APIRouter()


@router.post("/")
async def create_new_room(room_in: RoomCreate):
    new_generated_room_id = await room.create(room_in.copy(exclude={"amenity"}))
    room_dict = room_in.copy(exclude={"amenity"}).dict()
    amenity_dict = room_in.amenity.dict()
    amenity_dict.update({"room_id": new_generated_room_id})
    try:
        await amenity.create(AmenityCreate(**amenity_dict))
        return {
            "id": new_generated_room_id,
            **room_dict,
            **amenity_dict,
        }
    except NotImplementedError:
        await room.remove(new_generated_room_id)
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Could not create."
        )
