from datetime import date
from sqlalchemy import select, or_, and_
from typing import List


from .base import CRUDBase
from models import BookedByUser
from schemas.books import BookedByUserCreate
from utils.db import database


class CRUDBookedByUser(CRUDBase[BookedByUser, BookedByUserCreate, None]):
    async def get_many_by_booked_date(
        self, check_in: date, check_out: date, room_id: int
    ) -> List[BookedByUser]:
        query = (
            select(BookedByUser)
            .where(BookedByUser.room_id == room_id)
            .where(
                or_(
                    BookedByUser.check_in.between(check_in, check_out),
                    BookedByUser.check_out.between(check_in, check_out),
                )
            )
        )

        return await database.fetch_all(query)

    async def get_many_filtered_by_hotel_user_id_date(
        self, hotel_id: int, user_id: int, current_date: date
    ) -> List[BookedByUser]:
        query = select(BookedByUser).where(
            and_(
                BookedByUser.user_id == user_id,
                BookedByUser.hotel_id == hotel_id,
                BookedByUser.check_out < current_date,
            )
        )
        return await database.fetch_all(query)


booked_by_user = CRUDBookedByUser(BookedByUser)
