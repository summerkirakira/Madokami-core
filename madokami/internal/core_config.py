from madokami.crud import get_plugin_config, add_plugin_config
from typing import Optional
from madokami.db import engine
from sqlmodel import Session
from .models import PluginMetaData


def get_config(key: str, default: str = None) -> Optional[str]:
    with Session(engine) as session:
        value = get_plugin_config(session=session, key=key)
        if value is None:
            return default
        return value


def set_config(key: str, value: str) -> None:
    with Session(engine) as session:
        add_plugin_config(session=session, key=key, value=value)


def get_proxy_url() -> Optional[str]:
    config = get_config(key='madokami.config.proxy_url')
    if config == '':
        return None
    return config


_registered_metas: dict[str, PluginMetaData] = {}


def register_plugin_meta(plugin_meta: PluginMetaData):
    _registered_metas[plugin_meta.namespace] = plugin_meta


def get_plugin_meta(namespace: str) -> PluginMetaData:
    return _registered_metas[namespace]


def get_all_plugin_metas() -> dict[str, PluginMetaData]:
    return _registered_metas
