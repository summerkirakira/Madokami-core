from abc import abstractmethod
from ..basic_plugin import BasicPlugin


class Requester(BasicPlugin):
    @abstractmethod
    def request(self, data):
        pass

    @abstractmethod
    def status(self) -> tuple[int, str]:
        pass

    @abstractmethod
    def cancel(self):
        pass