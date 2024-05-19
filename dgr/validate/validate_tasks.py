from ..plugins import load_plugin
from ..config import Config

def validate_task(prefix, task, config: Config) -> list[bool, str|None]:
    if not isinstance(task, dict):
        return False, f"{prefix} was not a dict"
    
    # Deps themselves must be validated by the dag validator
    if not isinstance(task.get("dep", []), list):
        return False, f"{prefix}.dep was not a list"
    
    if "plugin" not in task:
        return False, f"{prefix}.plugin was missing"
    
    if not config.validation.check_plugins_tasks:
        return True, None
    
    # A nothing-burger is possible but pointless.
    # TODO ensure a None plugin is immediately evaluated as success upon all 
    #   upstreams being successful.
    if task['plugin'] is None:
        return True, None
    
    if task['plugin'] not in config.plugins.tasks:
        return False, f"{prefix}.plugin is not configured as a task plugin"
    
    plugin = load_plugin(task['plugin'], config)
    if not hasattr(plugin, "DGR_TASK_TARGET"):
        return False, f"{prefix}.plugin does not have a task target"
    
    result = plugin.DGR_TASK_TARGET.validate({k:v for k,v in task.items() if k not in ['plugin', 'dep']})

    if not result:
        return False, f"{prefix}.plugin validator indicated args are invalid"
    
    return True, None

