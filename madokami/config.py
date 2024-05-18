from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress
from typing import Any, Optional, Literal
from pathlib import Path
from .util import load_yaml


class BaseSettings(BaseModel):
    pass


class MadokamiBasicConfig(BaseSettings):
    env_file: str = ".env"
    mode: Literal["product", "dev"] = "product"
    host: IPvAnyAddress = IPvAnyAddress("127.0.0.1")
    port: int = 8000
    debug: bool = False
    sqlite_uri: str = "./data/madokami.db"
    static_files: str = "../frontend/dist"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.load_env_file()
        if not self.sqlite_uri.startswith("sqlite"):
            self.sqlite_uri = f"sqlite:///{self.sqlite_uri}"

    def load_env_file(self) -> None:
        env_file = Path.cwd() / self.env_file
        if env_file.exists():
            env = load_yaml(env_file)
            for key, value in env.items():
                setattr(self, key, value)


class MadokamiConfig(MadokamiBasicConfig):
    username: str
    password: str


basic_config = MadokamiBasicConfig()