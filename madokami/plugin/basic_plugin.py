import abc
from abc import abstractmethod
from pydantic import BaseModel
from typing import Callable, Optional, Dict


class Status(BaseModel):

    class ConfigRequest(BaseModel):
        class Config(BaseModel):
            key: str
            name: str
        method: Callable[[Dict[str, str]], None]
        configs: list[Config]

    success: bool
    message: str
    running: bool = False
    config_request: Optional[ConfigRequest] = None


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
