from pydantic import BaseModel
from typing import List, Union, Callable, Optional, Any
from madokami.plugin.subscription import SubscriptionManager


class Setting(BaseModel):
    key: str
    name: str
    description: str
    default: Optional[str] = None


class PluginMetaData(BaseModel):
    name: str
    namespace: str
    description: str
    version: str = '0.0.1'
    author: str = ''
    license: str = 'MIT'
    settings: list[Setting] = []
    engines: list[str] = []
    subscription_manager: Any  # SubscriptionManager


class BangumiSearchResult(BaseModel):
    class Data(BaseModel):
        class Tag(BaseModel):
            name: str
            count: int

        date: str
        image: str
        type: int
        summary: str
        name: str
        name_cn: str
        tags: List[Tag]
        score: float
        id: int
        rank: int

    data: list[Data]


class BangumiSearchPostBody(BaseModel):
    class Filter(BaseModel):
        type: list[int] = [2]
    keyword: str
    filter: Filter = Filter()


class EpisodeInfo(BaseModel):
    class Datum(BaseModel):
        airdate: str
        name: str
        name_cn: str
        duration: str
        desc: str
        ep: int
        sort: int
        id: int
        subject_id: int
        comment: int
        type: int
        disc: int
        duration_seconds: int

    data: List[Datum]
    total: int
    limit: int
    offset: int


class BangumiSubject(BaseModel):
    class Images(BaseModel):
        small: str
        grid: str
        large: str
        medium: str
        common: str

    class Rating(BaseModel):

        rank: int
        total: int
        score: float

    class Tag(BaseModel):
        name: str
        count: int

    class Collection(BaseModel):
        on_hold: int
        dropped: int
        wish: int
        collect: int
        doing: int

    class InfoboxItem(BaseModel):
        class ValueItem(BaseModel):
            v: str

        key: str
        value: Union[str, List[ValueItem]]

    date: str
    platform: str
    images: Images
    summary: str
    name: str
    name_cn: str
    tags: List[Tag]
    infobox: List[InfoboxItem]
    rating: Rating
    total_episodes: int
    collection: Collection
    id: int
    eps: int
    volumes: int
    locked: bool
    nsfw: bool
    type: int