import importlib


def count_public(module_name):
    module = importlib.import_module(module_name)
    # dir(module) icinden "_" ile baslamayanlar
    return 0

print(count_public("math"))
print(count_public("statistics") > 10)
