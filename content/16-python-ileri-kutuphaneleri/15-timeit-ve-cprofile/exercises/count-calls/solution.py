import cProfile
import pstats


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def count_calls(n):
    profiler = cProfile.Profile()
    profiler.runcall(fib, n)
    for (_, _, name), (cc, nc, *_rest) in pstats.Stats(profiler).stats.items():
        if name == "fib":
            return nc
    return 0

print(count_calls(10), count_calls(15))
