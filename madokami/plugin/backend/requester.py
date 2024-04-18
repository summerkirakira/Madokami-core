from abc import abstractmethod
from ..basic_plugin import BasicPlugin


class Requester(BasicPlugin):
    @abstractmethod
    def request(self, url: str, **kwargs) -> bytes:
        pass

    @abstractmethod
    def status(self) -> tuple[int, str]:
        pass

    @abstractmethod
    def cancel(self):
        pass