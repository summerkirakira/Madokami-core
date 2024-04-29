import abc
from abc import ABC, abstractmethod
from typing import Optional, Dict, Literal, Callable
from pydantic import BaseModel
from enum import Enum
from pathlib import Path


class DownloadStatus(Enum):
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"
    REMOVED = "removed"


class Download(BaseModel):
    id: str
    is_metadata: bool
    name: str
    target_path: Path
    dir: Path
    total_length: int
    progress: float
    current_download: int
    status: DownloadStatus
    current_speed: int
    finished_callback: Optional[Callable]
    move_up: Callable[[[]], None]
    move_to_bottom: Callable[[], None]
    move_down: Callable[[], None]
    purge: Callable[[], None]
    pause: Callable[[bool], None]
    resume: Callable[[], None]
    remove: Callable[[bool], None]
    error_message: Optional[str]


class Downloader(metaclass=abc.ABCMeta):
    @property
    @abstractmethod
    def namespace(self) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def get_downloads(self) -> list[Download]:
        pass

    @abstractmethod
    def get_download_by_id(self, download_id: str) -> Optional[Download]:
        pass

    @abstractmethod
    def add_download(self, uri: str, options: dict = None, callback: Optional[Callable] = None) -> Download:
        pass

    @classmethod
    def refresh(self):
        pass

