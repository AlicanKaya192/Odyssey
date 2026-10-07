Belleğin ne kadarı sayılara, ne kadarı metne gidiyor?

**Yapman gerekenler:**

1. 20 000 siparişlik dosyayı yaz ve `df`'ye oku.
2. Sayı sütunlarını `df.select_dtypes("number")` ile, metin sütunlarını
   `df.select_dtypes(exclude="number")` ile ayır.
3. İki grubun belleğini `memory_usage(deep=True, index=False).sum()` ile
   ölç (`index=False` indeksi saymıyor).
4. Her grubun toplamdaki payını yüzde olarak, bir ondalığa yuvarlayıp
   yazdır: önce `numbers`, sonra `text` (örnek biçim: `numbers 12.3`).
5. Tablonun satır başına baytını (toplam / satır sayısı) bir ondalığa
   yuvarlayıp yazdır.

**Beklenen çıktı:**

```
numbers 31.8
text 68.2
100.5
```

Sekiz sütunun dördü metin, ama bellek payı yarıdan çok fazla.
