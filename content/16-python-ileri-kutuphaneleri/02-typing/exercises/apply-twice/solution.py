from collections.abc import Callable


def apply_twice(func: Callable[[int], int], value: int) -> int:
    return func(func(value))


def double(v: int) -> int:
    return v * 2


print(apply_twice(double, 3))
print(apply_twice(lambda v: v + 10, 1))
