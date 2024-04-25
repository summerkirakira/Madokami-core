from abc import abstractmethod
from ..basic_plugin import BasicPlugin
from typing import Any, Literal
from pydantic import BaseModel


class DownloadStatus(BaseModel):
    id: str
    name: str
    current: int
    total: int
    source: str
    status: Literal['downloading', 'completed', 'failed', 'pending', 'paused']
    speed_per_sec: int
    message: str


class Engine(BasicPlugin):
    @abstractmethod
    def run(self):
        ...


class FileDownloaderEngine(Engine):
    ...



