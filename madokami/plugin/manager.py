from ..crud import get_plugins
from ..db import engine
from ..models import Plugin as PluginInfo
from sqlmodel import Session
import pkgutil
from pkgutil import ModuleInfo
from pathlib import Path
from pydantic import BaseModel
from typing import Literal, Dict
import os
import shutil
from ..crud import add_plugin, get_plugin_by_namespace
import importlib
from .backend.engine import Engine
from .engine_register import get_registered_engines


def load_plugin_names_from_db() -> list[PluginInfo]:
    with Session(engine) as session:
        plugins = get_plugins(session=session)
        return plugins


def is_python_package(path: Path) -> bool:
    return (path / "__init__.py").exists()


class Plugin(BaseModel):
    name: str
    namespace: str
    type: Literal["local", "package"]


LOCAL_PLUGIN_DIR = Path.cwd() / "data" / "plugins"
if not LOCAL_PLUGIN_DIR.exists():
    os.makedirs(LOCAL_PLUGIN_DIR)


LOCAL_PLUGIN_PACKAGE_PREFIX = "data.plugins"


def _copy_plugin_to_local_path(dir_path: Path):
    if not dir_path.exists():
        raise FileNotFoundError(f"Plugin {dir_path} not found")
    if not dir_path.is_dir():
        raise NotADirectoryError(f"{dir_path} is not a directory")

    shutil.rmtree(LOCAL_PLUGIN_DIR / dir_path.name, ignore_errors=True)
    shutil.copytree(dir_path, LOCAL_PLUGIN_DIR / dir_path.name)


class PluginManager:
    def __init__(self):
        self.plugin_names_from_db: list[PluginInfo] = load_plugin_names_from_db()
        self.search_path: set[Path] = set()
        self.search_path.add(LOCAL_PLUGIN_DIR)
        self.registered_engines: Dict[str, Engine] = {}
        self._load_local_plugins()

    def _get_local_plugins(self) -> list[ModuleInfo]:
        modules = []
        for path in self.search_path:
            if not path.exists():
                continue
        for module in pkgutil.iter_modules([str(path) for path in self.search_path]):
            modules.append(module)
        return modules

    def add_local_plugin(self, plugin_path: Path):
        if not is_python_package(plugin_path):
            raise ValueError(f"{plugin_path} is not a python package")
        _copy_plugin_to_local_path(plugin_path)

    def _load_local_plugins(self):
        for module in self._get_local_plugins():
            importlib.import_module(f"{LOCAL_PLUGIN_PACKAGE_PREFIX}.{module.name}")
        self._register_engine()

    def _register_engine(self):
        with Session(engine) as session:
            for plugin_engine in get_registered_engines():
                exist_plugin = get_plugin_by_namespace(session=session, namespace=plugin_engine.namespace)
                if not exist_plugin:
                    plugin_info = PluginInfo(
                        name=plugin_engine.name,
                        namespace=plugin_engine.namespace,
                        description=plugin_engine.description,
                        is_active=True)
                    add_plugin(session=session, plugin=plugin_info)
                self.registered_engines[plugin_engine.namespace] = plugin_engine
        self.plugin_names_from_db = load_plugin_names_from_db()

    def get_active_plugins(self) -> list[PluginInfo]:
        return [plugin for plugin in self.plugin_names_from_db if plugin.is_active]

    def get_engine_by_namespace(self, namespace: str) -> Engine:
        return self.registered_engines[namespace]


plugin_manager = PluginManager()