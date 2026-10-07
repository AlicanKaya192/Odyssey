**What to do:** make `GET /slow` an `async def` that waits for `seconds`
(a float query, default `0.1`) with `await asyncio.sleep(...)` and returns
`{"waited": seconds}`.

- `GET /slow` → `{"waited": 0.1}`
- `GET /slow?seconds=0.2` → `{"waited": 0.2}`
