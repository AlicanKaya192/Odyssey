import io
from contextlib import redirect_stdout


def capture(func, *args):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args)
    return buffer.getvalue()


def greet(name):
    print(f"hello {name}")
    print("bye")


print(repr(capture(greet, "ada")))
