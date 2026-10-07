`/stats` uç noktası anahtarsız kimseye cevap vermiyor. Önce anahtarsız dene,
sonra anahtarı başlıkta gönder.

Anahtar (alıştırma sunucusunun herkese açık okuyucu anahtarı):
`demo-key-123`, başlık adı `X-API-Key`.

**Yapman gerekenler:**

1. `/stats`'a anahtarsız istek gönder ve durum kodunu yazdır.
2. Aynı isteği `headers=` ile anahtarla gönder; durum kodunu, kitap sayısını
   ve en yeni kitabın yılını yazdır.

**Beklenen çıktı:**

```
without key: 401
with key: 200
books: 23
newest: 1986
```
