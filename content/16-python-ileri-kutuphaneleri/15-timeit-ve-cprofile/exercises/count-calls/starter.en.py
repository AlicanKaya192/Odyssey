import cProfile
import pstats


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def count_calls(n):
    profiler = cProfile.Profile()
    # runcall, pstats.Stats(profiler).stats
    return 0

print(count_calls(10), count_calls(15))
