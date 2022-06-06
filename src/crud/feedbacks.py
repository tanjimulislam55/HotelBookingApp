from typing import List
from sqlalchemy import select

from models import Feedback
from .base import CRUDBase
from utils.db import database
from schemas.feedbacks import FeedbackCreate, FeedbackUpdate


class CRUDFeedback(CRUDBase[Feedback, FeedbackCreate, FeedbackUpdate]):
    async def get_many_by_user_id(self, user_id: int) -> List[Feedback]:
        query = select(Feedback).where(Feedback.user_id == user_id)
        return await database.fetch_all(query)

    async def get_many_by_hotel_id(self, hotel_id: int) -> List[Feedback]:
        query = select(Feedback).where(Feedback.hotel_id == hotel_id)
        return await database.fetch_all(query)


feedback = CRUDFeedback(Feedback)
