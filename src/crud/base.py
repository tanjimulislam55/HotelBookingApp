from typing import Any, Generic, List, Optional, Type, Union, TypeVar
from sqlalchemy.orm import Session, declarative_base
from pydantic import BaseModel
from datetime import datetime

from utils.db import database

Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model



    