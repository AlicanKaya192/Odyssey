import asyncio
import time


async def tick(n):
    time.sleep(0.2)
    return n

async def main():
    start = time.perf_counter()
    results = await asyncio.gather(*(tick(n) for n in range(4)))
    print(results, time.perf_counter() - start < 0.5)


asyncio.run(main())
