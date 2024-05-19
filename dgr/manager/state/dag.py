from dataclasses import dataclass

from ...cron import Cron
from .task import Task
from ...types import DotDict

@dataclass
class Dag:
    name: str
    sch: Cron
    backrun: bool
    tasks: DotDict[str, Task]
