from fastapi import APIRouter, HTTPException, Depends
from .models import UserCreate, UserResponse, InfoMessage, AllScheduledTasksResponse, UpdateCronBody
from madokami.drivers.deps import SessionDep, get_client_id
from madokami.crud import get_engine_schedule_configs, update_engine_scheduler_config

scheduler_router = APIRouter(tags=["Scheduler"])


@scheduler_router.get("/schedule/restart", response_model=InfoMessage, dependencies=[Depends(get_client_id)])
def restart_scheduler():
    from madokami import get_app
    app = get_app()
    try:
        app.restart_scheduler()
        return InfoMessage(message='Scheduler started')
    except Exception as e:
        return InfoMessage(message=f'Failed to restart scheduler: {e}', success=False)


@scheduler_router.get("/schedule/all", response_model=AllScheduledTasksResponse, dependencies=[Depends(get_client_id)])
def get_all_schedules(session: SessionDep):
    from madokami import get_app
    app = get_app()
    try:
        schedules = get_engine_schedule_configs(session)
        plugins: dict[str, AllScheduledTasksResponse.Plugin] = {}
        for schedule in schedules:
            if schedule.plugin_name not in plugins:
                plugins[schedule.plugin_name] = AllScheduledTasksResponse.Plugin(
                    namespace=schedule.plugin_name,
                    tasks=[]
                )
            if (engine :=app.plugin_manager.get_engine_by_namespace(schedule.namespace)) is not None:
                plugins[schedule.plugin_name].tasks.append(
                    AllScheduledTasksResponse.Plugin.ScheduledTask(
                        id=schedule.id,
                        cron_str=schedule.cron_str,
                        namespace=schedule.namespace,
                        name=engine.name,
                        description=engine.description
                    )
                )
        return AllScheduledTasksResponse(data=list(plugins.values()))
    except Exception as e:
        return AllScheduledTasksResponse(message=f'Failed to retrieve schedules: {e}', success=False)


@scheduler_router.post("/schedule/update", response_model=InfoMessage, dependencies=[Depends(get_client_id)])
def update_schedule(update_body: UpdateCronBody, session: SessionDep):
    from madokami import get_app
    app = get_app()
    try:
        update_engine_scheduler_config(session=session, engine_scheduler_id=update_body.schedule_id, cron_str=update_body.cron_str)
        return InfoMessage(message='Schedule updated')
    except Exception as e:
        return InfoMessage(message=f'Failed to update schedule: {e}', success=False)
