from typing import List
from sqlalchemy import select

from models import Cart
from .base import CRUDBase
from utils.db import database
from schemas.carts import CartCreate


class CRUDCart(CRUDBase[Cart, CartCreate, None]):
    async def get_many_by_user_id(
        self, user_id: int, skip: int, limit: int
    ) -> List[Cart]:
        query = select(Cart).where(Cart.user_id == user_id).offset(skip).limit(limit)
        return await database.fetch_all(query)


cart = CRUDCart(Cart)
