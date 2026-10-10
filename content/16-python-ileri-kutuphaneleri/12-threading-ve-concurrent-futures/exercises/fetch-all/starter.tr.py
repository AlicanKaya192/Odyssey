import time
from concurrent.futures import ThreadPoolExecutor


def fake_fetch(url):
    time.sleep(0.3)
    return len(url)


def fetch_all(urls):
    return [fake_fetch(url) for url in urls]

urls = [f"https://example.test/{i}" for i in range(10)]
start = time.perf_counter()
print(fetch_all(urls))
print(time.perf_counter() - start < 1.5)
