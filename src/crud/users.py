from typing import Optional

from schemas.users import UserCreate, UserUpdate
from models import User
from .base import CRUDBase

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_one_by_email(self, email: str) -> Optional[User]:
        pass


user = CRUDUser(User)