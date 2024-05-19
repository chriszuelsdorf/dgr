from dataclasses import dataclass

from ...db import DB
from ...config import Config
from .hotconf import HotConf

@dataclass
class State:
    db: DB
    config: Config
    hotconf: HotConf
    lastrun: int = 0
    cache: dict = {}
