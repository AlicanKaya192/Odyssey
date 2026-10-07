Raporlar arka planda hazırlanıyor; `reports` sözlüğü her raporun durumunu
tutuyor.

**Yapman gereken:** `GET /reports/{report_id}`:

- Rapor yok → `404`, `detail` `{"code": "not_found"}`
- Hazır değil (`"pending"`) → `503`, `detail` `{"code": "not_ready"}` ve
  `Retry-After: 30` başlığı (istemciye "30 saniye sonra dene" diyor)
- Hazır → `{"id": ..., "status": "ready"}`

API 1'de istemci olarak `Retry-After`'ı okumuştun; şimdi gönderiyorsun.
