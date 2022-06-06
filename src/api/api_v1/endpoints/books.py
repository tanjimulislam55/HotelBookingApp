from typing import List
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException

from schemas.books import BookedByUserCreate, BookedByUserOut
from models import User
from api.dependencies import get_current_active_superuser, get_current_user
from crud.books import booked_by_user

router = APIRouter()


@router.get("/", response_model=List[BookedByUserOut], status_code=status.HTTP_200_OK)
async def get_multiple_bookings(
    current_user: User = Depends(get_current_active_superuser),
    skip: int = 0,
    limit: int = 10,
):
    return await booked_by_user.get_many(skip, limit)


@router.post("/", response_model=BookedByUserOut, status_code=status.HTTP_201_CREATED)
async def book_a_room(
    book_in: BookedByUserCreate,
    current_user: User = Depends(get_current_user),
):
    booked_by_user_info = await booked_by_user.get_many_by_booked_date(
        book_in.check_in, book_in.check_out, book_in.room_id
    )
    if booked_by_user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to book in between these dates",
        )
    new_generated_id = await booked_by_user.create(book_in)
    return {**book_in.dict(), "id": new_generated_id}


@router.delete("/{booking_id}", status_code=status.HTTP_202_ACCEPTED)
async def remove_booking(
    booking_id: int, current_user: User = Depends(get_current_active_superuser)
):
    if not await booked_by_user.get_one(booking_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await booked_by_user.remove(booking_id)
    return {"message": "deleted successfully"}
