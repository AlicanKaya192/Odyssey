import linecache
import tracemalloc

kept = []


def top_growth(func):
    tracemalloc.start()
    first = tracemalloc.take_snapshot()
    func()
    second = tracemalloc.take_snapshot()
    tracemalloc.stop()
    frame = second.compare_to(first, "lineno")[0].traceback[0]
    return linecache.getline(frame.filename, frame.lineno).strip()


def leaky():
    for _ in range(3_000):
        kept.append(bytearray(1_000))


print(top_growth(leaky))
