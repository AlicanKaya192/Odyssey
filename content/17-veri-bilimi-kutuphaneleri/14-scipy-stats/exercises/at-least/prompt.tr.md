`at_least(n, p, k)` `n` denemede başarı olasılığı `p` iken **en az** `k` başarı
olma olasılığını 4 basamağa yuvarlı döndürsün. `stats.binom(n, p).sf(x)`
"x'ten **büyük**" demek; "en az k" = "k − 1'den büyük". Başlangıç kodu
`sf(k)` yazıyor ve tam `k`'yi dışarıda bırakıyor.

**Beklenen çıktı:**

```
0.1719
0.8784
```
