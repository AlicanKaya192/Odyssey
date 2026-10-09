import time


def measure(func, repeat):
    # time every call with perf_counter, return the shortest
    return 0.0

calls = []
print(measure(lambda: calls.append(1), 4) >= 0)
print(len(calls))
print(measure(lambda: time.sleep(0.05), 3) >= 0.05)
delays = [0.06, 0.02, 0.04]
print(measure(lambda: time.sleep(delays.pop(0)), 3) < 0.04)
