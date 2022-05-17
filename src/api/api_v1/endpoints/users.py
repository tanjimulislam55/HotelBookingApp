from typing import List, Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import UJSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from schemas import UserOut, UserCreate, UserInDB
from models import User
from api.dependencies import get_current_active_superuser, get_current_user
from crud.users import user
from settings import settings
from utils.auth import create_access_token, verify_password, get_password_hash

router = APIRouter()

@router.get("/", response_model=List[UserOut])
async def get_multiple_users(current_user: User = Depends(get_current_active_superuser), skip: int = 0, limit: int = 10):
    users = await user.get_many(skip, limit)
    return UJSONResponse(content=users, status_code=status.HTTP_200_OK)

@router.get("/me", response_model=UserOut)
async def get_user_me(current_user: User = Depends(get_current_user)):
    return UJSONResponse(content=current_user, status_code=status.HTTP_200_OK)

@router.post("/sign_up", response_model=UserOut)
async def create_new_user(user_in: UserCreate):
    user_info = await user.get_one_by_email(user_in.email)
    if user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email is already taken")
    user_info = await user.get_one_by_username(user_in.username)
    if user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is already taken")
    user_dict = user_in.dict(exclude={"password"})
    password = get_password_hash(user_in.password)
    user_dict.update({"password": password, "is_superuser": False})
    new_generated_id = await user.create(UserInDB(**user_dict))
    response = {**user_in.dict(), "id": new_generated_id}
    return UJSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    

@router.post("/sign_in", response_model=UserOut)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_info = await user.get_one_by_email(email=form_data.username)
    if not user_info and not verify_password(form_data.password, user_info.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user_info.email, access_token_expires)
    response = {"access_token": access_token, "token_type": "bearer"}
    return UJSONResponse(status_code=status.HTTP_200_OK, content=response)