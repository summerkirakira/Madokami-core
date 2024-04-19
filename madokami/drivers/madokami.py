from ..db import Session, engine, init_db
from ..config import basic_config
from pathlib import Path
from madokami.plugin.manager import PluginManager
from madokami.internal.scheduler import MadokamiScheduler
from fastapi import FastAPI
from apscheduler.triggers.cron import CronTrigger
from madokami.crud import get_engines_schedule_by_plugin_namespace
from .app import get_fastapi_app
from .router import get_registered_router
import uvicorn
from .hooks import app_hooks
from madokami.util import restart_program


def pre_start():
    plugin_dir = Path.cwd() / 'data' / 'plugins'
    if not plugin_dir.exists():
        plugin_dir.mkdir(parents=True)
    init_db()


class Launcher:
    def __init__(self):
        pre_start()
        self._plugin_manager = PluginManager()
        self._scheduler = MadokamiScheduler()
        self._app = get_fastapi_app()
        self.add_app_routers()

    def add_background_jobs(self):
        for plugin in self._plugin_manager.get_active_plugins():
            with Session(engine) as session:
                engines = get_engines_schedule_by_plugin_namespace(session=session, namespace=plugin.namespace)
            for registered_engine in engines:
                if not registered_engine.cron_str:
                    continue
                self._scheduler.add_engine(self._plugin_manager.get_engine_by_namespace(registered_engine.namespace),  CronTrigger.from_crontab(registered_engine.cron_str))

    def clear_background_jobs(self):
        self._scheduler.clear_all()

    def start_background_jobs(self):
        self._scheduler.start()

    def add_app_routers(self):
        self._app.include_router(get_registered_router())

    def start_fastapi_app(self):
        uvicorn.run(self._app, host=str(basic_config.host), port=basic_config.port)

    def start(self):
        for before_run_hook in app_hooks.get_before_startup_hooks():
            before_run_hook()

        self.add_background_jobs()
        self.start_background_jobs()
        self.start_fastapi_app()

        for after_run_hook in app_hooks.get_after_startup_hooks():
            after_run_hook()

    def shutdown(self):

        for before_shutdown_hook in app_hooks.get_before_shutdown_hooks():
            before_shutdown_hook()

        self.clear_background_jobs()
        self._scheduler.shutdown()
        self._scheduler = None
        self._plugin_manager = None
        self._app = None

        for after_shutdown_hook in app_hooks.get_after_shutdown_hooks():
            after_shutdown_hook()


    def restart(self):
        restart_program()
