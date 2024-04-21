from typing import Optional, Callable
from ..downloader import Downloader, Download, DownloadStatus
from madokami import get_config
import aria2p
from aria2p.downloads import Download as Aria2Download
from typing import Optional, Callable, Any
from madokami.log import logger
import uuid
import threading
import time


def _convert_aria2_download(aria2_download: Aria2Download, finished_callback: Optional[Callable[[Download], None]] = None) -> Download:
    status = DownloadStatus.DOWNLOADING
    error_message = None
    file = aria2_download.files[0]
    if aria2_download.is_paused:
        status = DownloadStatus.PAUSED
    elif aria2_download.is_complete:
        status = DownloadStatus.COMPLETED
    elif aria2_download.is_active:
        status = DownloadStatus.DOWNLOADING
    elif aria2_download.is_removed:
        status = DownloadStatus.REMOVED
    elif aria2_download.error_code is not None:
        status = DownloadStatus.FAILED
        error_message = aria2_download.error_message

    download = Download(
        id=aria2_download.gid,
        is_metadata=file.is_metadata,
        name=aria2_download.name,
        target_path=file.path,
        dir=aria2_download.dir,
        total_length=aria2_download.total_length,
        progress=aria2_download.progress,
        current_download=aria2_download.completed_length,
        status=status,
        current_speed=aria2_download.download_speed,
        finished_callback=finished_callback,
        move_up=aria2_download.move_up,
        move_to_bottom=aria2_download.move_to_bottom,
        move_down=aria2_download.move_down,
        purge=aria2_download.purge,
        pause=aria2_download.pause,
        resume=aria2_download.resume,
        remove=aria2_download.remove,
        error_message=error_message,
    )
    download.finished_callback = lambda : finished_callback(download)
    return download


class DefaultAria2Downloader(Downloader):

    def __init__(self):
        self._status = "Initialized"
        aria2_host = get_config('madokami.config.aria2_host', default='http://localhost')
        aria2_port = get_config('madokami.config.aria2_port', default='6800')
        aria2_secret = get_config('madokami.config.aria2_secret', default='')
        if aria2_host is None or aria2_port is None or aria2_secret is None:
            raise ValueError('Aria2 configuration is not set')
        client = aria2p.Client(
            host=aria2_host,
            port=int(aria2_port),
            secret=aria2_secret
        )
        self.aria2 = aria2p.api.API(client)
        self.downloads: dict[str, Aria2Download] = {}
        self.client = client
        self._callback_map: dict[str, Callable] = {}
        self.finished_downloads: list[Download] = []

        self.refresh_thread = threading.Thread(target=self.refresh_thread)
        self.refresh_thread.start()

    def check_finished(self):
        for uid, download in self.downloads.items():
            if download.is_complete and uid not in [finished_download.id for finished_download in self.finished_downloads]:
                finished_download = _convert_aria2_download(download, self._callback_map.get(uid))
                finished_download.id = uid
                callback = self._callback_map.get(uid)
                if callback:
                    callback(finished_download)
                self.finished_downloads.append(finished_download)
                logger.info(f"Download {finished_download.name} is finished and file has been saved to {finished_download.target_path}")

    def refresh_thread(self):
        while True:
            self._refresh_downloads()
            self.check_finished()
            time.sleep(5)

    @property
    def namespace(self) -> str:
        return 'madokami.summerkirakira.default_aria2_downloader'

    @property
    def name(self) -> str:
        return 'Default Aria2 Downloader'

    @property
    def description(self) -> str:
        return 'Default Aria2 Downloader for madokami'

    def get_downloads(self) -> dict[str, Download]:
        converted_downloads = {}
        for uid, download in self.downloads.items():
            converted_download = _convert_aria2_download(download, self._callback_map.get(uid))
            converted_download.id = uid
            converted_downloads[uid] = converted_download
        return converted_downloads

    def get_download_by_id(self, download_id: str) -> Optional[Download]:
        if download := self.downloads.get(download_id):
            converted_download = _convert_aria2_download(download, self._callback_map.get(download_id))
            converted_download.id = download_id
            return converted_download

    def add_download(self, uri: str, options: dict = None, callback: Optional[Callable] = None) -> Download:
        downloads = self.aria2.add(uri, options)
        uid = str(uuid.uuid4())
        self._callback_map[uid] = callback
        self.downloads[uid] = downloads[0]

        converted_download = _convert_aria2_download(downloads[0], callback)
        converted_download.id = uid
        return converted_download

    def _refresh_downloads(self):
        for uid, download in self.downloads.items():
            download.update()
            if len(download.followed_by) == 1:
                self.downloads[uid] = download.followed_by[0]
            if download.error_code == '12':
                all_downloads = self.aria2.get_downloads()
                for old_download in all_downloads:
                    if (old_download.is_active or old_download.is_complete) and old_download.info_hash == download.info_hash:
                        if len(old_download.followed_by) == 1:
                            self.downloads[uid] = old_download.followed_by[0]
                        else:
                            self.downloads[uid] = old_download
                        break

    def refresh(self):
        self._refresh_downloads()

