from .backend.engine import Engine
from madokami.models import Plugin, PluginInfo
from typing import Dict, Optional, Tuple


_registered_engines: Dict[str, list[Engine]] = {}
# _registered_plugins: Dict[str, PluginInfo] = {}


def register_engine(plugin_namespace: str, engine: Engine):
    if plugin_namespace in _registered_engines:
        _registered_engines[plugin_namespace].append(engine)
    else:
        _registered_engines[plugin_namespace] = [engine]

    # _registered_plugins[plugin.namespace] = plugin


def get_registered_engines() -> Dict[str, list[Engine]]:
    return _registered_engines


