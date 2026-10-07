İki arama uç noktası çalışıyor ama ikisi de sorguyu f-string ile kuruyor:
SQL enjeksiyonuna açık.

**Yapman gereken:** ikisini de parametreli sorguya (`?`) çevir. Sonuçlar
normal aramada aynı kalmalı, saldırı metni ise hiçbir şey bulmamalı.

- `GET /search?text=call mom` → `[{"id": 2, "text": "call mom"}]`
- `GET /search?text=x' OR '1'='1` → `[]`
- `GET /find?word=ea` → `read Dune`
- `GET /find?word=x' OR 1=1 --` → `[]`
