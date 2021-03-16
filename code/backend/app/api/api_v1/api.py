from fastapi import APIRouter

from code.backend.app.api.api_v1.endpoints import orders, findata #, login, users, utils

api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(findata.router, prefix="/findata", tags=["findata"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
