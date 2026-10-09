from functools import wraps


def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@count_calls
def square(n):
    return n * n


for n in range(5):
    square(n)
print(square.calls)
print(square.__name__, square(9))
