from abc import abstractmethod
from ..basic_plugin import BasicPlugin
from typing import Tuple, Any


class Downloader(BasicPlugin):
    @abstractmethod
    def download(self, **kwargs) -> bytes:
        pass

    @abstractmethod
    def status(self) -> Tuple[int, str]:
        pass

    @abstractmethod
    def cancel(self):
        pass

    @abstractmethod
    def pause(self):
        pass

