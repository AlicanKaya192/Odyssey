Uç noktalar hazır.

**Yapman gereken:** bütün doğrulama hatalarını tek bir biçime çeviren
yakalayıcı:

```json
{"error": "invalid_input",
 "fields": ["title", "year"]}
```

`fields`: her hatanın `loc`'u, ilk öğesi (`body`, `query`) atılıp noktayla
birleştirilmiş hâli.

- `POST /books` `{"title": "", "year": "x"}` → `422`, `fields` `["title", "year"]`
- `GET /books?limit=abc` → `422`, `fields` `["limit"]`
- `POST /books` `{"title": "Dune", "year": 1965}` → `201`
