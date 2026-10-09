import sys


def is_standard(name):
    # is it in sys.stdlib_module_names?
    return False

for name in ("json", "csv", "numpy", "requests"):
    print(name, is_standard(name))
