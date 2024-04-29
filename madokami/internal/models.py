from pydantic import BaseModel


class Setting(BaseModel):
    key: str
    name: str
    description: str


class PluginMetaData(BaseModel):
    name: str
    namespace: str
    description: str
    version: str = '0.0.1'
    author: str = ''
    license: str = 'MIT'
    settings: list[Setting] = []
    engines: list[str] = []