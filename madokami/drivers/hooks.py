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


app_hooks = AppHooks()

