from ..cron import Cron

from .validate_tasks import validate_task


def validate_dags(d: dict, config) -> list[bool, str|None]:
    if not isinstance(d, dict):
        return False, "dags was not a dict"
    for dagname, dag in d.items():
        res, msg = validate_dag(f"dags.{dagname}", dag, config)
        if res is False:
            return False, msg
    return True, None


def validate_dag(prefix: str, dag: dict, config) -> list[bool, str|None]:
    if not isinstance(dag, dict):
        return False, f"{prefix} was not a dict"
    
    # All dags must have a valid schedule
    if "sch" not in dag:
        return False, f"{prefix}.sch did not exist"
    try:
        c = Cron(dag['sch'])
    except Exception as e:
        return False, f"{prefix}.sch failed to parse (make sure it's valid)"
    
    # All dags must have at least one task
    if "tasks" not in dag:
        return False, f"{prefix}.tasks did not exist"
    if not isinstance(dag['tasks'], dict) or len(dag["tasks"]) == 0:
        return False, f"{prefix}.tasks was invalid (must be map with at least one entry)"
    deps = {}
    for taskname, task in dag['tasks'].items():
        result, msg = validate_task(f"{prefix}.tasks.{taskname}", task, config)
        if result is False:
            return result, msg
        deps[taskname] = task.get("dep", [])
    
    # Validate dependencies
    # (1) they must exist (i.e. dep tasks must be real)
    # (2) they cannot create circular dependencies
    has_downstream = set()
    for taskname, depl in deps.items():
        for dep in depl:
            if dep not in deps:
                return False, f"{prefix}.tasks.{taskname}.dep lists {dep} which is not a task in this DAG"
        has_downstream |= set(depl)
    
    # Verify acyclicity
    for taskname in deps:
        if not has_noncyclical_ancestry(taskname, deps):
            return False, f"{prefix}.tasks.{taskname} has cyclical ancestry"

    return True, None


def has_noncyclical_ancestry(node, deps:dict[str, list[str]], chain=[]):
    """Verify for a given node that the DAG is actually acyclic"""
    for dep in deps[node]:
        if dep == node:
            return False
        if dep in chain:
            return False
        r = has_noncyclical_ancestry(dep, deps, chain + [dep])
        if not r:
            return False
    return True

