import time
from contextlib import contextmanager


@contextmanager
def timed(results, label):
    start = time.perf_counter()
    yield
    results[label] = time.perf_counter() - start

results = {}
with timed(results, "ok"):
    sum(range(1000))
try:
    with timed(results, "failed"):
        raise RuntimeError("boom")
except RuntimeError:
    pass
print(sorted(results))
