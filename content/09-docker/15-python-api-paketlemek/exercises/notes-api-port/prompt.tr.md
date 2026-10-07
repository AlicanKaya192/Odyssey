Program konteynerin içinde 8000 yerine **9000** portunu dinlesin. `app.py`'ye
ve Dockerfile'a dokunma; program portu `PORT` ortam değişkeninden okuyor.

**Yapman gerekenler:**

1. `.env`'de `PORT`'u 9000 yap.
2. `compose.yaml`'da bilgisayarın 8095'i konteynerin **9000**'ine gitsin.

Sağlık denetimi de portu `PORT`'tan okuduğu için ona dokunmana gerek yok.
Odyssey servisin `healthy` olmasını bekleyecek ve 9000'den `/health`'e
bakacak:

```
{"status": "ok"}
```
