from dataclasses import dataclass
import datetime

from ...cron import Cron
from .task import Task
from ...types import DotDict
from .state import State

Q_LATEST_DAGRUN = "SELECT max(\"scheduled\") FROM dagruns WHERE \"name\" = ?;"


@dataclass
class Dag:
    name: str
    sch: Cron
    backrun: bool
    tasks: DotDict[str, Task]

    def eligible_for_run(self, state: State) -> bool:
        # Find time of last run
        res = state.db.querymany(Q_LATEST_DAGRUN, [self.name])

        # There is a known last run and the last cron ts is later than the last
        #   known run
        if len(res) == 1 and self.sch.prev() > res[0][0]:
            return True
        # There is no last known run but backrun is set to True
        elif len(res) == 0 and self.backrun is True:
            return True
        return False
    
    def create_dagrun(self, state: State):
        now_ts = datetime.datetime.now(datetime.timezone.utc)
        # init dagrun
        stmt = (
            "INSERT INTO dagruns "
            '("name", "status", "scheduled", "last_updated") '
            "VALUES (%s, %s, %s, %s) "
            'RETURNING "id";'
        )
        r = state.db.executefetch(stmt, [self.name, "created", self.sch.prev(), now_ts])
        dagrun_id = r[0][0]
        # init tasks
        taskids = {}
        taskdeps = {}
        for taskname, taskspec in self.tasks.items():
            taskids[taskname] = taskspec.create_task(state, dagrun_id, now_ts)
            taskdeps[taskname] = taskspec.dep
        # init taskdeps
        stmt = (
            'INSERT INTO taskdeps ('
            '"dagrun_id", "task_id", "dep_task_id", "last_managed", "last_updated"'
            ') VALUES (%s, %s, %s, %s, %s);'
        )
        for taskname, deplist in taskdeps.items():
            for dep in deplist:
                state.db.execute(stmt, [dagrun_id, taskids[taskname], taskids[dep], now_ts, now_ts])
