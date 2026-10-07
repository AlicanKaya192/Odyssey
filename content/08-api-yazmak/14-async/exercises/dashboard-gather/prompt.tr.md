`get_weather` ve `get_news` hazır; her biri 0,2 sn bekliyor.

**Yapman gereken:** `GET /dashboard/{city}` ikisini **aynı anda** beklesin
(`asyncio.gather`) ve `{"weather": ..., "news": ...}` döndürsün. Sırayla
beklersen 0,4 sn, birlikte 0,2 sn.

- `GET /dashboard/Izmir` → `{"weather": {"city": "Izmir", "temp": 21}, "news": [...iki haber...]}`
