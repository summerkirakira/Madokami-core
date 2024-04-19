from madokami.internal.scheduler import scheduler
from madokami.plugin.manager import PluginManager, LOCAL_PLUGIN_DIR
from madokami.crud import add_plugin, get_plugins
from madokami.models import Plugin
from sqlmodel import Session
from madokami.db import engine
import shutil
from pathlib import Path
from apscheduler.triggers.cron import CronTrigger
from madokami.plugin import plugin_hooks
from madokami.plugin.backend.engine import Engine


def init_plugins():
    with Session(engine) as session:
        plugins = get_plugins(session=session)
        for plugin in plugins:
            session.delete(plugin)
        session.commit()
        add_plugin(session=session, plugin=Plugin(namespace="test.test", is_active=False, name="test", description="test"))


def rm_local_plugins():
    shutil.rmtree(LOCAL_PLUGIN_DIR / "test_plugin", ignore_errors=True)


def test_scheduler():
    plugin_manager = PluginManager()
    init_plugins()
    rm_local_plugins()
    plugin_manager.add_local_plugin(Path("tests/plugin/test_plugin"))

    reloaded_manager = PluginManager()
    # assert len(reloaded_manager.plugin_names_from_db) == 1
    assert len(reloaded_manager.registered_engines) == 1
    assert reloaded_manager.registered_engines["summerkirakira.test_engine"] is not None

    @plugin_hooks.before_run
    def before_run(engine: Engine):
        assert engine.namespace == "summerkirakira.test_engine"

    @plugin_hooks.after_run
    def after_run(engine: Engine, result):
        assert result is None
        assert engine.namespace == "summerkirakira.test_engine"


    for plugin in reloaded_manager.get_active_plugins():
        scheduler.add_engine(reloaded_manager.get_engine_by_namespace(plugin.namespace), CronTrigger.from_crontab("* * * * *"))
    scheduler.start()

    assert len(scheduler.scheduler.get_jobs()) == 1

