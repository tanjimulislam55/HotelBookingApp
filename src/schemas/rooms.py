from pydantic import BaseModel
from typing import Optional
from fastapi import File, UploadFile


class RoomBase(BaseModel):
    adult: Optional[int] = 0
    child: Optional[int] = 0
    extra_bed: Optional[int] = 0
    max_occupancies: Optional[int] = 0
    available_room: Optional[int] = 0
    rate: Optional[int] = 0


class RoomCreate(RoomBase):
    hotel_id: int
    board_type_id: int


class RoomUpdate(RoomBase):
    pass


class AmenityBase(BaseModel):
    air_conditioning: Optional[bool] = False
    balcony: Optional[bool] = False
    bathtub: Optional[bool] = False
    ceiling_fan: Optional[bool] = False
    clothes_dryer: Optional[bool] = False
    connecting_rooms: Optional[bool] = False
    cooker: Optional[bool] = False
    dining_area: Optional[bool] = False
    disability_friendly: Optional[bool] = False
    electric_kettle: Optional[bool] = False
    garden_view: Optional[bool] = False
    hairdryer: Optional[bool] = False
    hot_water: Optional[bool] = False
    ironing_set: Optional[bool] = False
    kitchenete: Optional[bool] = False
    microwave_oven: Optional[bool] = False
    minibar: Optional[bool] = False
    mountain_or_hill_view: Optional[bool] = False
    non_smoking_room: Optional[bool] = False
    pool_view: Optional[bool] = False
    power_outlet: Optional[bool] = False
    private_beach: Optional[bool] = False
    safe_or_locker: Optional[bool] = False
    smoking_room: Optional[bool] = False
    tea_and_offee: Optional[bool] = False
    telephone: Optional[bool] = False
    toiletries: Optional[bool] = False
    tv: Optional[bool] = False
    wifi: Optional[bool] = False


class AmenityCreate(AmenityBase):
    room_id: int


class AmenityUpdate(AmenityBase):
    pass


class ImageBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    source_url: Optional[str]
    file_name: Optional[str]


class ImageCreate(ImageBase):
    @classmethod
    def as_form(
        cls,
        title: Optional[str],
        description: Optional[str],
        source_url: Optional[str],
        file_name: Optional[str],
        file: UploadFile = File(...),
    ):
        return cls(
            title=title,
            description=description,
            source_url=source_url,
            file_name=file_name,
            file=file,
        )


class RoomOut(
    AmenityBase,
):
    id: int

    class Config:
        orm_mode = True
