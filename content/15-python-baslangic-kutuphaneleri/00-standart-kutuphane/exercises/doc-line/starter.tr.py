import importlib


def doc_line(module_name, attr):
    module = importlib.import_module(module_name)
    # getattr, __doc__, ilk satir
    return ""

print(doc_line("math", "gcd"))
print(doc_line("math", "sqrt"))
