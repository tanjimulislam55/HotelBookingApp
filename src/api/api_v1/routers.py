from fastapi import APIRouter

from .endpoints import users, hotels, boards, rooms

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(hotels.router, prefix="/hotels", tags=["hotels"])
api_router.include_router(boards.router, prefix="/board_types", tags=["board_types"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
