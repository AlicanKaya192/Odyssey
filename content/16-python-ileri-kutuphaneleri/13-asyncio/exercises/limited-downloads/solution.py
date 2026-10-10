import asyncio


async def download(n, gate, state):
    async with gate:
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        await asyncio.sleep(0.02)
        state["active"] -= 1
        return n


async def download_all(count, limit):
    gate = asyncio.Semaphore(limit)
    state = {"active": 0, "peak": 0}
    results = await asyncio.gather(*(download(n, gate, state) for n in range(count)))
    return [len(results), state["peak"]]

def run_downloads(count, limit):
    return asyncio.run(download_all(count, limit))


print(run_downloads(10, 3))
