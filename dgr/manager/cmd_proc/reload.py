import os

from ...yaml import load_yaml
from ...validate import Validator
from ...types import DotDict
from ..state import State, HotConf, Dag, Task
from ...cron import Cron

I_NOTICE = "INSERT INTO notices VALUES ('loading', %s, %s, now() at time zone 'utc')"
BADYAML = "Loading file %s failed with message: %s"
INTERCONFL = "Interfile conflict detected: kind %s, name: %s"

def reload(state: State) -> str:
    # return "success" or "failure"
    # this job should (a) validate the yaml and (b) load it to state
    pfx = f"{state.config.basepath}/jobs"
    any_failed = False
    hotconf_d = {
        "dags": DotDict()
    }
    # TODO implement walking, i.e. allow subfolders
    for file in os.listdir(pfx):
        if not file.endswith(".yaml"):
            continue

        # Load, validate, and issue notices
        contents = load_yaml(f"{pfx}/{file}")
        result, msg = Validator.validate(contents, config=state.config)
        if result is False:
            state.db.execute(I_NOTICE, [file, BADYAML.format(file, msg)])
            any_failed = True
        
        # Check for interfile conflicts and populate hotconf_d
        # kind is top level, "dags", for example
        if "dags" in contents:
            conflicts = set(hotconf_d["dags"]) & set(contents["dags"])
            if len(conflicts) > 0:
                state.db.execute(I_NOTICE, [file, INTERCONFL.format("dags", conflicts)])
                any_failed = True
            if any_failed:
                break
            for dagname, dagspec in contents["dags"]:
                if dagname in hotconf_d['dags']:
                    state.db.execute(I_NOTICE, [file, INTERCONFL.format("dags", dagname)])
                tasks = DotDict()
                for taskname, taskspec in dagspec["tasks"]:
                    tasks[taskname] = Task(
                        name=taskname,
                        plugin=taskspec["plugin"],
                        args=DotDict(taskspec.get("args", {})),
                        dep=taskspec.get("dep", [])
                    )
                hotconf_d["dags"][dagname] = Dag(
                    name=dagname,
                    sch=Cron(dagspec['sch']),
                    backrun=dagspec['backrun'],
                    tasks=tasks
                )
    if any_failed:
        return "failure"
    state.hotconf = HotConf(**hotconf_d)
    state.cache = {}
    return "success"
