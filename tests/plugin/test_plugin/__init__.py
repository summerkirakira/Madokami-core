from typing import Tuple, Any

from madokami.plugin.backend.engine import Engine
from madokami.plugin.backend.requester import Requester
from madokami.plugin import register_engine
from madokami.models import PluginInfo
from madokami.log import logger


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


test_engine = TestEngine()


plugin_info = PluginInfo(
    namespace=str(test_engine.namespace),
    name=str(test_engine.name),
    description=str(test_engine.description),
)


register_engine(plugin=plugin_info, engine=test_engine)

