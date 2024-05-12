from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from .models import MediaResponse, MediasResponse
from madokami.drivers.deps import SessionDep, get_client_id
from madokami.internal.utils import get_cover_image
from madokami.crud import get_all_media_info, get_media_info_by_id
from madokami.models import Media as MediaInfo

media_router = APIRouter(tags=["Media"])


def convert_media(media_info: MediaInfo) -> MediaResponse.Media:
    return MediaResponse.Media(
        id=media_info.id,
        link=media_info.link,
        title=media_info.title,
        bangumi_id=media_info.bangumi_id,
        season=media_info.season,
        contents=[MediaResponse.Media.Content(
            title=content.title,
            episode=content.episode,
            link=content.link,
            path=content.path,
            add_time=content.add_time
        ) for content in media_info.contents]
    )


@media_router.get("/media/cover/{media_id}")
def _get_cover_image(media_id: str, session: SessionDep):
    cover_image_path = get_cover_image(session, media_id)
    if cover_image_path is None:
        raise HTTPException(status_code=404, detail="Cover image not found")
    return FileResponse(cover_image_path, media_type='image/jpeg')


@media_router.get("/media/all", response_model=MediasResponse, dependencies=[Depends(get_client_id)])
def _get_all_media(session: SessionDep):
    try:
        medias = get_all_media_info(session)
        return MediasResponse(data=[convert_media(media_info) for media_info in medias])
    except Exception as e:
        MediaResponse(message=f'Failed to retrieve media: {e}', success=False)


@media_router.get("/media/{media_id}", response_model=MediaResponse, dependencies=[Depends(get_client_id)])
def _get_media(media_id: str, session: SessionDep):
    try:
        media = get_media_info_by_id(session, media_id)
        if media is None:
            return MediaResponse(message=f'Media {media_id} not found', success=False)
        return MediaResponse(data=convert_media(media))
    except Exception as e:
        return MediaResponse(message=f'Failed to retrieve media: {e}', success=False)