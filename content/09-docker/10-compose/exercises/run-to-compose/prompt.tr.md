Şu uzun komutu compose.yaml'a çevir:

```text
docker run -d -p 8091:8000 -e APP_ENV=production -e DB_PATH=/data/app.db `
  -v appdata:/data --restart unless-stopped app
```

**Yapman gerekenler:** `web` adında bir servis; imaj bu klasördeki
Dockerfile'dan. Port, iki ortam değişkeni, volume ve yeniden başlatma kuralı
komuttakiyle aynı olsun. Adlı volume'u dosyanın en altında da tanımla.

Odyssey servisi ayağa kaldırıp ona istek atacak; yanıt
`{"env": "production", "db": "/data/app.db"}` olmalı.
