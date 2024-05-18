from pydantic import BaseModel
import datetime
from typing import Callable, Union


class SearchItem(BaseModel):
    title: str
    cover: str
    bangumi_id: int
    bangumi_name: str
    subtitle_group_id: int
    subtitle_group_name: str
    group_type: str
    tags: list[str] = []
    link: str
    last_updated: datetime.datetime
    # callback: Union[Callable[['SearchItem', str], None], None]
    is_checked: bool = False
