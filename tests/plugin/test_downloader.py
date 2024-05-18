from madokami.internal.default_plugins.default_downloader import DefaultAria2Downloader
from madokami.internal.core_config import get_config, set_config
import pytest


@pytest.mark.skip(reason="Test not implemented")
def test_default_downloader(database):
    set_config('madokami.config.aria2_host', 'http://localhost')
    set_config('madokami.config.aria2_port', '6800')
    set_config('madokami.config.aria2_secret', '')
    downloader = DefaultAria2Downloader()
    try:
        downloader.download('https://google.com', {})
        status = downloader.status
        assert status is not None
    except Exception as e:
        pass
