import sys


def is_standard(name):
    return name in sys.stdlib_module_names

for name in ("json", "csv", "numpy", "requests"):
    print(name, is_standard(name))
