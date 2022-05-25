from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    Text,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Enum,
)

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(50), nullable=False, unique=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(14), nullable=False)
    birth_date = Column(String(10))
    password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False)


class Hotel(BaseModel):
    __tablename__ = "hotels"

    name = Column(String(100), nullable=False, unique=True, index=True)
    tax = Column(Integer)
    service_charge = Column(Integer)
    partnership_discount = Column(Float)
    discount_promo_code = Column(String(20))
    discount_description = Column(String(150))
    rating_value = Column(Float)  # sort/filter key

    facility_group = relationship("FacilityGroup", back_populates="hotel")
    address = relationship("Address", back_populates="hotel")
    rooms = relationship("Room", back_populates="hotel")


class FacilityGroup(BaseModel):
    __tablename__ = "facility_group"

    breakfast = Column(Boolean, default=False)
    restaurant = Column(Boolean, default=False)
    parking = Column(Boolean, default=False)
    two_four_security = Column(Boolean, default=False)
    business = Column(Boolean, default=False)
    swimming_pool = Column(Boolean, default=False)
    room_service = Column(Boolean, default=False)
    indoor_games = Column(Boolean, default=False)
    outdoor_activities = Column(Boolean, default=False)
    fitness_centre = Column(Boolean, default=False)
    airport_shuttle = Column(Boolean, default=False)
    early_checkin = Column(Boolean, default=False)
    late_checkout = Column(Boolean, default=False)
    air_conditioning = Column(Boolean, default=False)
    kid_friendly = Column(Boolean, default=False)
    couple_friendly = Column(Boolean, default=False)
    disability_friendly = Column(Boolean, default=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"))

    hotel = relationship("Hotel", back_populates="facility_group")


class Facility(BaseModel):
    __tablename__ = "facilities"

    name = Column(String(20))
    tag = Column(String(20))


class Address(BaseModel):
    __tablename__ = "addresses"

    area = Column(String(100))
    street_address = Column(String(255))
    city = Column(String(50))
    country = Column(String(50))
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="CASCADE"))

    hotel = relationship("Hotel", back_populates="address")


class BoardType(BaseModel):
    __tablename__ = "board_types"

    name = Column(String(50))  # Break and Breakfast
    code = Column(String(5))  # BB
    description = Column(String())  # Breakfast Included

    rooms = relationship("Room", back_populates="board_type")


class Room(BaseModel):
    __tablename__ = "rooms"

    adult = Column(Integer)
    child = Column(Integer)
    extra_bed = Column(Integer)
    max_occupancies = Column(Integer)
    available_room = Column(Integer)
    rate = Column(Integer)  # sort/filter key
    board_type_id = Column(ForeignKey("board_types.id", ondelete="SET_NULL"))
    hotel_id = Column(ForeignKey("hotels.id", ondelete="CASCADE"))

    board_type = relationship("BoardType", back_populates="rooms")
    amenity = relationship("Amenity", back_populates="room")
    images = relationship("Image", back_populates="room")
    hotel = relationship("Hotel", back_populates="rooms")


class Amenity(BaseModel):
    __tablename__ = "amenities"

    air_conditioning = Column(Boolean, default=False)
    balcony = Column(Boolean, default=False)
    bathtub = Column(Boolean, default=False)
    ceiling_fan = Column(Boolean, default=False)
    clothes_dryer = Column(Boolean, default=False)
    connecting_rooms = Column(Boolean, default=False)
    cooker = Column(Boolean, default=False)
    dining_area = Column(Boolean, default=False)
    disability_friendly = Column(Boolean, default=False)
    electric_kettle = Column(Boolean, default=False)
    garden_view = Column(Boolean, default=False)
    hairdryer = Column(Boolean, default=False)
    hot_water = Column(Boolean, default=False)
    ironing_set = Column(Boolean, default=False)
    kitchenette = Column(Boolean, default=False)
    microwave_oven = Column(Boolean, default=False)
    minibar = Column(Boolean, default=False)
    mountain_or_hill_view = Column(Boolean, default=False)
    non_smoking_room = Column(Boolean, default=False)
    pool_view = Column(Boolean, default=False)
    power_outlet = Column(Boolean, default=False)
    private_beach = Column(Boolean, default=False)
    safe_or_locker = Column(Boolean, default=False)
    smoking_room = Column(Boolean, default=False)
    tea_and_offee = Column(Boolean, default=False)
    telephone = Column(Boolean, default=False)
    toiletries = Column(Boolean, default=False)
    tv = Column(Boolean, default=False)
    wifi = Column(Boolean, default=False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"))

    room = relationship("Room", back_populates="amenity")


class Image(BaseModel):
    __tablename__ = "images"

    title = Column(String(50))
    description = Column(String(100))
    source_url = Column(String(250))
    file_name = Column(String(50))
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"))

    room = relationship("Room", back_populates="images")
