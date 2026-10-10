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
    return STEPS[1]

print(slowest_step())
