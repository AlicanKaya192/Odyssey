İki uç nokta da yazılmış ama biri hiç çalışmıyor:

- `GET /books/latest` → `422` (beklenen: en yeni kitap)

**Yapman gereken:** sebebi bul ve düzelt. Doğru hâl:

- `GET /books/latest` → `{"id": 1, "title": "Dune", "year": 1965}`
- `GET /books/3` → `{"id": 3, "title": "Ulysses", "year": 1922}`
