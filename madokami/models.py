from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


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
    is_active: bool = Field()
