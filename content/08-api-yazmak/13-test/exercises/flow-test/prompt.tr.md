**Yapman gereken:** kitabın bütün ömrünü deneyen **tek** bir test:

1. `POST /books` → `201`; cevaptaki `id`'yi al.
2. `GET /books/{id}` → `200`, `{"title": ..., "year": ...}`.
3. `DELETE /books/{id}` → `204`.
4. `GET /books/{id}` → `404`.

Bozuk sürümlerde silme hiçbir şey silmiyor, okuma boş gövde dönüyor ya da
cevaptaki numara yanlış olacak.
