import logging
import sys


def get_logger(name):
    return logging.Logger(name)

a = get_logger("db")
b = get_logger("db")
print(a.name, a is b, a.getEffectiveLevel())
