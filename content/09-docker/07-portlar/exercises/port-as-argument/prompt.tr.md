Bir önceki bölümün `ENTRYPOINT` + `CMD` düzenini portla birleştir:
`docker run site` 8000'de, `docker run site 9000` 9000'de çalışsın.

**Yapman gerekenler:**

1. `ENTRYPOINT` ile her zaman `python -m http.server` çalışsın.
2. `CMD` ile varsayılan argüman `8000` olsun.

Odyssey konteyneri iki kez çalıştıracak: argümansız (8000) ve `9000`
argümanıyla (9000); ikisinde de sayfa gelmeli.
