import timeit


def measure(func, number):
    return 0

t = measure(lambda: sum(range(1000)), 100)
print(type(t).__name__, t > 0)
