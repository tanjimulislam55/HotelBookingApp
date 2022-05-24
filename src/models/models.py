from email.policy import default
from enum import unique
from turtle import title
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
    tax = Column(String(5))
    service_charge = Column(String(5))
    partnership_discount = Column(Float)
    discount_promo_code = Column(String(20))
    discount_description = Column(String(150))
    rating_value = Column(Integer) # sort/filter key


class Address(BaseModel):
    __tablename__ = "addresses"

    area = Column(String(100))
    street_address = Column(String(255))
    city = Column(String(50))
    country = Column(String(50))


class Room(BaseModel):
    __tablename__ = "rooms"

    adult = Column(Integer)
    child = Column(Integer)
    extra_bed = Column(Integer)
    max_occupancies = Column(Integer)
    available_room = Column(Integer)
    rate = Column(Integer)


class BoardType(BaseModel):
    __tablename__ = "boards_types"

    name = Column(String(50)) # Break and Breakfast
    code = Column(String(5)) # BB
    description = Column(String()) # Breakfast Included


class Amenity(BaseModel):
    __tablename__ = "amenties"

    

class Facility(BaseModel):
    __tablename__ = "facilities"

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
    disability_friendly = Column(Boolean, default=False)


class Image(BaseModel):
    __tablename__ = "images"

    title = Column(String(50))
    description = Column(String(100))
    source_url = Column(String(250))
    file_name = Column(String(50))

    couple_friendly = Column(Boolean, default=False)