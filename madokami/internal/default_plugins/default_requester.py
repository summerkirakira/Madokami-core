from madokami.plugin.backend.requester import Requester
from madokami.internal.core_config import get_proxy_url
import requests


class DefaultRequester(Requester):

    def __init__(self, headers: dict = None):
        self.headers = headers
        if proxy_url := get_proxy_url() is not None:
            self.proxy = {
                'http': proxy_url,
                'https': proxy_url
            }
        else:
            self.proxy = None

        self._status = "Initialized"

    def request(self, url: str, method: str = 'GET'):
        self._status = "Requesting"
        response = requests.request(method, url, headers=self.headers, proxies=self.proxy)
        self._status = "Finished"
        return response

    @property
    def status(self) -> tuple[int, str]:
        return 0, self._status

    def cancel(self):
        pass

    @property
    def namespace(self) -> str:
        return 'madokami.summerkirakira.default_requester'

    @property
    def name(self) -> str:
        return 'Default Requester'

    @property
    def description(self) -> str:
        return 'Default Requester for madokami'
