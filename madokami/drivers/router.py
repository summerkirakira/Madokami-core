from fastapi import APIRouter


router = APIRouter()


def register_router(api_router: APIRouter, prefix: str = "", tags: list[str] = None) -> None:
    api_router.include_router(router, prefix=prefix, tags=tags)


def get_router() -> APIRouter:
    return router

