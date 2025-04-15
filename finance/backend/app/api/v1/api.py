from fastapi import APIRouter
from app.api.v1.endpoints import auth, stocks, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(users.router, prefix="/users", tags=["users"]) 