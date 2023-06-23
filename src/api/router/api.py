from fastapi import APIRouter

from src.api.router.endpoints import comixes, login, users, utils, chapters

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(comixes.router, prefix="/comixes", tags=["comixes"])
api_router.include_router(chapters.router, prefix="/chapters", tags=["chapters"])
