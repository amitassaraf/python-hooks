# mypy: ignore-errors

import importlib
import pkgutil

discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg in pkgutil.iter_modules()
    if name.startswith("hooks_")
}

for module in discovered_plugins.values():
    globals().update(
        {n: getattr(module, n) for n in module.__all__}
        if hasattr(module, "__all__")
        else {k: v for (k, v) in module.__dict__.items() if not k.startswith("_")}
    )
