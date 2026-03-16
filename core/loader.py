import pkgutil
import importlib
from pathlib import Path


def discover_plugins(plugin_dir):

    plugins = []

    for subdir in Path(plugin_dir).iterdir():

        if not subdir.is_dir():
            continue

        for module in pkgutil.iter_modules([str(subdir)]):

            m = importlib.import_module(
                f"plugins.{subdir.name}.{module.name}"
            )

            for attr in dir(m):

                obj = getattr(m, attr)

                try:

                    from core.plugin import InfoPlugin

                    if issubclass(obj, InfoPlugin) and obj != InfoPlugin:
                        plugins.append(obj())

                except:
                    pass

    return plugins
