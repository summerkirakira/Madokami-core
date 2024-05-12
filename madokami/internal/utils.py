from madokami import get_config
from madokami.internal.default_plugins.bangumi_requester import BangumiRequester
from madokami.models import Media as MediaInfo
from madokami.crud import get_media_info_by_id
from madokami.db import Session
from typing import Optional
from pathlib import Path


def get_validated_path(path: str) -> Path:
    path = Path(path)
    if not path.is_absolute():
        path = Path.cwd() / path
    if not path.exists():
        path.mkdir(parents=True)
    return path


def get_cover_image(session: Session, mikan_id: str) -> Optional[Path]:
    cache_path = get_config('madokami.config.cache_path', './data/cache')
    cache_path = get_validated_path(cache_path)
    cover_cache_path = cache_path / 'cover'
    if not cover_cache_path.exists():
        cover_cache_path.mkdir(parents=True)
    media_info = get_media_info_by_id(session, mikan_id)
    if media_info is None:
        return None
    cover_path = cover_cache_path / f'{mikan_id}.jpg'
    if cover_path.exists():
        return cover_path
    bangumi_requester = BangumiRequester()
    if media_info.bangumi_id is None:
        return None
    cover_image = bangumi_requester.get_subject_image(media_info.bangumi_id)
    cover_path.write_bytes(cover_image)

    return cover_path