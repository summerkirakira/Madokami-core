from apscheduler.schedulers.background import BackgroundScheduler
from ..plugin.backend.engine import Engine
import uuid
from typing import Dict, Callable
from ..plugin import plugin_hooks


class MadokamiScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self._job_id_dict: Dict[str, Callable] = {}
        self._engine_id_dict: Dict[str, Engine] = {}

    def add_job(self, func, trigger) -> str:
        job_id = str(uuid.uuid4())
        self._job_id_dict[job_id] = func
        self.scheduler.add_job(func, trigger, id=job_id)
        return job_id

    def remove_job(self, job_id) -> Callable:
        if job_id not in self._job_id_dict:
            raise ValueError(f"Job with id {job_id} not found")
        job = self._job_id_dict.pop(job_id)
        self.scheduler.remove_job(job_id)
        return job

    def add_engine(self, engine: Engine, trigger) -> str:
        engine_id = str(uuid.uuid4())
        self._engine_id_dict[engine_id] = engine

        def new_job():
            result = engine.run()
            for hook in plugin_hooks.get_after_run_hooks():
                hook(engine, result)

        for hook in plugin_hooks.get_before_run_hooks():
            hook(engine)

        self.scheduler.add_job(new_job, trigger, id=engine_id)
        return engine_id

    def remove_engine(self, engine_id) -> Engine:
        if engine_id not in self._engine_id_dict:
            raise ValueError(f"Engine with id {engine_id} not found")
        engine = self._engine_id_dict.pop(engine_id)
        self.remove_job(engine_id)
        return engine

    def clear_all(self):
        self.scheduler.remove_all_jobs()

    def get_running_engines(self) -> Dict[str, Engine]:
        return self._engine_id_dict

    def get_running_jobs(self) -> Dict[str, Callable]:
        return self._job_id_dict

    def get_running_engine_by_namespace(self, namespace: str) -> Dict[str, Engine]:
        result = {k: v for k, v in self._engine_id_dict.items() if v.namespace == namespace}
        return result

    def start(self):
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()


# scheduler = MadokamiScheduler()
