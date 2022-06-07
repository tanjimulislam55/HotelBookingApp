from typing import List
from datetime import date
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException

from schemas.feedbacks import FeedbackCreate, FeedbackOut, FeedbackUpdate
from models import User
from api.dependencies import get_current_user
from crud.feedbacks import feedback
from crud.books import booked_by_user


router = APIRouter()


@router.get("/", response_model=List[FeedbackOut], status_code=status.HTTP_200_OK)
async def get_multiple_feedbacks(
    skip: int = 0,
    limit: int = 10,
):
    return await feedback.get_many(skip, limit)


@router.post("/", response_model=FeedbackOut, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback_in: FeedbackCreate,
    current_user: User = Depends(get_current_user),
):
    """if a user books a hotel and traverse checkout date, eligible to give feedback"""
    total_traversed_bookings = (
        await booked_by_user.get_many_filtered_by_hotel_user_id_date(
            feedback_in.hotel_id, user_id=current_user.id, current_date=date.today()
        )
    )
    if not total_traversed_bookings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not permitted to give feedback to the hotel",
        )
    new_generated_id = await feedback.create(feedback_in)
    return {**feedback_in.dict(), "id": new_generated_id}


@router.put("/{feedback_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_board_type(
    feedback_id: int,
    feedback_update: FeedbackUpdate,
    current_user: User = Depends(get_current_user),
):
    if not await feedback.get_one(feedback_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await feedback.update(feedback_id, feedback_update)
    return {**feedback_update.dict(exclude_unset=True), "id": feedback_id}
