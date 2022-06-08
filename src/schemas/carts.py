from pydantic import BaseModel


class CartCreate(BaseModel):
    user_id: int
    room_id: int
    hotel_id: int


class CartOut(CartCreate):
    id: int

    class Config:
        orm_mode = True
