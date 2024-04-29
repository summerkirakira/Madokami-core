from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from pydantic import BaseModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    is_superuser: bool = True
    password: str = Field()


class PluginConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(unique=True)
    value: str = Field()


class Plugin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    namespace: str = Field(unique=True)
    name: str = Field()
    description: str = Field()
    is_internal: bool = Field(default=False)
    is_local_plugin: bool = Field(default=False)
    is_active: bool = Field()


class Oauth2Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: str = Field(unique=True)
    client_secret: str = Field()
    expires_at: int = Field()


class EngineSchedulerConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    namespace: str = Field(unique=True)
    plugin_name: str = Field()
    cron_str: Optional[str] = Field()


class PluginInfo(BaseModel):
    name: str
    namespace: str
    description: str
    is_local_plugin: bool = False
    is_internal: bool = False


class DownloadHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time: int = Field()
    link: str = Field()
    success: bool = Field()
    message: str = Field()


class Content(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field()
    link: str = Field()
    episode: int = Field()
    path: str = Field()
    add_time: int = Field()
    media_id: str | None = Field(default=None, foreign_key="media.id")
    media: Optional['Media'] = Relationship(back_populates="contents")


class Media(SQLModel, table=True):
    id: str = Field(primary_key=True)
    link: str = Field()
    type: str = Field()
    title: str = Field()
    bangumi_id: Optional[int] = Field()
    season: int = Field()
    contents: list[Content] = Relationship(back_populates="media")

