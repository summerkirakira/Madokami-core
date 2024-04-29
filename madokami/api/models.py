from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    is_superuser: bool


class InfoMessage(BaseModel):
    message: str
    success: bool = True
    title: str = "Info"
    data: str = ""


class DownloadItem(BaseModel):
    id: str
    is_metadata: bool
    name: str
    target_path: str
    dir: str
    total_length: int
    progress: float
    current_download: int
    status: str
    current_speed: int


class DownloadResponse(BaseModel):
    downloads: list[DownloadItem]