import importlib


def count_public(module_name):
    module = importlib.import_module(module_name)
    return len([n for n in dir(module) if not n.startswith("_")])

print(count_public("math"))
print(count_public("statistics") > 10)
