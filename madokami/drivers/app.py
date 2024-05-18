from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from ..config import basic_config
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path


static_file_path = Path(basic_config.static_files)

# print(static_file_path.absolute())


def get_fastapi_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    mount_static_files(app)
    return app


def mount_static_files(app: FastAPI):
    app.mount("/webui", StaticFiles(directory=static_file_path), name="webui")

    @app.get("/")
    async def index():
        return RedirectResponse(url="/webui/index.html")