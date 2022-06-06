from typing import List
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException

from schemas.feedbacks import FeedbackCreate, FeedbackOut, FeedbackUpdate
from models import User
from api.dependencies import get_current_active_superuser, get_current_user
from crud.feedbacks import feedback


router = APIRouter()
