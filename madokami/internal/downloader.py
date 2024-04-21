import abc
from abc import ABC, abstractmethod
from typing import Optional, Dict, Literal, Callable
from pydantic import BaseModel
from enum import Enum


class Download(BaseModel):

    class Status(Enum):
        DOWNLOADING = "downloading"
        PAUSED = "paused"
        COMPLETED = "completed"
        FAILED = "failed"

    class SourceType(Enum):
        LINK = "link"
        TORRENT = "torrent"
        MAGNET = "magnet"

    id: str
    url: str
    source_type: SourceType
    filename: str
    size: int
    total_size: int
    current_download: int
    status: Status
    download_path: str
    download_speed: int
    download_requester: str
    download_engine_namespace: str
    finished_callback: Optional[Callable]
    move_up: Callable[[], None]
    move_to_bottom: Callable[[], None]
    move_down: Callable[[], None]
    move_to: Callable[[int], None]
    purge: Callable[[], None]
    pause: Callable[[], None]
    resume: Callable[[], None]
    cancel: Callable[[], None]


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
    def get_download_by_id(self, download_id: str) -> Download:
        pass

    @abstractmethod
    def add_download(self, uri: str, options: dict = None, callback: Optional[Callable] = None) -> Download:
        pass

    @abstractmethod
    def pause_download(self, download_id: str) -> Download:
        pass

    @abstractmethod
    def cancel_download(self, download_id: str) -> Download:
        pass

    @abstractmethod
    def resume_download(self, download_id: str) -> Download:
        pass

