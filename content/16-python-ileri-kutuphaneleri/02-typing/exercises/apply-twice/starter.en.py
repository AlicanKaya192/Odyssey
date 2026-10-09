from collections.abc import Callable


def apply_twice(func, value):
    return func(value)


def double(v: int) -> int:
    return v * 2


print(apply_twice(double, 3))
print(apply_twice(lambda v: v + 10, 1))
