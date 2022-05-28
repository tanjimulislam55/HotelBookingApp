# from pydantic import BaseModel
# from typing import Optional


# class FacilityGroupBase(BaseModel):
#     breakfast: Optional[bool] = False
#     restaurant: Optional[bool] = False
#     parking: Optional[bool] = False
#     two_four_security: Optional[bool] = False
#     business: Optional[bool] = False
#     swimming_pool: Optional[bool] = False
#     room_service: Optional[bool] = False
#     indoor_games: Optional[bool] = False
#     outdoor_activities: Optional[bool] = False
#     fitness_centre: Optional[bool] = False
#     airport_shuttle: Optional[bool] = False
#     early_checkin: Optional[bool] = False
#     late_checkout: Optional[bool] = False
#     air_conditioning: Optional[bool] = False
#     kid_friendly: Optional[bool] = False
#     couple_friendly: Optional[bool] = False
#     disability_friendly: Optional[bool] = False


# class FacilityGroupCreate(FacilityGroupBase):
#     hotel_id: int


# class FacilityGroupUpdate(FacilityGroupBase):
#     pass


# class HotelBase(BaseModel):
#     name: str
#     tax: Optional[int] = 0
#     service_charge: Optional[int] = 0
#     partnership_discount: Optional[float] = 0
#     discount_promo_code: Optional[str]
#     discount_description: Optional[str]
#     rating_value: Optional[float] = 0


# class HotelCreate(HotelBase):
#     facility_group: FacilityGroupBase


# class HotelUpdate(BaseModel):
#     name: Optional[str]
#     tax: Optional[int]
#     service_charge: Optional[int]
#     partnership_discount: Optional[float]
#     discount_promo_code: Optional[str]
#     discount_description: Optional[str]
#     rating_value: Optional[float]


# class HotelOut(HotelBase, FacilityGroupBase):
#     id: int

#     class Config:
#         orm_mode = True
