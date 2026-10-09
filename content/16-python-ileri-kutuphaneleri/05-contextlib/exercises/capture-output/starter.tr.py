import io
from contextlib import redirect_stdout


def capture(func, *args):
    func(*args)
    return ""


def greet(name):
    print(f"hello {name}")
    print("bye")


print(repr(capture(greet, "ada")))
