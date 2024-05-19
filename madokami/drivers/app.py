from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
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
    # app.mount("/webui/", StaticFiles(directory=static_file_path, html=True), name="webui")

    @app.get("/webui/{full_path:path}")
    async def catch_all(request: Request, full_path: str):
        file_path = static_file_path / full_path
        if not file_path.exists():
            return FileResponse(str(static_file_path / 'index.html'))
        return FileResponse(str(file_path))

    @app.get("/")
    async def index():
        return RedirectResponse(url="/webui/index.html")