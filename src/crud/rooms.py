from typing import Optional
from sqlalchemy import select

# from schemas.rooms import RoomCreate
from models import Room
from .base import CRUDBase
from utils.db import database


class CRUDRoom(CRUDBase[Room, None, None]):
    pass


room = CRUDRoom(Room)
