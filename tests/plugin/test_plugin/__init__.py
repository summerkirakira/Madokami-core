from typing import Tuple, Any

from madokami.plugin.backend.engine import Engine
from madokami.plugin.backend.requester import Requester
from madokami.plugin import register_engine
from madokami.models import Plugin


class TestEngine(Engine):
    def run(self):
        pass

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


plugin_info = Plugin(
    namespace=TestEngine.namespace,
    name=TestEngine.name,
    description=TestEngine.description,
    is_active=True
)


register_engine(TestEngine())
