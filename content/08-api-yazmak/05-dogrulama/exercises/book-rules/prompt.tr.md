**Yapman gerekenler:** `Book` modelinin alanlarına kural koy ve
`POST /books` kitabı `201` ile olduğu gibi döndürsün.

| Alan | Kural |
|---|---|
| `title` | 1–80 karakter |
| `year` | 1450–2100 (ikisi de dahil) |
| `pages` | 0'dan büyük |

- `{"title": "Dune", "year": 1965, "pages": 412}` → `201`
- `{"title": "", "year": 1965, "pages": 412}` → `422`
- `{"title": "Dune", "year": 2101, "pages": 412}` → `422`
- `{"title": "Dune", "year": 1450, "pages": 1}` → `201`
- `{"title": "Dune", "year": 1965, "pages": 0}` → `422`
