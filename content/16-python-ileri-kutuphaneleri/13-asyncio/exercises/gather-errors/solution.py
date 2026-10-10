import asyncio


async def check(x):
    await asyncio.sleep(0.01)
    if x < 0:
        raise ValueError(x)
    return x * 10


async def safe_all(values):
    results = await asyncio.gather(*(check(v) for v in values), return_exceptions=True)
    return ["error" if isinstance(r, Exception) else r for r in results]

def run_safe(values):
    return asyncio.run(safe_all(values))


print(run_safe([1, -2, 3]))
