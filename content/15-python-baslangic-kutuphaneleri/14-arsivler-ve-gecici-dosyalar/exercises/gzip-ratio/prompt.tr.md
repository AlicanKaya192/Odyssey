`gzip_ratio(text)` fonksiyonunu yaz: metni UTF-8 bayta çevirsin
(`encode`), `gzip.compress` ile sıkıştırsın ve **asıl boyut / sıkıştırılmış
boyut** oranını `round(..., 1)` ile döndürsün. 1'den küçükse sıkıştırma
dosyayı büyütmüş demektir.

**Beklenen çıktı:**

```
69.8
0.1
```
