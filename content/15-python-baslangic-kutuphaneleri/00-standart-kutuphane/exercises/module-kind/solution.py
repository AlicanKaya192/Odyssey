import importlib.util
import sys


def module_kind(name):
    if name in sys.builtin_module_names:
        return "built-in"
    if name in sys.stdlib_module_names:
        return "standard"
    if importlib.util.find_spec(name) is not None:
        return "third-party"
    return "missing"

for name in ("math", "json", "numpy", "no_such_module_x"):
    print(name, module_kind(name))
