from ..basic_plugin import BasicPlugin
from abc import abstractmethod


class Parser(BasicPlugin):

    @abstractmethod
    def parse(self, data):
        pass

    @abstractmethod
    def cancel(self):
        pass

    @abstractmethod
    def status(self):
        pass