from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress
from typing import Any, Optional
from pathlib import Path
from .util import load_yaml


class BaseSettings(BaseModel):
    pass


class MadokamiBasicConfig(BaseSettings):
    env_file: str = ".env"
    mode = "production"
    host: IPvAnyAddress = IPvAnyAddress("127.0.0.1")
    port: int = 8000
    debug: bool = False
    sqlite_path: str = "./data/madokami.db"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.load_env_file()
        if not self.sqlite_path.startswith("sqlite"):
            self.sqlite_path = f"sqlite:///{self.sqlite_path}"

    def load_env_file(self) -> None:
        env_file = Path.cwd() / self.env_file
        if env_file.exists():
            env = load_yaml(env_file)
            for key, value in env.items():
                setattr(self, key, value)


class MadokamiConfig(MadokamiBasicConfig):
    username: str
    password: str
