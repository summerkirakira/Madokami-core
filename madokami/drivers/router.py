from fastapi import APIRouter


router = APIRouter()


def register_router(api_router: APIRouter, prefix: str = "", tags: list[str] = None) -> None:
    router.include_router(api_router, prefix=prefix, tags=tags)


def get_registered_router() -> APIRouter:
    return router

