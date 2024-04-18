import abc
from abc import abstractmethod


class BasicPlugin(metaclass=abc.ABCMeta):

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
