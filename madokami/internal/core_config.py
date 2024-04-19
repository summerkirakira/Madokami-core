from madokami.crud import get_plugin_config, add_plugin_config
from typing import Optional
from madokami.db import engine
from sqlmodel import Session


def get_config(key: str) -> Optional[str]:
    with Session(engine) as session:
        return get_plugin_config(session=session, key=key)


def set_config(key: str, value: str) -> None:
    with Session(engine) as session:
        add_plugin_config(session=session, key=key, value=value)


def get_proxy_url() -> Optional[str]:
    return get_config(key='madokami.config.proxy_url')

