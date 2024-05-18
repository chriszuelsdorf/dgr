import os
import shutil
import pathlib

from ..yaml import load_yaml

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def convert_to_dotdict(o):
    if type(o) == dict:
        return dotdict({k:convert_to_dotdict(v) for k, v in o.items()})
    elif type(o) == list:
        return [convert_to_dotdict(x) for x in o]
    return o

class Config:
    def __init__(self, path="/etc/dgr-49d7b9af5e2d.yaml") -> None:
        if not os.path.exists(path):
            src = pathlib.Path(__file__).parent.parent / "blob/dgr-49d7b9af5e2d.yaml"
            shutil.copyfile(src, path)
        self._conf = convert_to_dotdict(load_yaml(path))
    def __getattr__(self, name: str) -> os.Any:
        return self._conf[name]
