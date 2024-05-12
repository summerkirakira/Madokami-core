from fastapi import FastAPI
from ..config import basic_config
from fastapi.middleware.cors import CORSMiddleware


def get_fastapi_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
