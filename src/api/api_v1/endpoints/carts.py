from typing import List
from fastapi import APIRouter, Depends, status, Response

from schemas.carts import CartCreate, CartOut
from models import User
from api.dependencies import get_current_user
from crud.carts import cart

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
