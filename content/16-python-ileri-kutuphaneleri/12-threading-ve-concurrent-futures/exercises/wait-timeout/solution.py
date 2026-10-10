import time
from concurrent.futures import ThreadPoolExecutor, wait


def nap(seconds):
    time.sleep(seconds)
    return seconds


def finished_within(delays, limit):
    with ThreadPoolExecutor() as pool:
        futures = [pool.submit(nap, d) for d in delays]
        done, not_done = wait(futures, timeout=limit)
        return [len(done), len(not_done)]

print(finished_within([0.1, 0.1, 1.5], 0.5))
