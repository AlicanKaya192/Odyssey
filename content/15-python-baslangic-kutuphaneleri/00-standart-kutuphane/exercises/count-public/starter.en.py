import importlib


def count_public(module_name):
    module = importlib.import_module(module_name)
    # names in dir(module) not starting with "_"
    return 0

print(count_public("math"))
print(count_public("statistics") > 10)
