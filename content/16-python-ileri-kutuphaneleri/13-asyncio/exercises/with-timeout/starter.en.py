import asyncio


async def slow(delay):
    await asyncio.sleep(delay)
    return "ok"


async def fetch_or_default(delay, limit):
    return await slow(delay)

def check(delay, limit):
    return asyncio.run(fetch_or_default(delay, limit))


print(check(0.05, 0.5), check(1.0, 0.1))
