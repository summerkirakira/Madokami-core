from madokami.drivers.madokami import MadokamiApp
from typing import Optional


_app: Optional[MadokamiApp] = None


def get_app():
    global _app
    if _app is None:
        _app = MadokamiApp()
    return _app

