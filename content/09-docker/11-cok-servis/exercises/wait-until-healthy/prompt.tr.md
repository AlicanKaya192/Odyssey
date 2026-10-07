Bu sefer `web`'deki istemci **tek bir istek** atıp bitiyor: API hazır değilse
düşüyor. API açılışta iki saniye hazırlık yapıyor.

**Yapman gerekenler:** compose.yaml'ı yaz:

1. `api`: imaj `./api`'den; bir sağlık denetimi:
   `test` = `["CMD", "python", "-c", "import urllib.request as u; u.urlopen('http://localhost:8000')"]`,
   `interval: 2s`, `timeout: 3s`, `retries: 15`.
2. `web`: imaj `./web`'den; `api` **sağlıklı** olunca başlasın
   (`depends_on` + `condition: service_healthy`).

Odyssey projeyi ayağa kaldırıp `web`'in günlüğünde `items: 3`'ü arayacak.
