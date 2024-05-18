from madokami.internal.default_plugins.default_downloader import DefaultAria2Downloader, Download
from madokami import set_config
import pytest


@pytest.mark.skip(reason="Test not implemented")
def test_downloader(database):
    set_config('madokami.config.aria2_host', 'http://localhost')
    set_config('madokami.config.aria2_port', '6800')
    set_config('madokami.config.aria2_secret', '')
    downloader = DefaultAria2Downloader()
    download_info = downloader.add_download(
        uri='https://www.baidu.com/',
        callback=lambda download: "Hello World"
    )

