from .backend.engine import Engine


_registered_engines: list[Engine] = []


def register_engine(engine: Engine):
    _registered_engines.append(engine)


def get_registered_engines() -> list[Engine]:
    return _registered_engines

