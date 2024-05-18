from ..db import Session, engine, init_db
from ..config import basic_config
from pathlib import Path
from madokami.plugin.manager import PluginManager
from madokami.internal.scheduler import MadokamiScheduler
from madokami.plugin.backend.engine import Engine, FileDownloaderEngine, SearchEngine
from apscheduler.triggers.cron import CronTrigger
from madokami.crud import get_engines_schedule_by_plugin_namespace
from .app import get_fastapi_app
from .router import get_registered_router, register_router
import uvicorn
from .hooks import app_hooks
from madokami.util import restart_program
from madokami.internal.default_plugins.default_downloader import DefaultAria2Downloader
from madokami.api import get_internal_routers


def pre_start():
    plugin_dir = Path.cwd() / 'data' / 'plugins'
    if not plugin_dir.exists():
        plugin_dir.mkdir(parents=True)
    init_db()


class MadokamiApp:
    def __init__(self):
        pre_start()
        self.plugin_manager = PluginManager()
        self.scheduler = MadokamiScheduler()
        self.app = get_fastapi_app()
        self.add_app_routers()
        self.downloader = DefaultAria2Downloader()

    def add_background_jobs(self):
        for plugin in self.plugin_manager.get_active_plugins():
            with Session(engine) as session:
                engines = get_engines_schedule_by_plugin_namespace(session=session, namespace=plugin.namespace)
            for registered_engine in engines:
                if not registered_engine.cron_str:
                    continue
                target_engine = self.plugin_manager.get_engine_by_namespace(registered_engine.namespace)
                if isinstance(target_engine, FileDownloaderEngine):
                    self.scheduler.add_engine(target_engine, CronTrigger.from_crontab(registered_engine.cron_str))

    def clear_background_jobs(self):
        self.scheduler.clear_all()

    def start_background_jobs(self):
        self.scheduler.start()

    def add_app_routers(self):
        self._register_internal_routers()
        router = get_registered_router()
        self.app.include_router(router=router, prefix='/v1')

    def start_fastapiapp(self):
        uvicorn.run(self.app, host=str(basic_config.host), port=basic_config.port)

    def start(self):
        for before_run_hook in app_hooks.get_before_startup_hooks():
            before_run_hook()

        self.add_background_jobs()
        self.start_background_jobs()
        self.start_fastapiapp()

        for after_run_hook in app_hooks.get_after_startup_hooks():
            after_run_hook()

    def restart_scheduler(self):
        self.scheduler.clear_all()
        self.add_background_jobs()
        self.start_background_jobs()

    def shutdown(self):

        for before_shutdown_hook in app_hooks.get_before_shutdown_hooks():
            before_shutdown_hook()

        self.clear_background_jobs()
        self.scheduler.shutdown()
        self.scheduler = None
        self.plugin_manager = None
        self.app = None

        for after_shutdown_hook in app_hooks.get_after_shutdown_hooks():
            after_shutdown_hook()

    @classmethod
    def _register_internal_routers(cls):
        for router in get_internal_routers():
            register_router(router)

    def restart(self):
        restart_program()
