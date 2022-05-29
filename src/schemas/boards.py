from pydantic import BaseModel
from typing import Optional


class BoardTypeCreate(BaseModel):
    name: str  # Break and Breakfast
    code: str  # BB
    description: Optional[str]


class BoardTypeUpdate(BaseModel):
    name: Optional[str]  # Break and Breakfast
    code: Optional[str]  # BB
    description: Optional[str]


class BoardTypeOut(BoardTypeCreate):
    id: int

    class Config:
        orm_mode = True
