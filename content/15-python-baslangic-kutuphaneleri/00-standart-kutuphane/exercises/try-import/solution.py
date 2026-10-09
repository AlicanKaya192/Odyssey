import importlib


def try_import(name):
    try:
        module = importlib.import_module(name)
    except ImportError:
        return None
    return module.__name__

print(try_import("json"))
print(try_import("no_such_module_x"))
