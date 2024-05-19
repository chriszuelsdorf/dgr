import sys
import importlib.util

from ..config import Config

def load_plugin(name, config: Config):
    fn = config.dirs.base + f"/plugins/{name}.py"
    spec = importlib.util.spec_from_file_location(name, fn)
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"dgr__plugin__{name}"] = module
    spec.loader.exec_module(module)
    return module
