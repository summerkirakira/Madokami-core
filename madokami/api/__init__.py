from .register import register_router
from .engines import engine_router
from .downloads import download_router
from .media import media_router
from .subscribe import subscribe_router
from .plugins import plugin_router
from .settings import settings_router
from .logs import logs_router
from .scheduler import scheduler_router
from .app import app_router
from fastapi import APIRouter


def get_internal_routers() -> list[APIRouter]:
    return [app_router, register_router, engine_router, download_router, media_router, subscribe_router, plugin_router, settings_router, logs_router, scheduler_router]
