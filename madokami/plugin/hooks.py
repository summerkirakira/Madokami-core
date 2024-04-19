from ..plugin.backend.engine import Engine
from typing import Callable, List


class PluginHooks:
    def __init__(self):
        self._before_run_hooks: list[Callable] = []
        self._after_run_hooks: list[Callable] = []
        self._before_cancel_hooks: list[Callable] = []
        self._after_cancel_hooks: list[Callable] = []

    def before_run(self, func):
        self._before_run_hooks.append(func)
        return func

    def after_run(self, func):
        self._after_run_hooks.append(func)
        return func

    def before_shutdown(self, func):
        self._before_cancel_hooks.append(func)
        return func

    def after_shutdown(self, func):
        self._after_cancel_hooks.append(func)
        return func

    def get_before_run_hooks(self) -> List[Callable]:
        return self._before_run_hooks

    def get_after_run_hooks(self) -> List[Callable]:
        return self._after_run_hooks


plugin_hooks = PluginHooks()

