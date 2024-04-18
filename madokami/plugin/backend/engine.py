from abc import abstractmethod
from ..basic_plugin import BasicPlugin
from typing import Tuple, Any


class Engine(BasicPlugin):
    @abstractmethod
    def run(self) -> Any:
        pass

    @abstractmethod
    def cancel(self):
        pass

    @abstractmethod
    def status(self) -> Tuple[int, Any]:
        pass

