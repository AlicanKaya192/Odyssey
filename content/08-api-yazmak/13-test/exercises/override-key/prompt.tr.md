`/admin/stats` gizli bir anahtar istiyor; anahtarı bilmiyorsun.

**Yapman gerekenler:** iki test:

1. Anahtarsız istek `401` dönüyor.
2. `require_key`'i `app.dependency_overrides` ile "her zaman geçer"e çevirip
   `GET /admin/stats` → `200`, `{"books": 3}`. Sonra temizle (`finally`).
