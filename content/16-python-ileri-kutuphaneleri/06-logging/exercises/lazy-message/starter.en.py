import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def debug_value(log, value):
    log.debug(f"value: {value}")

log = logging.getLogger("demo")
calls = 0


class Expensive:
    def __str__(self):
        global calls
        calls += 1
        return "expensive"


for _ in range(3):
    debug_value(log, Expensive())
print(calls)
