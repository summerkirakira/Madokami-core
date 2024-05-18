from pydantic import BaseModel
from typing import Optional
from madokami.models import Media as MediaInfo


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    is_superuser: bool


class InfoMessage(BaseModel):
    message: str = "Success"
    success: bool = True
    title: str = "Info"
    data: str = ""


class DownloadData(BaseModel):
    id: str
    is_metadata: bool
    name: str
    target_path: str
    dir: str
    total_length: int
    progress: float
    current_download: int
    status: str
    current_speed: int


class DownloadItem(InfoMessage):
    data: Optional[DownloadData] = None


class DownloadResponse(InfoMessage):
    data: Optional[list[DownloadData]] = None


class MediaResponse(InfoMessage):

    class Media(BaseModel):
        class Content(BaseModel):
            title: str
            episode: int
            link: str
            path: str
            add_time: int

        contents: list[Content]
        id: str
        link: str
        title: str
        bangumi_id: Optional[int]
        season: int

    data: Optional[Media] = None


class MediasResponse(InfoMessage):
    data: Optional[list[MediaResponse.Media]] = None


class SubscriptionsAllResponse(InfoMessage):

    class SubscriptionRecord(BaseModel):

        class Subscription(BaseModel):
            id: str
            name: str
            data: str

        namespace: str
        subscriptions: list[Subscription]

    data: Optional[list[SubscriptionRecord]] = None


class AddSubscriptionBody(BaseModel):
    name: str
    data: str
    namespace: str


class RemoveSubscriptionBody(BaseModel):
    id: str
    namespace: str


class PluginInfoResponse(InfoMessage):

    class PluginInfo(BaseModel):

        class Engine(BaseModel):
            name: str
            description: str
            namespace: str
            cron_str: Optional[str]

        name: str
        namespace: str
        description: str
        is_local_plugin: bool
        is_internal: bool
        engines: list[Engine]

    data: list[PluginInfo] = []


class SettingsAllResponse(InfoMessage):

    class SettingRecord(BaseModel):

        class Setting(BaseModel):
            key: str
            name: str
            description: str
            value: Optional[str]

        namespace: str
        settings: list[Setting]

    data: Optional[list[SettingRecord]] = None


class UpdateSettingBody(BaseModel):
    key: str
    value: Optional[str]


class LogResponse(InfoMessage):
    data: Optional[list[str]] = None


class AllScheduledTasksResponse(InfoMessage):

    class Plugin(BaseModel):
        class ScheduledTask(BaseModel):
            id: int
            namespace: str
            name: str
            description: str
            cron_str: Optional[str]

        namespace: str
        tasks: list[ScheduledTask]

    data: list[Plugin] = []


class UpdateCronBody(BaseModel):
    schedule_id: int
    cron_str: Optional[str]
