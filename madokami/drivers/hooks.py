from typing import List, Callable


class AppHooks:
    def __init__(self):
        self._before_startup_hooks: List[Callable] = []
        self._after_startup_hooks: List[Callable] = []
        self._before_shutdown_hooks: List[Callable] = []
        self._after_shutdown_hooks: List[Callable] = []

    def before_startup(self, func):
        self._before_startup_hooks.append(func)
        return func

    def after_startup(self, func):
        self._after_startup_hooks.append(func)
        return func

    def before_shutdown(self, func):
        self._before_shutdown_hooks.append(func)
        return func

    def after_shutdown(self, func):
        self._after_shutdown_hooks.append(func)
        return func

    def get_before_startup_hooks(self) -> List[Callable]:
        return self._before_startup_hooks

    def get_after_startup_hooks(self) -> List[Callable]:
        return self._after_startup_hooks

    def get_before_shutdown_hooks(self) -> List[Callable]:
        return self._before_shutdown_hooks

    def get_after_shutdown_hooks(self) -> List[Callable]:
        return self._after_shutdown_hooks


class DownloadHooks:
    def __init__(self):
        self._before_download_hooks: List[Callable] = []
        self._after_download_hooks: List[Callable] = []

    def before_download(self, func):
        self._before_download_hooks.append(func)
        return func

    def after_download(self, func):
        self._after_download_hooks.append(func)
        return func

    def get_before_download_hooks(self) -> List[Callable]:
        return self._before_download_hooks

    def get_after_download_hooks(self) -> List[Callable]:
        return self._after_download_hooks

    def add_before_download_hook(self, func):
        self._before_download_hooks.append(func)
        return func

    def add_after_download_hook(self, func):
        self._after_download_hooks.append(func)
        return func


app_hooks = AppHooks()

download_hooks = DownloadHooks()


