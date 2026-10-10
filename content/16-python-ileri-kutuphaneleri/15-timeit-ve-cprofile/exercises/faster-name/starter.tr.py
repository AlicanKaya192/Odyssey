import time
import timeit


def faster(f, g):
    return f.__name__


def nap():
    time.sleep(0.02)


def quick():
    pass


print(faster(nap, quick), faster(quick, nap))
