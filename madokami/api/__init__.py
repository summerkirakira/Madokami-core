from .register import register_router
from fastapi import APIRouter


def get_internal_routers() -> list[APIRouter]:
    return [register_router]