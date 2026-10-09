from functools import wraps


def count_calls(func):
    # wrapper yaz, wrapper.calls = 0
    return func


@count_calls
def square(n):
    return n * n


for n in range(5):
    square(n)
print(square.calls)
print(square.__name__, square(9))
