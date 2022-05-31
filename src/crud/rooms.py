from typing import Optional
from sqlalchemy import select

from schemas.rooms import RoomCreate, RoomUpdate, AmenityCreate, AmenityUpdate
from models import Room, Amenity
from .base import CRUDBase
from utils.db import database


class CRUDRoom(CRUDBase[Room, RoomCreate, RoomUpdate]):
    pass


room = CRUDRoom(Room)


class CRUDAmenity(CRUDBase[Amenity, AmenityCreate, AmenityUpdate]):
    pass


amenity = CRUDAmenity(Amenity)
