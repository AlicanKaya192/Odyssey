**Yapman gerekenler:** imaja iki varsayılan yaz (`ENV`):

1. `APP_ENV=production`
2. `PYTHONUNBUFFERED=1`

Odyssey imajın ayarlarına da bakacak; ikinci çalıştırmada `-e APP_ENV=test`
verilecek ve `-e`'nin `ENV`'i ezdiği görülecek.

**Beklenen çıktılar:**

```
env: production
env: test
```
