import importlib


def doc_line(module_name, attr):
    module = importlib.import_module(module_name)
    func = getattr(module, attr)
    return func.__doc__.strip().splitlines()[0].strip()

print(doc_line("math", "gcd"))
print(doc_line("math", "sqrt"))
