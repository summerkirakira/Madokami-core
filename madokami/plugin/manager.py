from ..crud import get_plugins
from ..db import engine
from ..models import Plugin
from sqlmodel import Session


def load_plugin_names_from_db() -> list[Plugin]:
    with Session(engine) as session:
        plugins = get_plugins(session=session)
        return plugins


class PluginManager:
    def __init__(self):
        self.plugins: list[Plugin] = load_plugin_names_from_db()

