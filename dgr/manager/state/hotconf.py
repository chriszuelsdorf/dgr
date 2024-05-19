from dataclasses import dataclass

from .dag import Dag
from ...types import DotDict

@dataclass
class HotConf:
    dags: DotDict[str, Dag]
