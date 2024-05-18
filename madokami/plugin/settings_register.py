from .backend.engine import Engine
from typing import Dict, Optional, Tuple
from pydantic import BaseModel
from madokami.db import engine, Session
from madokami.crud import get_plugin_config, add_plugin_config


class Setting(BaseModel):
    namespace: str
    key: str
    name: str
    description: str


_registered_settings: Dict[str, list[Setting]] = {}
# _registered_plugins: Dict[str, PluginInfo] = {}


def register_setting(key: str, name: str, description: str, plugin_namespace: Optional[str] = None, default: Optional[str] = None):
    if default is not None:
        with Session(engine) as session:
            config = get_plugin_config(session=session, key=key)
            if config is None:
                add_plugin_config(session=session, key=key, value=default)

    if plugin_namespace is None:
        plugin_namespace = 'madokami.default'
    setting = Setting(
        name=name,
        namespace=plugin_namespace,
        key=key,
        description=description
    )
    if plugin_namespace in _registered_settings:
        _registered_settings[plugin_namespace].append(setting)
    else:
        _registered_settings[plugin_namespace] = [setting]

    # _registered_plugins[plugin.namespace] = plugin


def get_registered_settings() -> Dict[str, list[Setting]]:
    return _registered_settings


