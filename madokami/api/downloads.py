from fastapi import APIRouter, Depends
from .models import InfoMessage, DownloadResponse, DownloadItem, DownloadData
from madokami.drivers.deps import SessionDep, get_client_id
from madokami.internal.downloader import Download

download_router = APIRouter(tags=["Download"])


def convert_download(download: Download) -> DownloadData:
    return DownloadData(
        id=download.id,
        is_metadata=download.is_metadata,
        name=download.name,
        target_path=str(download.target_path),
        dir=str(download.dir),
        total_length=download.total_length,
        progress=download.progress,
        current_download=download.current_download,
        status=download.status.value,
        current_speed=download.current_speed
    )


@download_router.get("/download/all", response_model=DownloadResponse, dependencies=[Depends(get_client_id)])
def get_downloads():
    from madokami import get_app
    app = get_app()
    try:
        downloads = app.downloader.get_downloads().values()
        return DownloadResponse(data=[convert_download(download) for download in downloads])
    except Exception as e:
        return DownloadResponse(message=f'Failed to retrieve downloads: {e}', success=False)


@download_router.get("/download/{download_id}", response_model=DownloadItem, dependencies=[Depends(get_client_id)])
def get_download(download_id: str):
    from madokami import get_app
    app = get_app()
    try:
        download = app.downloader.get_download_by_id(download_id)
        if download is None:
            return InfoMessage(message=f'Download {download_id} not found', success=False)
        data = convert_download(download)
        return DownloadItem(data=data)
    except Exception as e:
        return DownloadItem(message=f'Failed to retrieve download: {e}', success=False)


@download_router.get("/download/pause/{download_id}", response_model=DownloadItem, dependencies=[Depends(get_client_id)])
def pause_download(download_id: str):
    from madokami import get_app
    app = get_app()
    try:
        download = app.downloader.get_download_by_id(download_id)
        if download is None:
            return DownloadItem(message=f'Download {download_id} not found', success=False)
        download.pause(True)
        return DownloadItem(data=convert_download(download))
    except Exception as e:
        return DownloadItem(message=f'Failed to pause download: {e}', success=False)


@download_router.get("/download/resume/{download_id}", response_model=DownloadItem, dependencies=[Depends(get_client_id)])
def resume_download(download_id: str):
    from madokami import get_app
    app = get_app()
    try:
        download = app.downloader.get_download_by_id(download_id)
        if download is None:
            return DownloadItem(message=f'Download {download_id} not found', success=False)
        download.resume()
        return DownloadItem(data=convert_download(download))
    except Exception as e:
        return DownloadItem(message=f'Failed to resume download: {e}', success=False)


@download_router.get("/download/remove/{download_id}", response_model=DownloadItem, dependencies=[Depends(get_client_id)])
def remove_download(download_id: str):
    from madokami import get_app
    app = get_app()
    try:
        download = app.downloader.get_download_by_id(download_id)
        if download is None:
            return DownloadItem(message=f'Download {download_id} not found', success=False)
        download.remove(True)
        return DownloadItem(data=convert_download(download))
    except Exception as e:
        return DownloadItem(message=f'Failed to remove download: {e}', success=False)


@download_router.post("/download/clear", response_model=InfoMessage, dependencies=[Depends(get_client_id)])
def _clear_downloads():
    from madokami import get_app
    app = get_app()
    try:
        app.downloader.remove_all()
        return InfoMessage(message="Downloads cleared successfully")
    except Exception as e:
        return InfoMessage(message=f'Failed to clear downloads: {e}', success=False)