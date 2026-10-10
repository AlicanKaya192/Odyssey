import asyncio
import time


async def fetch(name):
    await asyncio.sleep(0.2)
    return len(name)


async def fetch_all(names):
    return list(await asyncio.gather(*(fetch(name) for name in names)))

def run_fetch_all(names):
    return asyncio.run(fetch_all(names))


start = time.perf_counter()
print(run_fetch_all(["a", "bb", "ccc", "dddd", "e"]))
print(time.perf_counter() - start < 0.5)
