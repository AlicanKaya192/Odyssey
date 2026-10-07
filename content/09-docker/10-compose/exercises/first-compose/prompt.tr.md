İlk compose.yaml'ını yaz.

**Yapman gerekenler:** `web` adında tek bir servis:

1. İmajı bu klasördeki Dockerfile'dan kursun (`build`).
2. Bilgisayarın 8090'ı konteynerin 8000'ine gitsin (`ports`; tırnak içinde).
3. `APP_ENV` ortam değişkeni `production` olsun (`environment`).

Odyssey dosyayı okuyacak, sonra `docker compose up` ile gerçekten ayağa
kaldırıp sayfaya istek atacak. Kendin denemek için `docker compose up -d
--build` ve tarayıcıda `localhost:8090`.
