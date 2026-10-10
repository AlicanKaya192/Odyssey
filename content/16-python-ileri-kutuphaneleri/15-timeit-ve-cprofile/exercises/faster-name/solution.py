import time
import timeit


def best(func):
    return min(timeit.repeat(func, number=3, repeat=3))


def faster(f, g):
    return f.__name__ if best(f) < best(g) else g.__name__


def nap():
    time.sleep(0.02)


def quick():
    pass


print(faster(nap, quick), faster(quick, nap))
