import asyncio


async def check(x):
    await asyncio.sleep(0.01)
    if x < 0:
        raise ValueError(x)
    return x * 10


async def safe_all(values):
    return list(await asyncio.gather(*(check(v) for v in values)))

def run_safe(values):
    return asyncio.run(safe_all(values))


print(run_safe([1, -2, 3]))
