`tail_prob(mean, sd, limit)` ortalaması `mean`, sapması `sd` olan normal
dağılımda değerin `limit`'ten **büyük** olma olasılığını 4 basamağa yuvarlı
döndürsün (`stats.norm(...).sf(limit)`). Başlangıç kodu `cdf` kullanıyor: o
"limit ve altı" demek.

**Beklenen çıktı:**

```
0.0228
0.0228
```
