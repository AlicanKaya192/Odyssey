`index.html`'i konteynerde çalışan bir web sunucusuyla yayınla.

**Yapman gerekenler:**

1. `python:3.13-slim`'den başla, çalışma klasörü `/srv` olsun.
2. `index.html`'i kopyala.
3. 8000 portunu `EXPOSE` ile belgele.
4. `python -m http.server 8000` çalışsın (exec biçimi; dört parça).

Odyssey konteyneri bir porta yayınlayıp `/` adresine istek atacak; sayfada
`Odyssey Docs` görünmeli. Kendin denemek için:
`docker run -d -p 8080:8000 site` ve tarayıcıda `localhost:8080`.
