**Yapman gereken:** `GET /books` hem süzsün hem sayfalasın:

- `author` isteğe bağlı (yoksa süzme), `page` varsayılan `1`, `per_page`
  varsayılan `2`.
- Cevap: `{"total": ..., "titles": [...]}`. `total` **süzülmüş** listenin
  uzunluğu; `titles` o sayfadaki kitapların adları.

- `GET /books?author=Austen` → `{"total": 2, "titles": ["Emma", "Persuasion"]}`
- `GET /books?author=Austen&page=2` → `{"total": 2, "titles": []}`
- `GET /books?page=2` → `{"total": 6, "titles": ["Ulysses", "Kindred"]}`
- `GET /books?author=Nobody` → `{"total": 0, "titles": []}`
