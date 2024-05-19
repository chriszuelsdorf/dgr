import os
import shutil
import pathlib
from dataclasses import dataclass

from ..yaml import load_yaml

@dataclass
class Conf_dirs:
    base: str = "/usr/local/share/dgr-49d7b9af5e2d"

@dataclass
class Conf_validation:
    check_plugins_tasks: bool = True

@dataclass
class Conf_db:
    conn_host: str = "localhost"
    conn_port: int = 5432
    conn_user: str = "chris"
    conn_password: str = "1234"
    conn_dbname: str = "dev"

@dataclass
class Conf_manager:
    default_backrun: bool = False

@dataclass
class Conf_plugins:
    tasks: dict[str, dict] = {}

@dataclass
class Config:
    dirs: Conf_dirs = Conf_dirs()
    validation: Conf_validation = Conf_validation()
    db: Conf_db = Conf_db()
    manager: Conf_manager = Conf_manager()
    plugins: Conf_plugins = Conf_plugins()

def load_config(path:str="/etc/dgr-49d7b9af5e2d.yaml") -> Config:
    if not os.path.exists(path):
        src = pathlib.Path(__file__).parent.parent / "blob/dgr-49d7b9af5e2d.yaml"
        shutil.copyfile(src, path)

    contents = load_yaml(path)

    return Config(
        dirs = Conf_dirs(**contents.get("dirs", {})),
        validation = Conf_validation(**contents.get("validation", {})),
        db = Conf_db(**contents.get("db", {})),
        manager = Conf_manager(**contents.get("manager", {})),
        plugins = Conf_plugins(**contents.get("plugins", {}))
    )
