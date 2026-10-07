`/me` uç noktası jetonla giren kullanıcıyı söylüyor. Jeton: `letmein`.

**Yapman gerekenler:**

1. Jetonu **öneksiz** gönder (`Authorization: letmein`) ve durum kodunu
   yazdır; neden düştüğünü göreceksin.
2. Doğru biçimle gönder (`Authorization: Bearer letmein`); durum kodunu,
   kullanıcıyı ve rolünü yazdır.

**Beklenen çıktı:**

```
no prefix: 401
with Bearer: 200
user: ada
role: editor
```
