__all__ = ["base_router"]

from fastapi import APIRouter

# from .calendar import calendar_router
from .chat import chat_router
from .map import map_router

base_router = APIRouter(prefix="/api")

base_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
base_router.include_router(map_router, prefix="/map", tags=["Map"])
# base_router.include_router(calendar_router, prefix="/calendar", tags=["Calendar"])
