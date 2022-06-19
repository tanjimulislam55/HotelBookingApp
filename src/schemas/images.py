from typing import Union
from pydantic import BaseModel


class ImageOut(BaseModel):
    id: int
    name: str
    source_url: Union[str, None]
    description: Union[str, None]
    room_id: Union[int, None]
    hotel_id: Union[int, None]

    class Config:
        orm_mode = True
