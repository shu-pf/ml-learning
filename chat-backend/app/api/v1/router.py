"""API v1ルーターの集約"""
from fastapi import APIRouter
from app.api.v1.endpoints import items, chat

api_router = APIRouter()

api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(chat.router, prefix="", tags=["chat"])

