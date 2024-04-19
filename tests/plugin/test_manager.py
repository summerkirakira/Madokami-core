from madokami.plugin.manager import PluginManager, LOCAL_PLUGIN_DIR
from madokami.crud import add_plugin, get_plugins
from madokami.models import Plugin
from sqlmodel import Session
from madokami.db import engine
import shutil
from pathlib import Path


def init_plugins():
    with Session(engine) as session:
        plugins = get_plugins(session=session)
        for plugin in plugins:
            session.delete(plugin)
        session.commit()
        add_plugin(session=session, plugin=Plugin(namespace="test.test", is_active=False, name="test", description="test"))


def rm_local_plugins():
    shutil.rmtree(LOCAL_PLUGIN_DIR / "test_plugin", ignore_errors=True)


def test_plugin_manager(database):
    plugin_manager = PluginManager()
    init_plugins()
    rm_local_plugins()
    plugin_manager.add_local_plugin(Path("tests/plugin/test_plugin"))

    reloaded_manager = PluginManager()
    # assert len(reloaded_manager.plugin_names_from_db) == 1
    assert len(reloaded_manager.registered_engines) == 1
    assert reloaded_manager.registered_engines["summerkirakira.test_engine"] is not None
