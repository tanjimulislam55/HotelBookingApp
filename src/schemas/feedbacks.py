from typing import Text, Union
from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    rating_value: int
    review_comment: Union[Text, None]
    hotel_id: int
    user_id: int


class FeedbackOut(FeedbackCreate):
    id: int

    class Config:
        orm_mode = True


class FeedbackUpdate(BaseModel):
    rating_value: Union[int, None]
    review_comment: Union[Text, None]
