from fastapi import APIRouter, HTTPException, Depends
from .models import UserCreate, UserResponse, InfoMessage
from madokami.drivers.deps import SessionDep, get_client_id

engine_router = APIRouter(tags=["Engine"])


@engine_router.get("/engine/run", response_model=InfoMessage, dependencies=[Depends(get_client_id)])
def run_engine(engine_namespace: str):
    from madokami import get_app
    app = get_app()
    try:
        my_engine = app.plugin_manager.get_engine_by_namespace(engine_namespace)
        my_engine.run()
        return InfoMessage(message='Engine started')
    except Exception as e:
        return InfoMessage(message=f'Failed to start engine: {e}', success=False)


@engine_router.get("/engine/run-all", response_model=InfoMessage, dependencies=[Depends(get_client_id)])
def refresh_all_engines():
    from madokami import get_app
    app = get_app()
    try:
        engines = app.plugin_manager.registered_engines.values()
        for engine in engines:
            engine.run()
        return InfoMessage(message='Engines refreshed')
    except Exception as e:
        return InfoMessage(message=f'Failed to refresh engines: {e}', success=False)