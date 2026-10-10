import time
from concurrent.futures import ThreadPoolExecutor


def fake_fetch(url):
    time.sleep(0.3)
    return len(url)


def fetch_all(urls):
    with ThreadPoolExecutor(max_workers=10) as pool:
        return list(pool.map(fake_fetch, urls))

urls = [f"https://example.test/{i}" for i in range(10)]
start = time.perf_counter()
print(fetch_all(urls))
print(time.perf_counter() - start < 1.5)
