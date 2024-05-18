# Plugins

The plugin location is `/plugins` under the base directory given as `dirs.base` in the config file. The default location is `/usr/local/share/dgr-49d7b9af5e2d/plugins`.

Each plugin (for example, `myplugin`) must have a `myplugin.py` in that directory.
- To provide a task plugin, that file must contain `DGR_TASK_TARGET`, which must be a subclass of `dgr.plugins.TaskPlugin`.

Each plugin may if needed also use a `/myplugin` subdirectory.

The following assumptions are made with regards to plugins:
1. The `dgr` package is installed
2. Any dependencies of plugins must be installed when installing the plugin.
3. Task parameters are unavailable as `create` kwargs.

To install a plugin:
1. Install any dependencies required (for example, from a Python requirements.txt file associated with the plugin)
2. Put the plugin Python file (and its associated directory, if required) into 
