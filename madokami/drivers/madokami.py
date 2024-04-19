from ..db import Session, engine, init_db
from ..config import basic_config
from pathlib import Path
from madokami.plugin.manager import PluginManager


def pre_start():
    plugin_dir = Path.cwd() / 'data' / 'plugins'
    if not plugin_dir.exists():
        plugin_dir.mkdir(parents=True)

    init_db()


class Launcher:
    def __init__(self):
        pre_start()
        self.plugin_manager = PluginManager()
