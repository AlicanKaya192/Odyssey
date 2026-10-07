`/offset/books` ofset ve sınırla sayfalıyor. Yanıt `{"items": [...], "offset":
.., "limit": .., "total": ..}` biçiminde.

**Yapman gerekenler:**

1. `limit=8` ile, `offset=0`'dan başlayarak bütün kitapları `items`
   listesine topla. Her istekten sonra `offset`'i `limit` kadar artır;
   `offset >= total` olunca dur.
2. İstenen her ofseti ve o istekte gelen kitap sayısını yazdır; sonunda
   toplamı yazdır.

**Beklenen çıktı:**

```
offset 0 -> 8 books
offset 8 -> 8 books
offset 16 -> 7 books
total: 23
```
