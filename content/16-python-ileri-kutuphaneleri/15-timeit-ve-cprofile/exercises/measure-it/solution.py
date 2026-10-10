import timeit


def measure(func, number):
    return min(timeit.repeat(func, number=number, repeat=3))

t = measure(lambda: sum(range(1000)), 100)
print(type(t).__name__, t > 0)
