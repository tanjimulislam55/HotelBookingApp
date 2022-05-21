from enum import unique
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
    tax = Column(String())
    rating_value = Column(Integer)
    service_charge = Column(String(5))


class Address(BaseModel):
    __tablename__ = "addresses"

    area = Column(String(100))
    street_address = Column(String(255))
    city = Column(String(50))
    country = Column(String(50))