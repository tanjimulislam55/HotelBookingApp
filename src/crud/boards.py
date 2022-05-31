from schemas.boards import BoardTypeCreate, BoardTypeUpdate
from models import BoardType
from .base import CRUDBase
from sqlalchemy import select
from typing import Optional

from utils.db import database


class CRUDBoardType(CRUDBase[BoardType, BoardTypeCreate, BoardTypeUpdate]):
    async def get_one_by_name(self, name: str) -> Optional[BoardType]:
        query = select(BoardType).where(BoardType.name == name)
        return await database.fetch_one(query)


board_type = CRUDBoardType(BoardType)