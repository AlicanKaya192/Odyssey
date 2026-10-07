`get_weather` and `get_news` are ready; each waits 0.2 s.

**What to do:** `GET /dashboard/{city}` waits for both **at the same time**
(`asyncio.gather`) and returns `{"weather": ..., "news": ...}`. One after
another takes 0.4 s, together 0.2 s.

- `GET /dashboard/Izmir` → `{"weather": {"city": "Izmir", "temp": 21}, "news": [...two items...]}`
