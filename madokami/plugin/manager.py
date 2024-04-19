from ..crud import get_plugins,get_engine_scheduler_config, add_engine_scheduler_config
from ..db import engine
from ..models import Plugin as PluginInfo, EngineSchedulerConfig
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
from ..log import logger


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
        self._load_package_plugins()
        self._register_engine()

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
            try:
                importlib.import_module(f"{LOCAL_PLUGIN_PACKAGE_PREFIX}.{module.name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {module.name}: {e}")

    def _load_package_plugins(self):
        for plugin in self.plugin_names_from_db:
            if plugin.namespace in self.registered_engines:
                continue
            if not plugin.is_active:
                continue
            try:
                if '.' in plugin.namespace:
                    package_name = plugin.namespace.split('.')[-1]
                else:
                    package_name = plugin.namespace
                importlib.import_module(package_name)
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin.namespace}: {e}")

    def _register_engine(self):
        with Session(engine) as session:
            registered_plugins, registered_engines = get_registered_engines()
            for plugin_namespace, engines in registered_engines.items():
                exist_plugin = get_plugin_by_namespace(session=session, namespace=plugin_namespace)
                if not exist_plugin:
                    registered_plugin = registered_plugins[plugin_namespace]
                    plugin_info = PluginInfo(
                        name=registered_plugin.name,
                        namespace=registered_plugin.namespace,
                        description=registered_plugin.description,
                        is_active=True)
                    # logger.info(f"Adding plugin {plugin_name} to database")
                    add_plugin(session=session, plugin=plugin_info)
                for plugin_engine in engines:
                    self.registered_engines[plugin_engine.namespace] = plugin_engine
                    if not get_engine_scheduler_config(session=session, namespace=plugin_engine.namespace):

                        engine_info = EngineSchedulerConfig(
                            namespace=plugin_engine.namespace,
                            plugin_name=plugin_namespace,
                            cron_str="* * * 32 2",
                        )

                        add_engine_scheduler_config(
                            session=session,
                            engine_scheduler_config=engine_info)

        self.plugin_names_from_db = load_plugin_names_from_db()

    def get_active_plugins(self) -> list[PluginInfo]:
        return [plugin for plugin in self.plugin_names_from_db if plugin.is_active]

    def get_engine_by_namespace(self, namespace: str) -> Engine:
        return self.registered_engines[namespace]


# plugin_manager = PluginManager()