from fastapi import FastAPI
from ..config import basic_config


def get_fastapi_app() -> FastAPI:
    app = FastAPI()
    return app
