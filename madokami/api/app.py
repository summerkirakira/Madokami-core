from fastapi import APIRouter, Depends
from .models import InfoMessage
from madokami.drivers.deps import get_client_id

app_router = APIRouter(tags=["App"])


@app_router.get("/app/restart", response_model=InfoMessage, dependencies=[Depends(get_client_id)])
def _get_log_all():
    from madokami import get_app
    app = get_app()
    try:
        app.restart()
        return InfoMessage(message='Restarting app')
    except Exception as e:
        return InfoMessage(message=f"Failed to restart app: {e}", success=False)


