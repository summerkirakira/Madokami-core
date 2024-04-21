from typing import Tuple

from madokami.plugin.backend.downloader import Downloader
from madokami.internal.core_config import get_config
import aria2p
from aria2p.options import Options
from aria2p.downloads import Download


class DefaultAria2Downloader(Downloader):

    def __init__(self):
        self._status = "Initialized"
        aria2_host = get_config('madokami.config.aria2_host')
        aria2_port = get_config('madokami.config.aria2_port')
        aria2_secret = get_config('madokami.config.aria2_secret')
        if aria2_host is None or aria2_port is None or aria2_secret is None:
            raise ValueError('Aria2 configuration is not set')
        client = aria2p.Client(
                host=aria2_host,
                port=int(aria2_port),
                secret=aria2_secret
            )
        self.aria2 = aria2p.api.API(
            client
        )
        self.downloads = None
        self.client = client

    def download(self, uri: str, options: Options) -> list[Download]:
        self.downloads = self.aria2.add(uri, options)
        return self.downloads

    @property
    def status(self) -> Tuple[int, list[Download]]:
        return 200, self.downloads

    def cancel(self):
        pass

    def pause(self):
        pass

    @property
    def namespace(self) -> str:
        return 'madokami.summerkirakira.default_aria2_downloader'

    @property
    def name(self) -> str:
        return 'Default Aria2 Downloader'

    @property
    def description(self) -> str:
        return 'Default Aria2 Downloader for madokami'

    def get_options(self, gid: str):
        return self.aria2.get_download(gid)

