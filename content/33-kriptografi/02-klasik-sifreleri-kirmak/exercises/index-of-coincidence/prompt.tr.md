`ioc(text)` metindeki harflerin (büyük-küçük harf fark etmez, harf
olmayanlar sayılmaz) tesadüf indeksini `round(..., 4)` ile döndürsün:
her harfin sayısı `n` için `n * (n - 1)` toplanır ve `N * (N - 1)`'e
bölünür (`N` toplam harf). İkiden az harf varsa `0.0`.

**Beklenen çıktı:**

```
0.0682
0.0
1.0
0.0
```
