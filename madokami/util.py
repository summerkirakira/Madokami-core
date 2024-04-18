import yaml
from pathlib import Path


def load_yaml(file: Path) -> dict:
    with open(file, "r") as f:
        return yaml.safe_load(f)


def dump_yaml(file: Path, data: dict) -> None:
    with open(file, "w") as f:
        yaml.dump(data, f)

