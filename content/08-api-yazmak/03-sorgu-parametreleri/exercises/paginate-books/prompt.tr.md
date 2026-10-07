**Yapman gereken:** `GET /books` sayfalı cevap versin:

```json
{"page": 1, "per_page": 2, "total": 6,
 "items": [ ...iki kitap... ]}
```

- `page` varsayılan `1`, `per_page` varsayılan `2`.
- Sayfa `p` için dilim `(p - 1) * per_page`'den başlar.
- Sonu aşan sayfa hata değil: `items` boş.

- `GET /books` → Dune, Emma
- `GET /books?page=3` → Persuasion, Beloved
- `GET /books?page=2&per_page=4` → Persuasion, Beloved
- `GET /books?page=9` → `items: []`
