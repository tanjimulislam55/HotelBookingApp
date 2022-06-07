from pydantic import BaseModel
from datetime import date


class BookedByUserCreate(BaseModel):
    check_in: date
    check_out: date
    room_id: int
    hotel_id: int
    user_id: int


class BookedByUserOut(BookedByUserCreate):
    id: int

    class Config:
        orm_mode = True
