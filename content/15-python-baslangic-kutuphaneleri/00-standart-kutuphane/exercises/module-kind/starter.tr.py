import importlib.util
import sys


def module_kind(name):
    # Sirayla: built-in, standard, third-party, missing
    return "missing"

for name in ("math", "json", "numpy", "no_such_module_x"):
    print(name, module_kind(name))
