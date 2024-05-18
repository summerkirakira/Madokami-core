from fastapi import APIRouter, HTTPException, Depends
from .models import UserCreate, UserResponse, PluginInfoResponse
from madokami.drivers.deps import SessionDep, get_client_id
from madokami.crud import get_engines_schedule_by_plugin_namespace

plugin_router = APIRouter(tags=["Plugin"])


@plugin_router.get("/plugin/info", response_model=PluginInfoResponse, dependencies=[Depends(get_client_id)])
def run_engine(session: SessionDep):
    from madokami import get_app
    app = get_app()
    try:
        plugins_info = app.plugin_manager.get_active_plugins()
        plugin_response_list: list[PluginInfoResponse.PluginInfo] = []
        for plugin in plugins_info:
            schedule_cron_list = get_engines_schedule_by_plugin_namespace(session=session, namespace=plugin.namespace)
            engines: list[PluginInfoResponse.PluginInfo.Engine] = []
            for schedule_cron in schedule_cron_list:
                engine_instance = app.plugin_manager.get_engine_by_namespace(schedule_cron.namespace)
                engines.append(
                    PluginInfoResponse.PluginInfo.Engine(
                        namespace=schedule_cron.namespace,
                        cron_str=schedule_cron.cron_str,
                        name=engine_instance.name,
                        description=engine_instance.description,
                    )
                )

            plugin_response_list.append(PluginInfoResponse.PluginInfo(
                    name=plugin.name,
                    namespace=plugin.namespace,
                    engines=engines,
                    description=plugin.description,
                    is_local_plugin=plugin.is_local_plugin,
                    is_internal=plugin.is_internal,
                )
            )
        return PluginInfoResponse(data=plugin_response_list)

    except Exception as e:
        return PluginInfoResponse(message=f'Failed to get plugins info: {e}', success=False)
