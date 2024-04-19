from .backend.engine import Engine
from madokami.models import Plugin, PluginInfo
from typing import Dict, Optional, Tuple
from ..models import Plugin
from pydantic import BaseModel


_registered_engines: Dict[str, list[Engine]] = {}
_registered_plugins: Dict[str, PluginInfo] = {}


def register_engine(plugin: PluginInfo, engine: Engine):
    if plugin.namespace in _registered_engines:
        _registered_engines[plugin.namespace].append(engine)
    else:
        _registered_engines[plugin.namespace] = [engine]

    _registered_plugins[plugin.namespace] = plugin


def get_registered_engines() -> Tuple[Dict[str, PluginInfo], Dict[str, list[Engine]]]:
    return _registered_plugins, _registered_engines


