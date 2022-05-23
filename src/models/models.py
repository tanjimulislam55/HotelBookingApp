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

    hotel_board_type_name = Column(String(50)) # Break and Breakfast
    board_code = Column(String(5)) # BB
    description = Column(String()) # Breakfast Included
    adult = Column(Integer)
    child = Column(Integer)
    extra_bed = Column(Integer)
    max_occupancies = Column(Integer)
    extra_bed = Column(Integer)
    available_room = Column(Integer)
    rate = Column(Integer)


class Image(BaseModel):
    __tablename__ = "images"

    title = Column(String(50))
    description = Column(String(100))
    source_url = Column(String(250))
    file_name = Column(String(50))
