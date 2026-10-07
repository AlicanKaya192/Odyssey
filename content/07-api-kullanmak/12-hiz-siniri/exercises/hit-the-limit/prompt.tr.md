`/limited` saniyede 3 isteğe izin veriyor. Sınıra bilerek çarp ve sunucunun
ne dediğine bak.

**Yapman gerekenler:**

1. `/limited`'e art arda (beklemeden) 5 istek gönder.
2. Her istek için sırasını, durum kodunu ve `X-RateLimit-Remaining`
   başlığını yazdır.
3. Sonda kaç isteğin `429` aldığını yazdır.

**Beklenen çıktı:**

```
1 200 remaining 2
2 200 remaining 1
3 200 remaining 0
4 429 remaining 0
5 429 remaining 0
too many: 2
```
