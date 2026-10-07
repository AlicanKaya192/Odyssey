import time
from concurrent.futures import ThreadPoolExecutor


def fetch(page):
    time.sleep(0.1)
    return page * 10


with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(fetch, range(1, 9)))

print(results)
print(sum(results))
