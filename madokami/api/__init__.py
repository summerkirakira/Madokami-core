from .register import register_router
from .engines import engine_router
from .downloads import download_router
from .media import media_router
from .subscribe import subscribe_router
from .plugins import plugin_router
from fastapi import APIRouter


def get_internal_routers() -> list[APIRouter]:
    return [register_router, engine_router, download_router, media_router, subscribe_router, plugin_router]
