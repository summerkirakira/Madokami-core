from madokami.plugin.manager import PluginManager
from madokami.crud import add_plugin, get_plugins
from madokami.models import Plugin
from sqlmodel import Session
from madokami.db import engine


def init_plugins():
    with Session(engine) as session:
        plugins = get_plugins(session=session)
        for plugin in plugins:
            session.delete(plugin)
        session.commit()
        add_plugin(session=session, plugin=Plugin(namespace="test.test", is_active=False, name="test", description="test"))


def test_plugin_manager():
    init_plugins()
    plugin_manager = PluginManager()
    assert plugin_manager.plugins[0].namespace == "test.test"
