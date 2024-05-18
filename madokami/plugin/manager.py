from ..crud import get_plugins,get_engine_scheduler_config, add_engine_scheduler_config
from ..db import engine
from ..models import Plugin as PluginInfo, EngineSchedulerConfig
from sqlmodel import Session
import pkgutil
from pkgutil import ModuleInfo
from pathlib import Path
from pydantic import BaseModel
from typing import Literal, Dict, Union
import os
import shutil
from ..crud import add_plugin, get_plugin_by_namespace
import importlib
from .backend.engine import Engine
from .engine_register import get_registered_engines
from ..log import logger
from typing import Tuple, Any, Type
from madokami.internal.models import PluginMetaData
from madokami.internal.core_config import get_config, get_all_plugin_metas, register_plugin_meta
from madokami.plugin import register_engine
from madokami.plugin.subscription_regiser import register_subscription_manager, get_registered_subscription_managers
from .settings_register import register_setting, get_registered_settings
from madokami.internal.settings import register_internal_settings


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
INTERNAL_PLUGIN_DIR = Path.cwd() / "app" / "plugins"


if not LOCAL_PLUGIN_DIR.exists():
    os.makedirs(LOCAL_PLUGIN_DIR)


LOCAL_PLUGIN_PACKAGE_PREFIX = "data.plugins"
INTERNAL_PLUGIN_PACKAGE_PREFIX = "app.plugins"


def _copy_plugin_to_local_path(dir_path: Path):
    if not dir_path.exists():
        raise FileNotFoundError(f"Plugin {dir_path} not found")
    if not dir_path.is_dir():
        raise NotADirectoryError(f"{dir_path} is not a directory")

    shutil.rmtree(LOCAL_PLUGIN_DIR / dir_path.name, ignore_errors=True)
    shutil.copytree(dir_path, LOCAL_PLUGIN_DIR / dir_path.name)


def _register_meta_from_module(module: Any):
    metadata = getattr(module, '__metadata__', None)
    if not metadata:
        return None
    try:
        plugin_meta = PluginMetaData.model_validate(metadata)
    except Exception as e:
        logger.error(f"Failed to validate metadata from {module.__name__}: {e}")
        return None
    register_plugin_meta(plugin_meta)
    for plugin_engine in plugin_meta.engines:
        try:
            new_engine: Type[Engine] = getattr(module, plugin_engine)
            if not issubclass(new_engine, Engine):
                logger.error(f"Engine {new_engine} is not a subclass of Engine")
                continue
            register_engine(plugin_meta.namespace, new_engine())
            for setting in plugin_meta.settings:
                register_setting(setting.key, setting.name, setting.description, plugin_meta.namespace, setting.default)
        except Exception as e:
            logger.error(f"Failed to register engine {plugin_engine} from {module.__name__}: {e}")

    try:
        if plugin_meta.subscription_manager:
            register_subscription_manager(plugin_meta.namespace, plugin_meta.subscription_manager)
    except Exception as e:
        logger.error(f"Failed to register subscription function from {module.__name__}: {e}")


class PluginManager:
    def __init__(self):
        self.plugin_names_from_db: list[PluginInfo] = load_plugin_names_from_db()
        self.search_path: set[Path] = set()
        self.search_path.add(LOCAL_PLUGIN_DIR)
        self.search_path.add(INTERNAL_PLUGIN_DIR)
        self.registered_engines: Dict[str, Engine] = {}
        self._register_internal_settings()
        self._load_local_plugins()
        self._load_package_plugins()
        self._register_engine()
        self.subscription_managers = get_registered_subscription_managers()
        self.settings = get_registered_settings()

    @classmethod
    def _get_local_plugins(cls) -> [list[ModuleInfo], list[ModuleInfo]]:
        internal_modules = []
        for module in pkgutil.iter_modules([str(INTERNAL_PLUGIN_DIR)]):
            internal_modules.append(module)

        local_modules = []
        for module in pkgutil.iter_modules([str(LOCAL_PLUGIN_DIR)]):
            local_modules.append(module)

        return internal_modules, local_modules

    def add_local_plugin(self, plugin_path: Path):
        if not is_python_package(plugin_path):
            raise ValueError(f"{plugin_path} is not a python package")
        _copy_plugin_to_local_path(plugin_path)

    def _load_local_plugins(self):
        internal_modules, local_modules = self._get_local_plugins()
        for module in local_modules:
            try:
                plugin = importlib.import_module(f"{LOCAL_PLUGIN_PACKAGE_PREFIX}.{module.name}")
                _register_meta_from_module(plugin)
                logger.info(f"Loaded local plugin {module.name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {module.name}: {e}")

        for module in internal_modules:
            try:
                plugin = importlib.import_module(f"{INTERNAL_PLUGIN_PACKAGE_PREFIX}.{module.name}")
                _register_meta_from_module(plugin)
                logger.info(f"Loaded internal plugin {module.name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {module.name}: {e}")
                raise e

    def _load_package_plugins(self):
        for plugin in self.plugin_names_from_db:
            if plugin.namespace in self.registered_engines:
                continue
            if not plugin.is_active:
                continue
            if plugin.is_local_plugin:
                continue
            if plugin.is_internal:
                logger.info(f"Skipping internal plugin {plugin.namespace}")
                continue
            try:
                if '.' in plugin.namespace:
                    package_name = plugin.namespace.split('.')[-1]
                else:
                    package_name = plugin.namespace
                plugin = importlib.import_module(package_name)
                _register_meta_from_module(plugin)
                logger.info(f"Loaded package plugin {plugin.namespace}")
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin.namespace}: {e}")

    @classmethod
    def _register_internal_settings(cls):
        register_internal_settings()

    def _register_engine(self):
        with Session(engine) as session:
            registered_engines = get_registered_engines()
            plugin_metas = get_all_plugin_metas()
            for plugin_namespace, engines in registered_engines.items():
                exist_plugin = get_plugin_by_namespace(session=session, namespace=plugin_namespace)
                if not exist_plugin:
                    registered_plugin = plugin_metas[plugin_namespace]
                    plugin_info = PluginInfo(
                        name=registered_plugin.name,
                        namespace=registered_plugin.namespace,
                        description=registered_plugin.description,
                        is_local_plugin=True,
                        is_active=True)
                    # logger.info(f"Adding plugin {plugin_name} to database")
                    add_plugin(session=session, plugin=plugin_info)
                for plugin_engine in engines:
                    self.registered_engines[plugin_engine.namespace] = plugin_engine
                    if not get_engine_scheduler_config(session=session, namespace=plugin_engine.namespace):

                        engine_info = EngineSchedulerConfig(
                            namespace=plugin_engine.namespace,
                            plugin_name=plugin_namespace,
                            cron_str=None,
                        )

                        add_engine_scheduler_config(
                            session=session,
                            engine_scheduler_config=engine_info)

        self.plugin_names_from_db = load_plugin_names_from_db()

    def get_active_plugins(self) -> list[PluginInfo]:
        return [plugin for plugin in self.plugin_names_from_db if plugin.is_active]

    def get_engine_by_namespace(self, namespace: str) -> Engine:
        if namespace not in self.registered_engines:
            raise ValueError(f"Engine {namespace} not found")
        return self.registered_engines[namespace]

