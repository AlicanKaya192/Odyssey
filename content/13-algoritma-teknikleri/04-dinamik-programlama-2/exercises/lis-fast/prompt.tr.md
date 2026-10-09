`lis_length(values)` fonksiyonunu `O(n log n)`'de yaz: en uzun **kesin
artan** alt dizinin uzunluğunu döndürsün.

`tails` listesi tut; her `x` için `k = bisect.bisect_left(tails, x)`. `k`
listenin sonuysa `x`'i ekle, değilse `tails[k] = x`. Cevap `len(tails)`.

Son satır 200 000 elemanlı; `O(n²)` çözüm süre sınırına takılır.

**Beklenen çıktı:**

```
4
1
511
```
