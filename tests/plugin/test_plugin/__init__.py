from typing import Tuple, Any

from madokami.plugin.backend.engine import Engine
from madokami.plugin.backend.requester import Requester
from madokami.log import logger


__metadata__ = {
    'name': 'Test Plugin',
    'namespace': 'summerkirakira.test_project',
    'description': 'A plugin for Test Project',
    'version': '0.0.1',
    'author': 'summerkirakira',
    'license': 'MIT',
    'settings': [
        {
            'key': 'test_project.test_setting',
            'name': 'Test Setting',
            'description': 'A test setting for testing purposes',
        },
    ],
    'engines': [
        'TestEngine'
    ],
    'subscription_manager': None
}


class TestEngine(Engine):
    def run(self):
        logger.info('Test engine is running')

    def cancel(self):
        pass

    def status(self) -> Tuple[int, Any]:
        pass

    @property
    def namespace(self) -> str:
        return 'summerkirakira.test_engine'

    @property
    def name(self) -> str:
        return 'A test engine'

    @property
    def description(self) -> str:
        return 'A test engine for testing purposes'


class TestRequester(Requester):

    def request(self, data):
        pass

    def status(self) -> tuple[int, str]:
        pass

    def cancel(self):
        pass

    @property
    def namespace(self) -> str:
        return 'summerkirakira.test_requester'

    @property
    def name(self) -> str:
        return 'A test requester'

    @property
    def description(self) -> str:
        return 'A test requester for testing purposes'

