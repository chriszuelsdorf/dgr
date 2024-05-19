from dataclasses import dataclass
import typing
import datetime

from ...types import DotDict
from .state import State

@dataclass
class Task:
    name: str
    plugin: str|None
    args: DotDict[str, typing.Any]
    dep: list[str]

    def create_task(self, state: State, dagrun_id: int, now_ts: datetime.datetime):
        stmt = (
            'INSERT INTO tasks ('
            '"dagrun_id", "name", "plugin", "pluginargs", '
            '"status", "attempts", "last_updated"'
            ')'
            'VALUES (%s, %s, %s, %s, %s, %s, %s);'
        )
        vals = [
            dagrun_id, self.name, self.plugin, str(self.args), "created", 0, now_ts
        ]
        r = state.db.executefetch(stmt, vals)
        return r[0][0]
