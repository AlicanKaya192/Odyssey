import cProfile
import pstats
import time


def read():
    time.sleep(0.15)


def clean():
    time.sleep(0.05)


def save():
    time.sleep(0.1)


def pipeline():
    read()
    clean()
    save()


STEPS = ["read", "clean", "save"]


def slowest_step():
    profiler = cProfile.Profile()
    profiler.runcall(pipeline)
    times = {}
    for (_, _, name), values in pstats.Stats(profiler).stats.items():
        if name in STEPS:
            times[name] = values[3]
    return max(times, key=times.get)

print(slowest_step())
