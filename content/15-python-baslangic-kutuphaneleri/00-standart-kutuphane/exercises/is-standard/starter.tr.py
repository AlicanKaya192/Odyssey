import sys


def is_standard(name):
    # sys.stdlib_module_names icinde mi?
    return False

for name in ("json", "csv", "numpy", "requests"):
    print(name, is_standard(name))
