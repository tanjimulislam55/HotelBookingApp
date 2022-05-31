from typing import List
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException

from schemas import BoardTypeCreate, BoardTypeOut, BoardTypeUpdate
from models import User
from api.dependencies import get_current_active_superuser
from crud.boards import board_type

router = APIRouter()


@router.get("/", response_model=List[BoardTypeOut], status_code=status.HTTP_200_OK)
async def get_multiple_board_types(
    current_user: User = Depends(get_current_active_superuser),
    skip: int = 0,
    limit: int = 10,
):
    return await board_type.get_many(skip, limit)


@router.get(
    "/{board_type_id}", response_model=BoardTypeOut, status_code=status.HTTP_200_OK
)
async def get_a_board_type(
    board_type_id: int, current_user: User = Depends(get_current_active_superuser)
):
    return await board_type.get_one(board_type_id)


@router.post("/", response_model=BoardTypeOut, status_code=status.HTTP_201_CREATED)
async def create_a_board_type(
    board_in: BoardTypeCreate,
    current_user: User = Depends(get_current_active_superuser),
):
    board_type_info = await board_type.get_one_by_name(board_in.name)
    if board_type_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This name is already taken",
        )
    new_generated_id = await board_type.create(board_in)
    return {**board_in.dict(), "id": new_generated_id}


@router.put("/{board_type_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_board_type(
    board_type_id: int,
    board_type_update: BoardTypeUpdate,
    current_user: User = Depends(get_current_active_superuser),
):
    if not await board_type.get_one(board_type_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await board_type.update(board_type_id, board_type_update)
    return {**board_type_update.dict(exclude_unset=True), "id": board_type_id}


@router.delete("/{board_type_id}", status_code=status.HTTP_202_ACCEPTED)
async def remove_a_board_type(
    board_type_id: int, current_user: User = Depends(get_current_active_superuser)
):
    if not await board_type.get_one(board_type_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await board_type.remove(board_type_id)
    return {"message": "deleted successfully"}
