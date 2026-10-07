`books` ve `movies` listeleri hazır.

**Yapman gerekenler:**

1. `paging` bağımlılığı: `limit` (1–5, varsayılan `2`), `offset` (0 ya da
   büyük, varsayılan `0`); `{"limit": ..., "offset": ...}` döndürsün.
2. `GET /books` ve `GET /movies` ikisi de `paging`'i kullanıp listeden dilim
   döndürsün. Kurallar **yalnızca** `paging`'de yazılı olsun.

- `GET /books` → `["Dune", "Emma"]`
- `GET /books?limit=2&offset=3` → `["Kindred", "Beloved"]`
- `GET /movies?offset=1` → `["Heat", "Up"]`
- `GET /movies?limit=9` → `422`
