import os
import shutil
import pathlib

from ..yaml import load_yaml
from ..types import convert_to_dotdict

class Config:
    def __init__(self, path="/etc/dgr-49d7b9af5e2d.yaml") -> None:
        if not os.path.exists(path):
            src = pathlib.Path(__file__).parent.parent / "blob/dgr-49d7b9af5e2d.yaml"
            shutil.copyfile(src, path)
        self._conf = convert_to_dotdict(load_yaml(path))
    def __getattr__(self, name: str) -> os.Any:
        return self._conf[name]
