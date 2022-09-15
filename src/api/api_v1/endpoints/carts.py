from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException

from schemas.carts import CartCreate, CartOut
from models import User
from api.dependencies import get_current_user
from crud.carts import cart
from utils.db import database

router = APIRouter()


@router.get("/", response_model=List[CartOut], status_code=status.HTTP_200_OK)
async def get_multiple_carts_by_user(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
):
    return await cart.get_many_by_user_id(current_user.id, skip, limit)


@router.post("/", response_model=CartOut, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    cart_in: CartCreate,
    current_user: User = Depends(get_current_user),
):
    query = f"SELECT room_id FROM carts WHERE user_id = {cart_in.user_id}"
    async for row in database.iterate(query=query):
        if row.room_id == cart_in.room_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Not permissible to add duplicate rooms of",
            )
    count = f"SELECT COUNT(*) FROM carts WHERE user_id = {cart_in.user_id}"
    print(await database.execute(count))
    if await database.execute(count) > 20:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Not permitted to add more than 20 rooms",
        )
    new_generated_id = await cart.create(cart_in)
    return {**cart_in.dict(), "id": new_generated_id}


@router.delete("/{cart_id}", status_code=status.HTTP_202_ACCEPTED)
async def remove_cart_item(
    cart_id: int, current_user: User = Depends(get_current_user)
):
    if not await cart.get_one(cart_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await cart.remove(cart_id)
    return {"message": "deleted successfully"}
