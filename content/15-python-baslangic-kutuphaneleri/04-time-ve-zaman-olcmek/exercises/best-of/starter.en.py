import time


def measure(func, repeat):
    # time every call with perf_counter, return the shortest
    return 0.0

calls = []
print(measure(lambda: calls.append(1), 4) >= 0)
print(len(calls))
print(measure(lambda: time.sleep(0.05), 3) >= 0.05)
delays = [0.6, 0.05, 0.4]
print(measure(lambda: time.sleep(delays.pop(0)), 3) < 0.3)
