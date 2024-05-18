from fastapi import APIRouter, Depends
from .models import LogResponse
from madokami.log import message_storage_handler
from madokami.drivers.deps import get_client_id

logs_router = APIRouter(tags=["Log"])


@logs_router.get("/log/all", response_model=LogResponse, dependencies=[Depends(get_client_id)])
def _get_log_all():
    try:
        return LogResponse(data=message_storage_handler.get_messages())
    except Exception as e:
        return LogResponse(message=f"Failed to load message: {e}", success=False)


