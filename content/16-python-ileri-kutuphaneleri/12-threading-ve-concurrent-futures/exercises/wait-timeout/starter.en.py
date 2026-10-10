import time
from concurrent.futures import ThreadPoolExecutor, wait


def nap(seconds):
    time.sleep(seconds)
    return seconds


def finished_within(delays, limit):
    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(nap, d) for d in delays]
        results = [f.result() for f in futures]
    return [len(results), 0]

print(finished_within([0.1, 0.1, 1.5], 0.5))
