**Yapman gereken:** `GET /slow` bir `async def` olsun, `seconds` sorgusu
(ondalıklı, varsayılan `0.1`) kadar `await asyncio.sleep(...)` ile beklesin
ve `{"waited": seconds}` döndürsün.

- `GET /slow` → `{"waited": 0.1}`
- `GET /slow?seconds=0.2` → `{"waited": 0.2}`
