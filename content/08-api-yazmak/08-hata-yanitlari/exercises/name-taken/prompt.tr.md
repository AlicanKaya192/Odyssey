`names` kümesinde alınmış adlar duruyor (`"ada"`).

**Yapman gereken:** `POST /signup` adı küçük harfe çevirsin.

- Ad alınmışsa `409` ve `detail`'de bir sözlük:
  `{"code": "name_taken", "name": ...}`
- Değilse ekle, `201`, `{"name": ...}`

- `{"name": "Grace"}` → `201`, `{"name": "grace"}`
- `{"name": "ADA"}` → `409`, `{"detail": {"code": "name_taken", "name": "ada"}}`
- `{"name": "grace"}` → `409`
