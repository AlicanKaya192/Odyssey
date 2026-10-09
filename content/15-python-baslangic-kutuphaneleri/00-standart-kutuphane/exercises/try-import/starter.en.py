import importlib


def try_import(name):
    # try / except ImportError
    return None

print(try_import("json"))
print(try_import("no_such_module_x"))
